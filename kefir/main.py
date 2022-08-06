from kefir.kef_factory import KefirFactory


class Kefir:
    def __new__(
        self,
        represents=None,
        plugin="flask",
        datetime_format="%d.%m.%Y",
    ):
        return KefirFactory.build_kef(
            represents=represents,
            plugin=plugin,
            datetime_format=datetime_format,
        )
