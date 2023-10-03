from attrdictionary import AttrDict

from .http import request

class hashtags:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def list(
        self,
        sort,
        limit=10,
        attachedToUserOnly=False,
        attachedToLocalUserOnly=False,
        attachedToRemoteUserOnly=False,
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/list",
                {
                    "sort": sort,
                    "limit": limit,
                    "attachedToUserOnly": attachedToUserOnly,
                    "attachedToLocalUserOnly": attachedToLocalUserOnly,
                    "attachedToRemoteUserOnly": attachedToRemoteUserOnly,
                },
            )
        )

    async def search(self, query, limit=10, offset=0):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/search",
                {"query": query, "limit": limit, "offset": offset},
            )
        )

    async def search(self, tag):
        return AttrDict(
            await request(self.address, self.__i, "hashtags/show", {"tag": tag})
        )

    async def trend(self):
        return AttrDict(await request(self.address, self.__i, "hashtags/trend", {}))

    async def users(self, tag, sort, limit=10, state="all", origin="local"):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/users",
                {
                    "tag": tag,
                    "sort": sort,
                    "limit": limit,
                    "state": state,
                    "origin": origin,
                },
            )
        )