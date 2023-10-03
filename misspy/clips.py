
from attrdictionary import AttrDict

from .http import request

class server:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def clips_create(self, name, isPublic=False, description=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "clips/create",
                {"name": name, "isPublic": isPublic, "description": description},
            )
        )

    async def clips_update(self, clipId, name, isPublic=False, description=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "clips/update",
                {
                    "clipId": clipId,
                    "name": name,
                    "isPublic": isPublic,
                    "description": description,
                },
            )
        )

    async def clips_delete(self, clipId):
        return AttrDict(
            await request(self.address, self.__i, "clips/delete", {"clipId": clipId})
        )

    async def clips_list(self):
        return AttrDict(await request(self.address, self.__i, "clips/list", {}))

    async def clips_show(self, clipId):
        return AttrDict(
            await request(self.address, self.__i, "clips/show", {"clipId": clipId})
        )