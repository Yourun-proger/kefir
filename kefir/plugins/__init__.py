from .flask_plugin import FlaskPlugin
from .fastapi_plugin import FastAPIPlugin


PLUGINS = {
    'flask': FlaskPlugin,
    'fastapi': FastAPIPlugin
}
