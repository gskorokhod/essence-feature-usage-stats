import json
import subprocess


def get_essence_file_ast(fpath, conjure_bin_path) -> dict:
    """
    Run the `conjure pretty` command line tool and get the parsed AST as a dict
    ToDo: Instead of relying on a conjure binary being provided, download one automatically if needed
    :param conjure_path: path to conjure binary
    :param fpath: path to an essence file
    :return: the Abstract Syntax Tree in json format (as a dict)
    """

    result = subprocess.run([conjure_bin_path,
                             "pretty",
                             "--output-format=astjson",
                             fpath],
                            capture_output=True,
                            text=True)
    ast_json = json.loads(result.stdout)
    return ast_json


def get_version(conjure_bin_path) -> tuple:
    """
    Get version from conjure. Not useful now but maybe use this to auto-update conjure from git repo in the future?
    :param conjure_bin_path: path to conjure binary
    :return: tuple of (version, commit) - conjure version and git repo version (as given by conjure --version)
    """
    result = subprocess.run([conjure_bin_path,
                             "--version"],
                            capture_output=True,
                            text=True)

    version, commit = None, None
    lines = result.stdout.split('\n')
    for line in lines:
        if 'Release version' in line:
            version = line.lstrip('Release version ')
        if 'Repository version' in line:
            commit, *ts_parts = line.lstrip('Repository version ').split()

    return version, commit
