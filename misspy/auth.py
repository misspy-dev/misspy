import hashlib

from .core.http import request
from attrdictionary import AttrDict


class app:
    def __init__(self, address) -> None:
        if not address.startswith("http://") and not address.startswith("https://"):
            self._address: str = "https://" + address
        else:
            self._address: str = address

    async def create(
        self,
        name: str,
        description: str,
        permission: list = [
            "read:account",
            "write:account",
            "read:blocks",
            "write:blocks",
            "read:drive",
            "write:drive",
            "read:favorites",
            "write:favorites",
            "read:following",
            "write:following",
            "read:messaging",
            "write:messaging",
            "read:mutes",
            "write:mutes",
            "write:notes",
            "read:notifications",
            "write:notifications",
            "write:reactions",
            "write:votes",
            "read:pages",
            "write:pages",
            "write:page-likes",
            "read:page-likes",
            "write:gallery-likes",
            "read:gallery-likes",
        ],
        callbackUrl: str = None,
    ):
        res = await request(
            self._address, None, endpoint="app/create",
            jobj={
                    "name": name,
                    "description": description,
                    "permission": permission,
                    "callbackUrl": callbackUrl,
                }
        )
        return AttrDict(res)

    async def generate(self, appSecret):
        res = await request(
            self._address, None, endpoint="auth/session/generate",
            jobj={
                "appSecret": appSecret,
            }
        )
        return AttrDict(res)

    async def get_token(self, appSecret, token):
        res = await request(
            self._address, None, endpoint="auth/session/userkey",
            jobj={"appSecret": appSecret, "token": token}
        )
        return hashlib.sha256(
            (res["accessToken"] + appSecret).encode("utf-8")
        ).hexdigest()
