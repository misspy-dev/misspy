from attrdictionary import AttrDict

from .http import request, request_sync

class MiWeb:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    def request_reset_password(instance, username, email):
        return request_sync(
            instance, None, "request-reset-password", {"username": username, "email": email}
        )


    def reset_password(instance, i, password):
        return request_sync(
            instance, None, "request-reset-password", {"token": i, "password": password}
        )

    async def email_address_available(self, emailAddress):
        return AttrDict(
            request(
                self.address,
                self.__i,
                "email-address/available",
                {"emailAddress": emailAddress},
            )
        )

    async def username_available(self, username):
        return AttrDict(
            request(
                self.address, self.__i, "username/available", {"username": username}
            )
        )