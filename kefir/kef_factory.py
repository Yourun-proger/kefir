from kefir.kefs import SyncKefir


class KefirFactory:
    @staticmethod
    def makeKef(
        *args,
    ):
        mode = args[-1]
        if mode.lower() == "sync":
            return SyncKefir(*args[:-1])
        elif mode.lower() == "async":
            raise NotImplementedError(
                "Today Kefir can't be asynchronous!\n"
                "See this for more info:\n"
                "https://github.com/Yourun-proger/kefir/wiki/Docs#async-support"
            )
        else:
            raise ValueError('"mode" argumnet must be "sync" or "async" string!!11')
