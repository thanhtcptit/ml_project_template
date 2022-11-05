import os
import shutil

from tqdm import tqdm
from pprint import pprint

from src.utils import *


def train(config_path, dataset_path, checkpoint_dir, recover=True, force=False):
    config = Params.from_file(config_path)
    config["dataset_path"] = dataset_path
    pprint(config.as_dict())

    if not checkpoint_dir:
        dataset_name = get_basename(dataset_path)
        config_name = os.path.splitext(os.path.basename(config_path))[0]
        checkpoint_dir = os.path.join("train_logs", dataset_name, config_name)
    if os.path.exists(checkpoint_dir):
        if force:
            shutil.rmtree(checkpoint_dir)
        else:
            raise ValueError(f"{checkpoint_dir} already existed")
    os.makedirs(checkpoint_dir, exist_ok=True)
    save_json(os.path.join(checkpoint_dir, "config.json"), config.as_dict())
    print("Train log: ", checkpoint_dir)

    logger = Logger(os.path.join(checkpoint_dir, "log.txt"), stdout=True)


def test(checkpoint_dir, test_dataset_path):
    config = Params.from_file(os.path.join(checkpoint_dir, "config.json"))

    return 1


def hyperparams_search(config_file, dataset_path, test_dataset_path, num_trials=50, force=False):
    import optuna

    def objective(trial):
        dataset_name = get_basename(dataset_path)    
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
        checkpoint_dir = f"/tmp/{dataset_name}/{config_name}"
        trial_config_file = os.path.join(f"/tmp/hyp_{get_current_time_str()}.json")
        save_json(trial_config_file, config)

        best_val = train(trial_config_file, dataset_path, checkpoint_dir, force=force)
        if test_dataset_path:
            best_val = test(checkpoint_dir, test_dataset_path)
        return best_val

    study = optuna.create_study(study_name="hyp", direction="maximize")
    study.optimize(objective, n_trials=num_trials, gc_after_trial=True,
                   catch=())
    print("Number of finished trials: ", len(study.trials))

    df = study.trials_dataframe()
    print(df)

    print("Best trial:")
    trial = study.best_trial

    print(" - Value: ", trial.value)
    print(" - Params: ")
    for key, value in trial.params.items():
        print("  - {}: {}".format(key, value))

