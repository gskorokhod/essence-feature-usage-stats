import os


def count_lines(fpath):
    with open(fpath, "rbU") as f:
        return sum(1 for _ in f)


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
