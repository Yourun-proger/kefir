from kefir.base import BaseKefir
from kefir.plugins import PLUGINS
from kefir.plugins.base import BasePlugin


class KefirFactory:
    @staticmethod
    def build_kef(represents=None, plugin='flask', datetime_format='%d.%m.%Y'):
        if represents is None:
            represents = {}

        if not isinstance(plugin, BasePlugin):
            plugin = PLUGINS[plugin]

        return BaseKefir(
            represents=represents,
            plugin=plugin,
            datetime_format=datetime_format
        )
