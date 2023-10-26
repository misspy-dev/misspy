class MisskeyException(Exception):
    """Base exception class for misspy

    Ideally, this should be caught and the exception handled.
    """

    pass


class WebsocketError(MisskeyException):
    """websocket connection error class for misspy

    Ideally, this should be caught and the exception handled.
    """

    pass


class ClientException(MisskeyException):
    """Parent class of error classes such as login failure."""

class RateLimitError(ClientException):
    """RateLimitError trigger: RATE_LIMIT_EXCEEDED"""

class AuthenticationFailed(ClientException):
    """Class called if MisskeyAPI authentication fails."""


class MiAuthFailed(AuthenticationFailed):
    """Class called if MiAuth fails."""


class HTTPException(MisskeyException):
    """Error class called when a request to the misskey server's API fails.

    Called when httpx.HTTPError is caught.
    """
