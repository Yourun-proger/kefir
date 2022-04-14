from kefir.kefs import SyncKefir, AsyncKefir


class KefirFactory:
    @staticmethod
    def makeKef(
        *args,
    ):
        mode = args[-1]
        if mode.lower() == "sync":
            return SyncKefir(*args[:-1])
        elif mode.lower() == "async":
            print(
                """Just tell you that mode='async' this is all about view-functions
                    that kefir can decorate with @dump_route
                    Now this class has no async methods!
                    More here: https://github.com/Yourun-proger/kefir/wiki/Docs#async-support"""
            )
            return AsyncKefir(*args[:-1])
        else:
            raise ValueError('"mode" argumnet must be "sync" or "async" string!!11')
