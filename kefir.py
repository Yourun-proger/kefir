"""
Kefir main file
"""

import re
import functools
import json
import inspect


try:
    from flask import Response
except ImportError:
    Response = None


class Kefir:
    def __init__(self, represents={}):
        self.represents = represents

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
                    if no_repr:
                        dct[k] = getattr(obj, k)
                    else:
                        dct[reprsnt.names_map.get(k, k)] = getattr(obj, k)
                else:
                    if no_repr:
                        dct[k] = self.dump(getattr(obj, k), obj)
                    else:
                        dct[reprsnt.names_map.get(k, k)] = self.dump(getattr(obj, k), obj)
        else:
            if obj.__dict__.get("_sa_instance_state"):
                for k, v in (
                    obj.__dict__["_sa_instance_state"]
                    .__dict__["manager"]
                    .__dict__["local_attrs"]
                    .items()
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
                                dct[reprsnt.names_map.get(k, k)] = v
                        else:
                            if no_repr:
                                dct[k] = self.dump(v, obj)
                            else:
                                dct[reprsnt.names_map.get(k, k)] = self.dump(v, obj)
        if not no_repr:
            if reprsnt.extra is not None:
                for k, v in reprsnt.extra.items():
                    attr = dct[re.search("<(\w+)>", v).group(0)[1:-1]]
                    dct[k] = re.sub("<(\w+)>", f"{attr}", v)
            if reprsnt.look is not None:
                for name in reprsnt.look:
                    if len(list(filter(lambda x: x.name.startswith(f"look_{name}"),inspect.classify_class_attrs(reprsnt)))):
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

    def dump_route(self, view_func):
        """
        Special decorator for dumping returned value of your Flask view-function
        ONLY FOR FLASK!
        Simple example:
        @app.route('/users/<int:user_id>')
        @kef.dump_route
        def user_view(user_id):
            return User.query.get(user_id)
        WARNING:
        `dump_route` must be enter the `route` decorator and view function
        """

        @functools.wraps(view_func)
        def dump_response(*args, **kwargs):
            content = self.dump(view_func(*args, **kwargs))
            if Response is None:
                raise PleaseInstallException(
                    "If you want to use `dump_route`, please install Flask!"
                )
            response = Response(json.dumps(content), mimetype="application/json")
            return response

        return dump_response


class Repr:
    ignore = ()
    extra = None
    look = None
    names_map = None
    validate = None


class PleaseInstallException(Exception):
    ...
