"""
Kefir file
"""

import datetime
import functools
import inspect
import json
import re

try:
    from flask import Response as FlaskResponse
except ImportError:
    FlaskResponse = None

try:
    from fastapi.responses import JSONResponse as FastAPIResponse
except ImportError:
    FastAPIResponse = None

__version__ = '0.1.2'


class Kefir:
    def __init__(self, represents=None, datetime_format='%d.%m.%Y', used="flask"):
        if represents is None:
            represents = {}
        self.represents = represents
        self.datetime_format = datetime_format
        self.used = used

    def dump(self, obj, ignore=None):
        if isinstance(obj, list):
            lst = []
            for item in obj:
                lst.append(self.dump(item, ignore))
            return lst
        dct = {}
        reprsnt = self.represents.get(type(obj))
        no_repr = bool(reprsnt is None)
        ignorecase = []
        if not no_repr:
            ignorecase = reprsnt.ignore or ignorecase
        if hasattr(obj, "__slots__"):
            for k in obj.__slots__:
                if isinstance(getattr(obj, k), (int, str, bool, dict, float)):
                    if no_repr or reprsnt.names_map is None:
                        dct[k] = getattr(obj, k)
                    else:
                        dct[reprsnt.names_map.get(k, k)] = getattr(obj, k)
                elif isinstance(getattr(obj, k), datetime.datetime):
                    if no_repr:
                        dct[k] = getattr(obj, k).strftime(self.datetime_format)
                    else:
                        dct[k] = getattr(obj, k).strftime(reprsnt.datetime_format)
                else:
                    if no_repr or reprsnt.names_map is None:
                        dct[k] = self.dump(getattr(obj, k), obj)
                    else:
                        dct[reprsnt.names_map.get(k, k)] = self.dump(getattr(obj, k), obj)
        else:
            if obj.__dict__.get("_sa_instance_state"):
                for k, v in (
                        obj.__dict__["_sa_instance_state"].__dict__["manager"].__dict__["local_attrs"].items()
                ):
                    item = getattr(obj, k)
                    if not k.startswith("_") and k not in ignorecase:
                        if item is not ignore:
                            if isinstance(item, (int, str, bool, dict, float)):
                                if no_repr:
                                    dct[k] = item
                                else:
                                    dct[reprsnt.names_map.get(k, k)] = item
                            else:
                                if no_repr:
                                    dct[k] = self.dump(item, obj)
                                else:
                                    dct[reprsnt.names_map.get(k, k)] = self.dump(item, obj)

            else:
                for k, v in obj.__dict__.items():
                    if not k.startswith("_") and k not in ignorecase:
                        if isinstance(v, (int, str, bool, dict, float)):
                            if no_repr:
                                dct[k] = v
                            else:
                                if reprsnt.names_map is not None:
                                    dct[reprsnt.names_map.get(k, k)] = v
                                else:
                                    dct[k] = v
                        elif isinstance(v, datetime.datetime):
                            if no_repr:
                                dct[k] = v.strftime(self.datetime_format)
                            else:
                                dct[k] = v.strftime(reprsnt.datetime_format)
                        else:
                            if no_repr:
                                dct[k] = self.dump(v, obj)
                            else:
                                if reprsnt.names_map is not None:
                                    dct[reprsnt.names_map.get(k, k)] = self.dump(v, obj)
                                else:
                                    dct[k] = self.dump(v, obj)
        if not no_repr:
            if reprsnt.extra is not None:
                for k, v in reprsnt.extra.items():
                    attr = dct[re.search("<(\w+)>", v).group(0)[1:-1]]
                    dct[k] = re.sub("<(\w+)>", f"{attr}", v)
            if reprsnt.look is not None:
                for name in reprsnt.look:
                    if len(list(filter(lambda x: x.name.startswith(f"look_{name}"),
                                       inspect.classify_class_attrs(reprsnt)))):
                        dct[name] = list(
                            filter(
                                lambda x: x.name.startswith(f"look_{name}"),
                                inspect.classify_class_attrs(reprsnt)
                            )
                        )[0].object(dct[name])
            if reprsnt.validate is not None:
                for name in reprsnt.validate:
                    try:
                        list(
                            filter(
                                lambda x: x.name.startswith(f"validate_{name}"),
                                inspect.classify_class_attrs(reprsnt)
                            )
                        )[0].object(dct[name])
                    except AssertionError as e:
                        if e.args:
                            dct[name] = e.args[0]
                        else:
                            dct[name] = f'"{name}" is not valid!'
        return dct

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
                        f"\nThis object with the nested data.\nAdd Repr for {cls} class!\n"
                        f"In Repr, `{k}` field must be added to `loads` dict")
            if hasattr(cls, '__tablename__'):
                return cls(**dct)
            return cls(*dct.values())
        else:
            new_dct = {}
            names_map = reprsnt.names_map or {}
            names_map = {v: k for k, v in names_map.items()}
            for k, v in dct.items():
                if isinstance(v, dict):
                    sub_cls = reprsnt.loads[names_map.get(k, k)]
                    new_dct[names_map.get(k, k)] = self.load(v, sub_cls)
                elif isinstance(v, list):
                    new_dct[names_map.get(k, k)] = [self.load(i, reprsnt.loads[k]) for i in v]
                elif reprsnt.loads.get(names_map.get(k, k)) is datetime.datetime:
                    new_dct[names_map.get(k, k)] = datetime.datetime.strptime(v, reprsnt.datetime_format)
                else:
                    new_dct[names_map.get(k, k)] = v
            if reprsnt.validate is not None:
                for name in reprsnt.validate:
                    try:
                        list(
                            filter(
                                lambda x: x.name.startswith(f"validate_{name}"),
                                inspect.classify_class_attrs(reprsnt)
                            )
                        )[0].object(new_dct[name])
                    except AssertionError as e:
                        if e.args:
                            raise DeserializationException(f"\nCan't deserialize `{name}` field\n{e.args[0]}") from None
                        raise DeserializationException(f"\nCan't deserialize `{name}` field!") from None
            if hasattr(cls, '__tablename__'):
                return cls(**new_dct)
            return cls(*new_dct.values())

    def dump_route(self, view_func):
        """
        Special decorator for dumping returned value of your Flask or FastAPI view-function
        Simple example:
        @app.route('/users/<int:user_id>')
        @kef.dump_route
        def user_view(user_id):
            return User.query.get(user_id)
        WARNING:
        `dump_route` must be between the `route` decorator and view function
        """

        @functools.wraps(view_func)
        def dump_response(*args, **kwargs):
            content = self.dump(view_func(*args, **kwargs))
            if self.used.lower() == 'flask':
                if FlaskResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install Flask!"
                    )
                response = FlaskResponse(json.dumps(content), mimetype="application/json")
                return response
            elif self.used.lower() == 'fastapi':
                if FastAPIResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install FastAPI!"
                    )
                response = FastAPIResponse(content)
                return response
            else:
                raise ValueError('`used` arg can be only "flask" or "fastapi" string')

        return dump_response


class Repr:
    ignore = ()
    extra = None
    look = ()
    names_map = None
    validate = ()
    loads = None
    datetime_format = '%d.%m.%Y'

class PleaseInstallException(Exception):
    ...

class NeedReprException(Exception):
    ...

class DeserializationException(Exception):
    ...
