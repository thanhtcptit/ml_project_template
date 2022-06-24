import os
import shutil

from pprint import pprint

from src.utils import Params, save_json, save_txt, load_json, Logger, get_current_time_str


def train(config_path, checkpoint_dir, recover=True, force=False):
    config = Params.from_file(config_path)
    pprint(config.as_dict())

    if not checkpoint_dir:
        config_name = os.path.splitext(os.path.basename(config_path))[0]
        checkpoint_dir = os.path.join("train_logs", config_name)
    if os.path.exists(checkpoint_dir):
        if force:
            shutil.rmtree(checkpoint_dir)
        elif not recover:
            raise ValueError(f"{checkpoint_dir} already exists!")
    os.makedirs(checkpoint_dir, exist_ok=True)
    shutil.copy(config_path, os.path.join(checkpoint_dir, "config.json"))
    print("Train log: ", checkpoint_dir)

    logger = Logger(os.path.join(checkpoint_dir, "log"), stdout=True)


def test(checkpoint_path, dataset_path):
    raise NotImplementedError()


def hyperparams_search(config_file, dataset_path, num_trials=50, force=False):
    import optuna

    def objective(trial):        
        config_name = os.path.splitext(os.path.basename(config_file))[0]
        config = load_json(config_file)
        hyp_config = config["hyp"]
        for k, v in hyp_config.items():
            k_list = k.split(".")
            d = config
            for i in range(len(k_list) - 1):
                d = d[k_list[i]]
            if v["type"] == "int":
                val = trial.suggest_int(k, v["range"][0], v["range"][1])
            elif v["type"] == "float":
                val = trial.suggest_float(k, v["range"][0], v["range"][1], log=v.get("log", False))
            elif v["type"] == "categorical":
                val = trial.suggest_categorical(k, v["values"])
            d[k_list[-1]] = val
            config_name += f"_{k_list[-1]}-{val}"

        config.pop("hyp")
        checkpoint_dir = f"/tmp/{config_name}"
        trial_config_file = os.path.join(f"/tmp/hyp_{get_current_time_str()}.json")
        save_json(trial_config_file, config)

        best_val = train(trial_config_file, checkpoint_dir, force=force)
        if dataset_path:
            best_val = test(checkpoint_dir, dataset_path)
        return best_val

    study = optuna.create_study(study_name="hyp", direction="maximize")
    study.optimize(objective, n_trials=num_trials, gc_after_trial=True,
                   catch=(tf.errors.InvalidArgumentError,))
    print("Number of finished trials: ", len(study.trials))

    df = study.trials_dataframe()
    print(df)

    print("Best trial:")
    trial = study.best_trial

    print(" - Value: ", trial.value)
    print(" - Params: ")
    for key, value in trial.params.items():
        print("  - {}: {}".format(key, value))

