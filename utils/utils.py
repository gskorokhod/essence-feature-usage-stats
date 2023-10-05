import os
from collections.abc import Iterable


def trim_path(input_path, num_elements=0):
    if num_elements == 0:
        return input_path

    normalized_path = os.path.normpath(input_path)
    path_elements = normalized_path.split(os.path.sep)

    # Ensure num_elements is not greater than the length of the path
    num_elements = min(num_elements, len(path_elements))

    # Join the last num_elements elements to form the trimmed path
    trimmed_path = os.path.sep.join(path_elements[-num_elements:])

    return trimmed_path


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x, minn, maxn):
    return min(max(x, minn), maxn)
