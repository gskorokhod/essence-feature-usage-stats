from stats.essence_file import EssenceFile


class EssenceKeyword:
    def __init__(self, name: str, files=None):
        if files is None:
            files = []

        self.name = name

        self.file_usages = {}
        for file in files:
            if file not in self.file_usages and file.get_uses(self.name) > 0:
                self.file_usages[file] = file.get_uses(self.name)

        self.total_usages = sum(self.file_usages.values())
        self.max_usages = max(self.file_usages.values())
        self.min_usages = min(self.file_usages.values())

    def add_file(self, file: EssenceFile):
        if file not in self.file_usages and file.get_uses(self.name) > 0:
            usages = file.get_uses(self.name)
            self.file_usages[file] = usages
            self.total_usages += usages
            self.max_usages = max(self.max_usages, usages)
            self.min_usages = min(self.min_usages, usages)

    def get_files(self):
        return set(self.file_usages.keys())

    def get_file_paths(self, depth=0) -> list:
        return [x.get_fpath(depth) for x in self.get_files()]

    def get_num_files_using_feature(self) -> int:
        return len(self.get_files())

    def get_total_usages(self) -> int:
        return self.total_usages

    def get_avg_usages(self) -> float:
        return float(self.get_total_usages()) / float(self.get_num_files_using_feature())

    def get_min_usages(self) -> int:
        return self.min_usages

    def get_max_usages(self) -> int:
        return self.max_usages

    def get_usages_in_file(self, file) -> int:
        return file.get_uses(self.name)

    def as_json(self, path_depth=0) -> dict:
        return {
            'name': self.name,
            'used_in_files': self.get_file_paths(path_depth),
            'max_usages_in_file': self.get_max_usages(),
            'min_usages_in_file': self.get_min_usages(),
            'avg_usages_per_file': self.get_avg_usages(),
            'total_usages': self.get_total_usages()
        }
