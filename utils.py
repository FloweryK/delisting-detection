import pickle
import json
import os


def save(data, path):
    if path[-4:] == 'json':
        with open(path, 'w', encoding='UTF8') as f:
            json.dump(data, f, ensure_ascii=False)
    else:
        with open(path, 'wb') as f:
            pickle.dump(data, f)


def load(path):
    if path[-4:] == 'json':
        with open(path, encoding='UTF8') as f:
            result = json.load(f)
    else:
        with open(path, 'rb') as f:
            result = pickle.load(f)

    return result


def listdir(*args):
    return os.listdir(os.path.join(*args))
