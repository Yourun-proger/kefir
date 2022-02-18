from kefir.kefs import SyncKefir, AsyncKefir

class KefirFactory:

    @staticmethod
    def makeKef(represents=None, datetime_format='%d.%m.%Y', used='flask', mod='sync'):
        if mod.lower() == 'sync':
            return SyncKefir(represents, datetime_format, used)
        elif mod.lower() == 'async':
            raise NotImplementedError(
                                      """Today Kefir can't be asynchronous!
                                      See this for more info:
                                      https://github.com/Yourun-proger/kefir/wiki/Docs#async-support
                                      """)
        else:
            raise ValueError('"mod" argumnet must be "sync" or "async" string!!1')
