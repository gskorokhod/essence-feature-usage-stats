import json
import os
import subprocess

from utils.utils import trim_path


def find_essence_files(dir_path) -> list:
    """
    Find all essence files in a given directory and return a list of full paths to them
    :param dir_path: path to directory
    :return: a generator of paths to essence files
    """

    # Ensure the directory path is valid
    if not os.path.isdir(dir_path):
        raise ValueError(f"The provided path '{dir_path}' is not a valid directory.")

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.essence'):
                yield os.path.join(root, file)


def get_essence_file_ast(fpath, conjure_path) -> dict:
    """
    Run the `conjure pretty` command line tool and get the parsed AST as a dict
    ToDo: Instead of relying on a conjure binary being provided, download one automatically if needed
    :param conjure_path: path to conjure binary
    :param fpath: path to an essence file
    :return: the Abstract Syntax Tree in json format (as a dict)
    """
    result = subprocess.run([conjure_path,
                             "pretty",
                             "--output-format=astjson",
                             fpath],
                            capture_output=True,
                            text=True)
    ast_json = json.loads(result.stdout)
    return ast_json


def flat_keys_count(data, blocklist=None) -> dict:
    """
    Recurse over a dict or list (potentially with nested dicts / lists) and count all dictionary keys
    ToDo: Allowlist functionality
    :param data: a dictionary or list containing dictionaries / lists
    :param blocklist: collection of keys to ignore
    :return: dict in the format of <Key>:<№ of key's occurrences in data>
    """

    ans = {}

    def add_key(key, count=1):
        if (blocklist is None) or (key not in blocklist):
            if key in ans.keys():
                ans[key] += count
            else:
                ans[key] = count

    def recurse_and_add_keys(item):  # Recurse over entry (list or dict) and add its keys to the count
        if isinstance(item, (list, dict)):
            new_keys = flat_keys_count(item)
            for key in new_keys.keys():
                add_key(key, new_keys[key])

    if isinstance(data, dict):  # If it's a dict, add its keys and recurse over the values
        for key in data.keys():
            add_key(key)
            recurse_and_add_keys(data[key])
    elif isinstance(data, list):  # If it's a list, recurse over all its elements
        for entry in data:
            recurse_and_add_keys(entry)

    return ans


def get_features_used_in_file(fpath, conjure_path, blocklist=None):
    """
    Given a path to an essence file, return counts for Essence language features used in the file
    :param conjure_path: path to conjure binary
    :param fpath: path to an essence file
    :param blocklist: keywords to ignore
    :return: dict in the format of <Key>:<№ Of occurrences in file>
    """
    ast = get_essence_file_ast(fpath, conjure_path)
    return flat_keys_count(ast, blocklist=blocklist)


def process_essence_files(dir_path, conjure_path, blocklist=None):
    """
    Given a path to a directory containing Essence files, get stats for how often they use Essence language features
    :param conjure_path: path to conjure binary
    :param dir_path: - path to directory containing Essence files
    :param blocklist: - Essence keywords to ignore
    :return: - a generator of file stats in the format (path, {'Keyword':<Count>})
    """

    ans = {}

    essence_files = find_essence_files(dir_path)
    for fpath in essence_files:
        try:
            yield fpath, get_features_used_in_file(fpath, conjure_path, blocklist=blocklist)
        except Exception as e:
            print(f'Exception "{e}" while processing Essence file: {fpath}')


def get_feature_stats(dir_path, conjure_path, blocklist=None, path_depth=0):
    """
    :param dir_path: path to directory containing Essence files
    :param conjure_path: path to conjure binary
    :param blocklist: list of Essence keywords to ignore
    :param path_depth: trim Essence file paths to a given depth for display
           (for example foo/bar/baz with path_depth=2 will be trimmed to bar/baz)
    :return: ToDo - rework this function to return stats in a more robust and usable format (create a class?)
    """

    counts = {}
    features = {}

    for fpath, data in process_essence_files(dir_path, conjure_path, blocklist=blocklist):
        fpath = trim_path(fpath, path_depth)

        counts[fpath] = data
        # features = features.union(data.keys())
        for key in data.keys():
            if key not in features.keys():
                features[key] = {
                    'max_in_file': data[key],
                    'total_uses': data[key],
                    'n_files': 1
                }
            else:
                features[key]['max_in_file'] = max(features[key]['max_in_file'], data[key])
                features[key]['total_uses'] += data[key]
                features[key]['n_files'] += 1

    for key in features.keys():
        features[key]['avg_in_file'] = features[key]['total_uses'] / features[key]['n_files']

    return counts, features
