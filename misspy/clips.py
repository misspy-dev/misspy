
from attrdictionary import AttrDict

from .core.http import request

class clips:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def create(self, name, isPublic=False, description=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "clips/create",
                {"name": name, "isPublic": isPublic, "description": description},
            )
        )

    async def update(self, clipId, name, isPublic=False, description=None):
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

    async def delete(self, clipId):
        return AttrDict(
            await request(self.address, self.__i, "clips/delete", {"clipId": clipId})
        )

    async def list(self):
        return AttrDict(await request(self.address, self.__i, "clips/list", {}))

    async def show(self, clipId):
        return AttrDict(
            await request(self.address, self.__i, "clips/show", {"clipId": clipId})
        )