import os
import shutil

from src.utils import Params, save_json, save_txt, load_json, Logger


def train(config_path, checkpoint_dir, recover=True, force=False):
    if os.path.exists(checkpoint_dir):
        if force:
            shutil.rmtree(checkpoint_dir)
        elif not recover:
            raise ValueError(f"{checkpoint_dir} already exists!")
    os.makedirs(checkpoint_dir, exist_ok=True)

    logger = Logger(os.path.join(checkpoint_dir, "log"))

    config = load_json(config_path)


def eval(checkpoint_path, dataset_path):
    raise NotImplementedError()


def hyperparams_search(config_file, force=False):
    config_file_name = os.path.splitext(os.path.split(config_file)[1])[0]
    config = Params.from_file(config_file)
    hyp = config["hyp"]

    num_hyp = len(hyp)
    inds = [0] * num_hyp
    keys_list = []
    values_list = []
    len_search = []
    for k, v in hyp.items():
        keys_list.append(k)
        values_list.append(v)
        len_search.append(len(v))

    best_metric = 0
    best_model_dir = ""
    saved_model_list = []
    i = 0
    name = []
    while True:
        if inds[i] == len_search[i]:
            if i == 0:
                break
            inds[i] = 0
            i -= 1
            name.pop()
            continue

        if i == 0:
            name = []
        main_key, sub_key = keys_list[i].split(".")
        values = values_list[i][inds[i]]
        config[main_key][sub_key] = values
        inds[i] += 1
        name.append(sub_key + "-" + str(values))
        if i == num_hyp - 1:
            print(config.__dict__["params"])
            config_path = os.path.join("/tmp", config_file_name + '_' + '_'.join(name) + ".json")
            name.pop()
            save_json(config_path, config.__dict__["params"])

            model_dir = train()
            saved_model_list.append(model_dir)

            metric = eval()
            save_txt(os.path.join(model_dir, "res.txt"), [metric])
            if metric > best_metric:
                best_metric = metric
                best_model_dir = model_dir
        else:
            i += 1

    print("============================================")
    print("Best results: ", best_metric)
    print(best_model_dir + "\n\n")

    for d in saved_model_list:
        if d == best_model_dir:
            continue
        shutil.rmtree(d)
