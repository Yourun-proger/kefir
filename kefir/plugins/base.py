class BasePlugin:
    NAME = None
    RESPONSE_CLASS = None
    ADDITIONAL_KWARGS = {}
    IS_ASYNC = False

    @classmethod
    def make_response(cls, data):
        if cls.RESPONSE_CLASS is None:
            raise ModuleNotFoundError(f'No module named {cls.NAME}')
        content = cls.make_content(data)
        return cls.RESPONSE_CLASS(content, **cls.ADDITIONAL_KWARGS)

    @classmethod
    def make_content(cls, data):
        raise NotImplementedError
