def map_range(x, in_min, in_max, out_min, out_max):
    if in_min == in_max:
        return out_min + (out_max - out_min) / 2
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x, minn, maxn):
    return min(max(x, minn), maxn)
