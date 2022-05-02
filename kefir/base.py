import datetime
import inspect
import json

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

    def _is_good_field(self, field, reprsnt, item, ignore):
        return not field.startswith("_") and field not in reprsnt.ignore and item is not ignore

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
                    "No look function for `{name}` field declared in `Repr.look`!"
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
                if moment == "dump":
                    if e.args:
                        dct[name] = e.args[0]
                    else:
                        dct[name] = f"`{name}` is not valid!"
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
                    "No validate function for `{name}` field declared in `Repr.validate!`"
                )
        return dct

    def _dump_obj(self, obj, ignore=None):
        dct = {}
        reprsnt = self.represents.get(type(obj))
        if hasattr(obj, "__slots__"):
            fields_list = obj.__slots__
        else:
            # otherwise check if object is SQLAlchemy model
            if obj.__dict__.get("_sa_instance_state"):
                fields_list = (
                    obj.__dict__["_sa_instance_state"]
                    .__dict__["manager"]
                    .__dict__["local_attrs"]
                ).keys()
            else:
                fields_list = obj.__dict__.keys()
        if reprsnt is not None:
            for field in fields_list:
                item = getattr(obj, field)
                if self._is_good_field(field, reprsnt, item, ignore):
                    if isinstance(item, (int, str, bool, dict, float)):
                        dct[reprsnt.names_map.get(field, field)] = item
                    elif isinstance(item, datetime.datetime):
                        dct[reprsnt.names_map.get(field, field)] = item.strftime(
                            reprsnt.datetime_format
                        )
                    else:
                        dct[reprsnt.names_map.get(field, field)] = self.dump(item, obj)
            # i deleted `extra` field because this is not what i want to see
            # see here ->
            # https://github.com/Yourun-proger/kefir/wiki/Docs#what-worries-me
            # point 5
            dct = self._add_look(dct, reprsnt)
            dct = self._validate(dct, reprsnt, "dump")
        else:
            for field in fields_list:
                item = getattr(obj, field)
                if not field.startswith("_") and item is not ignore:
                    if isinstance(item, (int, str, bool, dict, float)):
                        dct[field] = item
                    elif isinstance(item, datetime.datetime):
                        dct[field] = item.strftime(self.datetime_format)
                    else:
                        dct[field] = self.dump(item, obj)
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

    def load(self, dct, cls, allow_dict=False):
        if isinstance(dct, list):
            lst = []
            for item in dct:
                lst.append(self.load(item, cls, allow_dict))
            return lst
        if isinstance(dct, str):
            if dct.endswith(".json"):
                try:
                    with open(dct, "r") as json_file:
                        dct = json.loads(json_file.read())
                except FileNotFoundError:
                    raise ValueError(
                        "\nWhere is json file?!\n" f'I can\'t found it here: "{dct}"'
                    ) from None
            else:
                raise ValueError(
                    "\nIf you want to feed me a json file,\n"
                    "please change/add the .json extension."
                )
        reprsnt = self.represents.get(cls)
        if reprsnt is None:
            for k, v in dct.items():
                if isinstance(v, dict) and not allow_dict:
                    raise NeedReprException(
                        f"\nThis object with the nested data.\nAdd Repr for `{cls.__name__}` class!\n"
                        f"In Repr, `{k}` field must be added to `loads` dict"
                    )
            try:
                if hasattr(cls, "__tablename__"):
                    return cls(**dct)
                return cls(*dct.values())
            except TypeError as e:
                err_msg = str(e).partition(')')[2]
                raise DeserializationException(f"\nBad dict where are{err_msg}") from None
        else:
            new_dct = {}
            names_map = {v: k for k, v in reprsnt.names_map.items()}
            for k, v in dct.items():
                if isinstance(v, dict) and not allow_dict:
                    sub_cls = reprsnt.loads[names_map.get(k, k)]
                    # i don't add `allow_dict` here because it's strange and dangerous!
                    new_dct[names_map.get(k, k)] = self.load(v, sub_cls)
                elif isinstance(v, list):
                    new_dct[names_map.get(k, k)] = [
                        self.load(i, reprsnt.loads[k]) for i in v
                    ]
                elif isinstance(
                    reprsnt.loads.get(names_map.get(k, k)), datetime.datetime
                ):
                    new_dct[names_map.get(k, k)] = datetime.datetime.strptime(
                        v, reprsnt.datetime_format
                    )
                else:
                    new_dct[names_map.get(k, k)] = v
            new_dct = self._validate(new_dct, reprsnt, "load")
            try:
                if hasattr(cls, "__tablename__"):
                    return cls(**new_dct)
                return cls(*new_dct.values())
            except TypeError as e:
                err_msg = str(e).partition(')')[2]
                raise DeserializationException(f"\nBad dict where are{err_msg}") from None
