class BasePlugin:
    IS_ASYNC = False

    @staticmethod
    def make_response(content):
        raise NotImplementedError
