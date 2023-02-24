#!/bin/python3
from pathlib import Path
import yaml


def yaml_loader(file_path):
    with file_path.open('r') as f:
        data = yaml.safe_load(f)
    return data

def yaml_dump(file_path, data):
    with file_path.open("w") as f:
        yaml.dump(data, f, allow_unicode=True)

# Return changes
def changes_from_yaml_file(yf, yf_changed):
    result = {}
    for key in yf_changed.keys():
        if yf.get(key):
            result_rec = changes_from_yaml_file_rec(yf[key], yf_changed[key], key)
            if result_rec:
                result.update(result_rec)
    return result

def changes_from_yaml_file_rec(yf, yf_changed, top_key):
    result = {}
    if yf == yf_changed:
        return None
    elif type(yf) != type(yf_changed):
        result[top_key] = yf_changed
    elif type(yf_changed) == dict:
        for key in yf_changed.keys():
            if not yf.get(key):
                result[top_key].update({key: yf_changed[key]})
            else:
                tmp = changes_from_yaml_file_rec(yf[key], yf_changed[key], key)
                if tmp:
                    if result.get(top_key):
                        result[top_key].update(tmp)
                    else:
                        result[top_key] = tmp
    elif type(yf_changed) == list:
        result = []
        for item in yf_changed:
            if type(item) == dict:
                
            elif item not in yf:
                print(str(item) + " NOT IN " + str(yf))
                result.append(item)
            else:
                print("LIST " + str(yf))
                print("LIST " + str(yf_changed))
                print("LIST " + str(item))                           
                tmp = changes_from_yaml_file_rec(item, item, item)
                if tmp:
                    if result.get(top_key):
                        result[top_key].update(tmp)
                    else:
                        result[top_key] = tmp
    elif type(yf_changed) in [str, float, int, complex]:
        result[top_key] = yf_changed
    return result

if __name__ == "__main__":
    result_config = {}
    config_old = yaml_loader(Path("to-merge-config/test.yml"))
    config_ui = yaml_loader(Path("to-merge-config/test2.yml"))
    result = changes_from_yaml_file(config_old, config_ui)
    print(result)
    yaml_dump(Path("to-merge-config/result.yml"), result)
