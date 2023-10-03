from attrdictionary import AttrDict

from .http import request, request_sync

class server:
    
    def __init__(self, address, i) -> None:
        self.i = i
        self.address = address

    def user(self):
        return AttrDict(request_sync(self.address, self.__i, "i", {}, ssl=self.ssl))

    def meta(self, detail: bool = True):
        return AttrDict(
            request_sync(self.address, self.__i, "meta", {"detail": detail})
        )
        
    async def announcements(
        self,
        limit: int = 10,
        withUnreads: bool = True,
        sinceId: str = None,
        untilId: str = None,
    ):
        data = {"limit": limit, "withUnreads": withUnreads}
        if sinceId is not None:
            data["sinceId"] = sinceId
        if untilId is not None:
            data["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "announcements", data))
        