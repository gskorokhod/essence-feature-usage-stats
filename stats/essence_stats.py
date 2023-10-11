import os

from stats.essence_feature import EssenceKeyword
from stats.essence_file import EssenceFile
from utils.git import sync_repo


class EssenceStats:
    """
    Class that stores stats for a given directory with
    """
    def __init__(self, essence_dir: str, conjure_bin: str,
                 remote_repo_url=None, remote_branch='master', remote_name='origin',
                 blocklist=None):
        self.essence_dir = os.path.abspath(essence_dir)
        self.conjure_bin = os.path.abspath(conjure_bin)

        self.essence_keywords = {}
        self.essence_files = {}
        self.remote_repo_url = remote_repo_url
        self.remote_branch = remote_branch
        self.remote_name = remote_name
        self.repo = None

        if remote_repo_url is not None:
            try:
                self.sync_repo(remote_repo_url, remote_branch, remote_name)
            except Exception as e:
                raise ValueError(f'Not a valid git repository url: {remote_repo_url}')

        self.update_stats()

    def update_stats(self):
        for file in EssenceFile.get_essence_files_from_dir(self.essence_dir, self.conjure_bin):
            self.essence_files[file.get_fpath()] = file

            for keyword in file.get_keywords():
                if keyword not in self.essence_keywords.keys():
                    self.essence_keywords[keyword] = EssenceKeyword(keyword)
                self.essence_keywords[keyword].add_file(file)

    def sync_repo(self, remote_repo_url=None, remote_branch=None, remote_name=None):
        if remote_repo_url is None:
            remote_repo_url = self.remote_repo_url
        if remote_branch is None:
            remote_branch = self.remote_branch
        if remote_name is None:
            remote_name = self.remote_name

        try:
            self.repo = sync_repo(self.essence_dir, remote_repo_url, remote_name=remote_name, branch=remote_branch)
            self.update_stats()

            self.remote_repo_url = remote_repo_url
            self.remote_branch = remote_branch
            self.remote_name = remote_name
        except Exception as e:
            raise ValueError(f'Not a valid git repository url: {remote_repo_url}')

    def get_essence_files(self):
        return self.essence_files.values()

    def get_essence_keywords(self):
        return self.essence_keywords.values()

    def get_stats_for_file(self, fpath):
        return self.essence_files.get(fpath, None)

    def get_stats_for_keyword(self, keyword):
        return self.essence_keywords.get(keyword, None)

    def as_json(self, path_depth=0):
        return {
            'essence_files': [x.as_json(path_depth) for x in self.get_essence_files()],
            'essence_keywords': [x.as_json(path_depth) for x in self.get_essence_keywords()]
        }


def get_essence_stats(dir_path, conjure_path, blocklist=None, path_depth=0,
                      remote_repo_url=None, remote_branch='master', remote_name='origin'):
    """
    :param remote_repo_url: url of git repository to sync ()
    :param remote_branch:
    :param remote_name:
    :param dir_path: path to directory containing Essence files
    :param conjure_path: path to conjure binary
    :param blocklist: list of Essence keywords to ignore
    :param path_depth: trim Essence file paths to a given depth for display
           (for example foo/bar/baz with path_depth=2 will be trimmed to bar/baz)
    :return: (counts, features) where:
             counts is a dictionary in the format: {<filepath>: {<keyword>: <n_usages>}}
             features is a dictionary in the format: {<keyword>: {<stat>: <value>}}
    ToDo - rework this function to return stats in a more robust and usable format (create a class?)
    """
    stats = EssenceStats(dir_path, conjure_path, remote_repo_url, remote_branch, remote_name, blocklist)
    return stats.as_json(path_depth)
