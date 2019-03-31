def get_from_dict(d, keys):
    if len(keys) == 0:
        return d
    else:
        return get_from_dict(d[keys[0]], keys[1:])
