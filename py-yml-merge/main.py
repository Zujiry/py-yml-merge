#!/bin/python3
from pathlib import Path
import yaml

__location__ = Path(__file__).parent


def yaml_loader(file_path):
    """
    Loading Yaml files
    :param file_path: Path to the file to load
    :return: yaml dictionary
    """
    with file_path.open('r') as f:
        data = yaml.safe_load(f)
    return data


def yaml_dump(file_path, data):
    """
    Dump dict as yaml file
    :param file_path: Path to dump dictionary content as yaml file to
    :param data: yaml dictionary
    """
    with file_path.open("w") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


# Return changes
def detect_changes(yf, yf_changed, sorted=False):
    result = {}
    for key in yf_changed.keys():
        if yf.get(key):
            result_rec = detect_changes_rec(yf[key], yf_changed[key], key, sorted)
            if result_rec:
                result.update(result_rec)
    return result


def detect_changes_rec(yf, yf_changed, top_key, sorted):
    result = {}
    if yf == yf_changed:
        return None
    elif type(yf) != type(yf_changed):
        result[top_key] = yf_changed
    elif type(yf_changed) == dict:
        for key in yf_changed.keys():
            if key not in yf:
                if result.get(top_key):
                    result[top_key].update({key: yf_changed[key]})
                else:
                    result[top_key] = {key: yf_changed[key]}
            else:
                print(f"Key2: {key}")
                tmp = detect_changes_rec(yf[key], yf_changed[key], key, sorted)
                if tmp:
                    if result.get(top_key):
                        result[top_key].update(tmp)
                    else:
                        result[top_key] = tmp
    elif type(yf_changed) == list:
        result = {}
        if not sorted:
            for item in yf_changed:
                if type(item) == dict:
                    if item not in yf:
                        result[top_key].append(item)
                elif item not in yf:
                    if result.get(top_key):
                        result[top_key].append(item)
                    else:
                        result[top_key] = [item]
                else:
                    tmp = detect_changes_rec(item, item, item, sorted)
                    if tmp:
                        if result.get(top_key):
                            result[top_key].update(tmp)
                        else:
                            result[top_key] = tmp
        else:
            for idx, item in enumerate(yf_changed):
                if idx > len(yf)-1:
                    if result.get(top_key):
                        result[top_key].append(item)
                    else:
                        result[top_key] = [item]
                else:
                    tmp = detect_changes_rec(yf[idx], item, None, sorted)
                if tmp:
                    if result.get(top_key):
                        result[top_key].append(tmp[None])
                    else:
                        result[top_key] = [tmp[None]]
    elif type(yf_changed) in [str, float, int, complex]:
        result[top_key] = yf_changed
    return result


def apply_changes(yf, yf_apply, sorted=False):
    result = {}
    for key in yf_apply.keys():
        if yf.get(key):
            result_rec = detect_changes_rec(yf[key], yf_apply[key], key, sorted)
            if result_rec:
                result.update(result_rec)
        else:
            result.update(key)
    return result


def apply_changes_rec(yf, yf_changed, top_key, sorted):
    result = {}
    if yf == yf_changed:
        result[top_key] = yf_changed
    elif type(yf) != type(yf_changed):
        result[top_key] = yf_changed
    elif type(yf_changed) == dict:
        for key in yf_changed.keys():
            if not yf.get(key):
                result[top_key].update({key: yf_changed[key]})
            else:
                tmp = detect_changes_rec(yf[key], yf_changed[key], key, sorted)
                if tmp:
                    if result.get(top_key):
                        result[top_key].update(tmp)
                    else:
                        result[top_key] = tmp
    elif type(yf_changed) == list:
        result = {}
        if not sorted:
            for item in yf_changed:
                if type(item) == dict:
                    if item not in yf:
                        result[top_key].append(item)
                elif item not in yf:
                    if result.get(top_key):
                        result[top_key].append(item)
                    else:
                        result[top_key] = [item]
                else:
                    tmp = detect_changes_rec(item, item, item, sorted)
                    if tmp:
                        if result.get(top_key):
                            result[top_key].update(tmp)
                        else:
                            result[top_key] = tmp
        else:
            for idx, item in enumerate(yf_changed):
                if idx > len(yf)-1:
                    if result.get(top_key):
                        result[top_key].append(item)
                    else:
                        result[top_key] = [item]
                else:
                    tmp = detect_changes_rec(yf[idx], item, None, sorted)
                if tmp:
                    if result.get(top_key):
                        result[top_key].append(tmp[None])
                    else:
                        result[top_key] = [tmp[None]]
    elif type(yf_changed) in [str, float, int, complex]:
        result[top_key] = yf_changed
    return result


if __name__ == "__main__":
    #file_simple_old = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_simple_old.yml")
    #file_simple_original = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_simple_original.yml")
    #file_simple_changed = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_simple_changed.yml")
    # 1. Load files
    file_simple_old = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_config_old.yml")
    file_simple_tomerge = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_config_tomerge.yml")
    file_simple_changed = yaml_loader(__location__.parent / "tests/yaml-files/changes/file_config_changed.yml")

    #resulting_yaml = detect_changes(file_simple_original, file_simple_changed, sorted=True)
    #yaml_dump(__location__.parent / "tests/yaml-files/changes/file_simple_result.yml", resulting_yaml)
    # 2. Detect changes old and tomerge
    resulting_yaml = detect_changes(file_simple_old, file_simple_tomerge, sorted=False)
    yaml_dump(__location__.parent / "tests/yaml-files/changes/file_config_result.yml", resulting_yaml)
    # 3. Apply changes tomerge on new
    final_resulting_yaml = apply_changes(file_simple_changed, resulting_yaml, sorted=True)
    yaml_dump(__location__.parent / "tests/yaml-files/changes/file_config_final_result.yml", final_resulting_yaml)

