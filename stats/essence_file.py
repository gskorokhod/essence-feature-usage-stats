import os

from utils.conjure import get_essence_file_ast
from utils.files import count_lines, trim_path
from utils.misc import flat_keys_count


def find_essence_files(dir_path: str):
    """
    Find all essence files in a given directory and return a list of full paths to them
    :param dir_path: path to directory
    :return: a generator of paths to essence files
    """

    # Ensure the directory path is valid
    if not os.path.isdir(dir_path):
        raise ValueError(f"The provided path '{dir_path}' is not a valid directory")

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(dir_path):
        for file in files:
            fpath = os.path.join(root, file)
            if os.path.isfile(fpath) and fpath.endswith('.essence'):
                yield fpath


class EssenceFile:
    """
    EssenceFile stores keyword counts and number of lines for a given file "fpath".
    """

    def __init__(self, fpath: str, conjure_bin_path, blocklist=None):
        if not os.path.exists(fpath):
            raise ValueError(f'File does not exist: {fpath}')
        if not os.path.isfile(fpath):
            raise ValueError(f'Not a file: {fpath}')
        if not fpath.endswith('.essence'):
            raise ValueError(f'Not an file: {fpath}')

        try:
            self.fpath = os.path.abspath(fpath)
            self.ast = get_essence_file_ast(self.fpath, conjure_bin_path=conjure_bin_path)
            self.keyword_counts = flat_keys_count(self.ast, blocklist)
            self.n_lines = count_lines(fpath)
        except Exception as e:
            raise ValueError(f'Invalid Essence file {fpath}. Trying to parse results in exception: {e}')

    def get_keyword_counts(self) -> dict:
        return self.keyword_counts

    def get_n_lines(self) -> int:
        return self.n_lines

    def get_ast(self) -> dict:
        return self.ast

    def get_fpath(self, depth=0) -> str:
        return trim_path(self.fpath, depth)

    def get_uses(self, keyword) -> int:
        return self.get_keyword_counts().get(keyword, 0)

    def get_keywords(self) -> set:
        return set(self.get_keyword_counts().keys())

    def __hash__(self):
        return hash(self.fpath)

    def __eq___(self, other):
        return self.fpath == other.fpath

    def __str__(self):
        return f'EssenceFile({self.fpath}): {self.n_lines} lines'

    def as_json(self, path_depth=0) -> dict:
        return {
            'path': self.get_fpath(path_depth),
            'ast': self.get_ast(),
            'keyword_counts': self.get_keyword_counts(),
            'n_lines': self.get_n_lines()
        }

    @staticmethod
    def get_essence_files_from_dir(dir_path, conjure_bin_path, blocklist=None):
        for fpath in find_essence_files(dir_path):
            try:
                file = EssenceFile(fpath, conjure_bin_path, blocklist=blocklist)
                yield file
            except Exception as e:
                print(f'Could not process file "{fpath}", throws exception: {e}')
