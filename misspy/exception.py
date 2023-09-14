class MisskeyException(Exception):
    """Base exception class for misspy.core

    Ideally, this should be caught and the exception handled.
    """

    pass


class WebsocketClosed(MisskeyException):
    """websocket connection closed error class for misspy.core

    Ideally, this should be caught and the exception handled.
    """

    pass


class ClientException(MisskeyException):
    """Parent class of error classes such as login failure."""


class AuthenticationFailed(ClientException):
    """Class called if MisskeyAPI authentication fails."""


class MiAuthFailed(AuthenticationFailed):
    """Class called if MiAuth fails."""


class HTTPException(MisskeyException):
    """Error class called when a request to the misskey server's API fails.

    Called when httpx.HTTPError is caught.
    """
