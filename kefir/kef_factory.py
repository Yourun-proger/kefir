from kefir.base import BaseKefir
from kefir.plugins import PLUGINS
from kefir.plugins.base import BasePlugin


class KefirFactory:
    @staticmethod
    def build_kef(represents=None, plugin="flask", datetime_format="%d.%m.%Y"):
        if represents is None:
            represents = {}

        if isinstance(plugin, str):
            try:
                plugin = PLUGINS[plugin]
            except KeyError:
                raise ValueError(
                    f"Plugin name must be one of: {PLUGINS}"
                ) from None
        elif not isinstance(plugin, BasePlugin):
            raise ValueError(
                f"Plugin argumnet must be string from {PLUGINS} or a"
                "subclass of the BasePlugin class"
            )

        return BaseKefir(
            represents=represents,
            plugin=plugin,
            datetime_format=datetime_format,
        )
