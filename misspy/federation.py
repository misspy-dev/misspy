from attrdictionary import AttrDict

from .util import nonecheck
from .http import request

class federation:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def followers(self, host, limit=10, sinceId=None, untilId=None):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "federation/followers", base)
        )

    async def following(self, host, limit=10, sinceId=None, untilId=None):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "federation/following", base)
        )

    async def instances(
        self,
        host=None,
        blocked=None,
        notResponding=None,
        suspended=None,
        fedrating=None,
        subscribing=None,
        publishing=None,
        limit=30,
        offset=0,
        sort=None,
    ):
        base = {
            "host": host,
            "blocked": blocked,
            "notResponding": notResponding,
            "suspended": suspended,
            "fedrating": fedrating,
            "subscribing": subscribing,
            "publishing": publishing,
            "limit": limit,
            "offset": offset,
        }
        if nonecheck(sort):
            base["sort"] = sort
        return AttrDict(
            await request(self.address, self.__i, "federation/instances", base)
        )

    async def show_instance(self, host):
        return AttrDict(
            await request(
                self.address, self.__i, "federation/show-instance", {"host": host}
            )
        )

    async def stats(self, limit=10):
        return AttrDict(
            await request(self.address, self.__i, "federation/stats", {"limit": limit})
        )

    async def update_remote_user(self, userId):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "federation/update-remote-user",
                {"userId": userId},
            )
        )

    async def users(self, host, sinceId=None, untilId=None, limit=10):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "federation/users", base))
