from attrdictionary import AttrDict

from ...http import request, request_sync
from ...util import nonecheck


class ad:
    def __init__(self, client) -> None:
        self.address = client.__address
        self.i = client.__address

    async def create(self, url, memo, place, priority, ratio, expiresAt, imageUrl):
        base = {
            "url": url,
            "memo": memo,
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "expiresAt": expiresAt,
            "imageUrl": imageUrl,
        }
        return AttrDict(await request(self.address, self.i, "admin/ad/create", base))

    async def delete(self, Id):
        return AttrDict(
            await request(self.address, self.i, "admin/ad/delete", {"id": Id})
        )

    async def update(self, Id, url, memo, place, priority, ratio, expiresAt, imageUrl):
        base = {
            "id": Id,
            "url": url,
            "memo": memo,
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "expiresAt": expiresAt,
            "imageUrl": imageUrl,
        }
        return AttrDict(await request(self.address, self.i, "admin/ad/update", base))

    async def list(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "admin/ad/list", base))

    async def suspend_user(self, userId):
        return AttrDict(
            await request(
                self.address, self.i, "admin/suspend-user", {"userId": userId}
            )
        )

    async def silence_user(self, userId):
        return AttrDict(
            await request(
                self.address, self.i, "admin/silence-user", {"userId": userId}
            )
        )

    async def unsuspend_user(self, userId):
        return AttrDict(
            await request(
                self.address, self.i, "admin/unsuspend-user", {"userId": userId}
            )
        )

    async def unsilence_user(self, userId):
        return AttrDict(
            await request(
                self.address, self.i, "admin/unsilence-user", {"userId": userId}
            )
        )
