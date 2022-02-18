from kefir.kef_factory import KefirFactory

class Kefir:
    def __new__(self, represents=None, datetime_format='%d.%m.%Y', used='flask', mod='sync'):
        return KefirFactory.makeKef(represents, datetime_format, mod)
