from attrdictionary import AttrDict

from .util import nonecheck
from .core.http import request

class channels:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def create(self, name, description=None, bannerId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "channels/create",
                {"name": name, "description": description, "bannerId": bannerId},
            )
        )

    async def list(self):
        return AttrDict(await request(self.address, self.__i, "channels/list", {}))

    async def update(self, channelId, name, description=None, bannerId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "channels/update",
                {
                    "channelId": channelId,
                    "name": name,
                    "description": description,
                    "bannerId": bannerId,
                },
            )
        )

    async def follow(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/follow", {"channelId": channelId}
            )
        )

    async def unfollow(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/unfollow", {"channelId": channelId}
            )
        )

    async def show(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/show", {"channelId": channelId}
            )
        )

    async def followed(self, limit=5, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "channels/followed", base)
        )

    async def owned(self, limit=5, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "channels/owned", base))

    async def featured(self):
        return AttrDict(await request(self.address, self.__i, "channels/featured", {}))
