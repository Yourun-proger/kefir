import datetime
import inspect

from kefir.exceptions import (
    NeedReprException,
    DeserializationException,
    NeedFunctionException,
)


class BaseKefir:
    def __init__(self, represents=None, datetime_format="%d.%m.%Y", used="flask"):
        if represents is None:
            represents = {}
        self.represents = represents
        self.datetime_format = datetime_format
        self.used = used

    def _add_look(self, dct, reprsnt):
        for name in reprsnt.look:
            try:
                dct[name] = list(
                    filter(
                        lambda x: x.name.startswith(f"look_{name}"),
                        inspect.classify_class_attrs(reprsnt),
                    )
                )[0].object(dct[name])
            except IndexError:
                raise NeedFunctionException(
                    'No look function for `{name}` field declared in `Repr.look`!'
                )
        return dct

    def _validate(self, dct, reprsnt, moment):
        for name in reprsnt.validate:
            try:
                list(
                    filter(
                        lambda x: x.name.startswith(f"validate_{name}"),
                        inspect.classify_class_attrs(reprsnt),
                    )
                )[0].object(dct[name])
            except AssertionError as e:
                if moment == 'dump':
                    if e.args:
                        dct[name] = e.args[0]
                    else:
                        dct[name] = f'`{name}` is not valid!'
                else:
                    if e.args:
                        raise DeserializationException(
                            f"\nCan't deserialize `{name}` field\n{e.args[0]}"
                        ) from None
                    raise DeserializationException(
                        f"\nCan't deserialize `{name}` field!"
                    ) from None
            except IndexError:
                raise NeedFunctionException(
                    'No validate function for `{name}` field declared in `Repr.validate!`'
                )
        return dct

    def _dump_obj(self, obj, ignore=None):
        dct = {}
        reprsnt = self.represents.get(type(obj))
        if hasattr(obj, "__slots__"):
            # make dict for objects with `__slots__`
            obj_dct = {k: getattr(obj, k) for k in obj.__slots__}
        else:
            # otherwise check if object is SQLAlchemy model
            if obj.__dict__.get("_sa_instance_state"):
                obj_dct = (
                    obj.__dict__["_sa_instance_state"]
                    .__dict__["manager"]
                    .__dict__["local_attrs"]
                )
            else:
                obj_dct = obj.__dict__
        if reprsnt is not None:
            for k, v in obj_dct.items():
                item = getattr(obj, k)
                if not k.startswith("_") and k not in reprsnt.ignore:
                    if item is not ignore:
                        if isinstance(item, (int, str, bool, dict, float)):
                            dct[reprsnt.names_map.get(k, k)] = item
                        elif isinstance(item, datetime.datetime):
                            dct[reprsnt.names_map.get(k, k)] = item.strftime(
                                reprsnt.datetime_format
                            )
                        else:
                            dct[reprsnt.names_map.get(k, k)] = self.dump(item, obj)
            # i deleted `extra` field because this is not what i want to see
            # see here ->
            # https://github.com/Yourun-proger/kefir/wiki/Docs#what-worries-me
            # point 5
            dct = self._add_look(dct, reprsnt)
            dct = self._validate(dct, reprsnt, 'dump')
        else:
            for k, v in obj_dct.items():
                item = getattr(obj, k)
                if not k.startswith("_") and item is not ignore:
                    if isinstance(item, (int, str, bool, dict, float)):
                        dct[k] = item
                    elif isinstance(item, datetime.datetime):
                        dct[k] = item.strftime(self.datetime_format)
                    else:
                        dct[k] = self.dump(item, obj)
        return dct

    def _dump_list(self, list_of_objs, ignore):
        lst = []
        for obj in list_of_objs:
            lst.append(self.dump(obj, ignore))
        return lst

    def dump(self, obj, ignore=None):
        if isinstance(obj, list):
            return self._dump_list(obj, ignore)
        return self._dump_obj(obj, ignore)

    def load(self, dct, cls):
        if isinstance(dct, list):
            lst = []
            for item in dct:
                lst.append(self.load(item, cls))
            return lst
        reprsnt = self.represents.get(cls)
        if reprsnt is None:
            for k, v in dct.items():
                if isinstance(v, dict):
                    raise NeedReprException(
                        f"\nThis object with the nested data.\nAdd Repr for `{cls}` class!\n"
                        f"In Repr, `{k}` field must be added to `loads` dict"
                    )
            if hasattr(cls, "__tablename__"):
                return cls(**dct)
            return cls(*dct.values())
        else:
            new_dct = {}
            names_map = {v: k for k, v in reprsnt.names_map.items()}
            for k, v in dct.items():
                if isinstance(v, dict):
                    sub_cls = reprsnt.loads[names_map.get(k, k)]
                    new_dct[names_map.get(k, k)] = self.load(v, sub_cls)
                elif isinstance(v, list):
                    new_dct[names_map.get(k, k)] = [
                        self.load(i, reprsnt.loads[k]) for i in v
                    ]
                elif reprsnt.loads.get(names_map.get(k, k)) is datetime.datetime:
                    new_dct[names_map.get(k, k)] = datetime.datetime.strptime(v, reprsnt.datetime_format)
                else:
                    new_dct[names_map.get(k, k)] = v
            new_dct = self._validate(new_dct, reprsnt, 'load')
            if hasattr(cls, "__tablename__"):
                return cls(**new_dct)
            return cls(*new_dct.values())
