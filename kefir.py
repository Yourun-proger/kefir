import re
def dump_to_dict(model, one=True):
    if one:
        dct = {}
        for key, value in model.__dict__.items():
            if not key.startswith('_'):
                if re.search('<__main__..*>', str(value)):
                    dct[key] = dump_to_dict(value)
                else:
                    dct[key] = value
        try:
            dct['id'] = model.id
        except AttributeError:
            pass
        return dct
    else:
        models = []
        for m in model:
            model_dct = {}
            for key, value in m.__dict__.items():
                if not key.startswith('_'):
                    if re.search('<__main__..*>', str(value)):
                        model_dct[key] = dump_to_dict(value)
                    else:
                        model_dct[key] = value
            try:
                model_dct['id'] = model.id
            except AttributeError:
                pass
            models.append(model_dct)
        return models
