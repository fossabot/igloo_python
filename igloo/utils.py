def get_from_dict(dict, keys):
    if len(keys) == 0:
        return dict
    else:
        return get_from_dict(dict[keys[0]], keys[1:])
