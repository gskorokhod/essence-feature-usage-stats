import os
from pathlib import Path

from utils.conjure import get_essence_file_ast
from utils.files import count_lines, trim_path
from utils.misc import flat_keys_count


class EssenceFileError(ValueError):
    pass


class EssenceFileInvalidPathError(EssenceFileError):
    def __init__(self, fpath):
        super().__init__(f"Not a valid Essence file: {fpath}")


class EssenceFileNotParsableError(EssenceFileError):
    def __init__(self, fpath, msg=None):
        message = f"Essence file could not be parsed: {fpath}"
        if msg:
            message += f", reason: {msg}"

        super().__init__(message)


class EssenceInvalidDirectoryError(ValueError):
    def __init__(self, dir_path):
        super().__init__(f"The provided path '{dir_path}' is not a valid directory")


def find_essence_files(dir_path: str | Path):
    """
    Find all essence files in a given directory and return a list of full paths to them
    :param dir_path: path to directory
    :return: a generator of paths to essence files
    """

    dir_path = Path(dir_path)

    # Ensure the directory path is valid
    if not dir_path.is_dir():
        raise EssenceInvalidDirectoryError

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(dir_path):
        for file in files:
            fpath = Path(root) / file
            if fpath.is_file() and fpath.suffix == ".essence":
                yield fpath


class EssenceFile:
    """
    EssenceFile stores keyword counts and number of lines for a given file "fpath".
    """

    # ToDo use python getters / setters instead of java style,
    #  search: "python function as attribute" or ask Nik

    # ToDo some attrs should be private?

    def __init__(self, fpath: str | Path, conjure_bin_path, blocklist=None):
        fpath = Path(fpath).resolve()

        if not (fpath.is_file() and fpath.suffix == ".essence"):
            raise EssenceFileInvalidPathError(fpath)
        try:
            self.fpath = Path.resolve(fpath)
            self.ast = get_essence_file_ast(
                self.fpath,
                conjure_bin_path=conjure_bin_path,
            )
            self.keyword_counts = flat_keys_count(self.ast, blocklist)
            self.n_lines = count_lines(fpath)
        except Exception as e:
            raise EssenceFileNotParsableError(fpath, str(e)) from e

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

    def __eq__(self, other):
        return self.fpath == other.fpath

    def __str__(self):
        return f"EssenceFile({self.fpath}): {self.n_lines} lines"

    def as_json(self, path_depth=0) -> dict:
        return {
            "path": self.get_fpath(path_depth),
            "ast": self.get_ast(),
            "keyword_counts": self.get_keyword_counts(),
            "n_lines": self.get_n_lines(),
        }

    @staticmethod
    def get_essence_files_from_dir(dir_path, conjure_bin_path, blocklist=None):
        for fpath in find_essence_files(dir_path):
            try:
                file = EssenceFile(fpath, conjure_bin_path, blocklist=blocklist)
                yield file
            except Exception as e:  # noqa: PERF203
                print(f'Could not process file "{fpath}", throws exception: {e}')
