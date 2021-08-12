def dump(model):
    dct = {}
    for key, value in model.__dict__.items():
        if not key.startswith('_'):
            if not isinstance(value, int)  and \
                not isinstance(value, str) and \
                not isinstance(value, bool) and \
                not isinstance(value, dict) and \
                not isinstance(value, float):
                dct[key] = dump(value)
            else:
                dct[key] = value
    return dct
