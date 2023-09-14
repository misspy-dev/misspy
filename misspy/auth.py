import hashlib

import httpx
from attrdictionary import AttrDict


class app:
    def __init__(self, address) -> None:
        if not address.startswith("http://") and not address.startswith("https://"):
            self._address: str = "https://" + address + "/api/"
        else:
            self._address: str = address + "/api/"

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
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self._address + "app/create",
                json={
                    "name": name,
                    "description": description,
                    "permission": permission,
                    "callbackUrl": callbackUrl,
                },
            )
            res = await res.json()
            return AttrDict(res)

    async def generate(self, appSecret):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self._address + "auth/session/generate",
                json={
                    "appSecret": appSecret,
                },
            )
            res = await res.json()
            return AttrDict(res)

    async def get_token(self, appSecret, token):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self._address + "auth/session/userkey",
                json={"appSecret": appSecret, "token": token},
            )
            res = await res.json()
            return hashlib.sha256(
                (res["accessToken"] + appSecret).encode("utf-8")
            ).hexdigest()
