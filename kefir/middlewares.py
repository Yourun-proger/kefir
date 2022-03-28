class ASGIDumpMiddleware:
    """
    ASGI Middleware for dump any raw response.
    Today only for fastapi because I haven't figured out how to do it for flask yet.
    And I'm not talking about the fact that I don't know how to
    make an asynchronous middleware for Flask (flask and ASGI, lol),
    I'm talking about the fact that I don't know how to write a WSGI middleware.
    I am looking for examples on the Internet, but they do not change the response itself,
    they only do metrics, logs, change headers, but not response..

    I don't know if it will work or not. use at your own risk)
    """

    def __init__(self, app, kef):
        self.app = app
        self.kef = kef

    async def __call__(self, scope, receive, send):
        # see here for info:
        # https://github.com/tiangolo/fastapi/issues/2696#issuecomment-768224643
        # some ASGI magic.
        # more here:
        # https://asgi.readthedocs.io/en/latest/specs/main.html
        await self.app(scope, receive, send)

    async def dispatch(self, request, call_next):
        content = await call_next(request)
        response = self.kef.dump(content)
        return response
