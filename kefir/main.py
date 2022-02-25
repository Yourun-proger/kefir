from kefir.kef_factory import KefirFactory


class Kefir:
    def __new__(
        self, represents=None, datetime_format="%d.%m.%Y", used="flask", mode="sync"
    ):
        return KefirFactory.makeKef(represents, datetime_format, used, mode)
