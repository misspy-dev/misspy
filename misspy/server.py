from attrdictionary import AttrDict

from .core.http import request, request_sync


class server:
    def __init__(self, address, i, ssl=True) -> None:
        self.ssl = False
        if ssl:
            self.ssl = True

        if not address.startswith("http://") and not address.startswith("https://"):
            self.address = "http://" + address
            if ssl:
                self.address = "https://" + address
            self.address_raw = address
        else:
            self.address = address
            self.address_raw = address.replace("https://", "").replace("http://", "")
        self.i = i

    def user(self):
        resp = request_sync(self.address, self.i, "i", {}, ssl=self.ssl)
        return AttrDict(resp)

    def meta(self, detail: bool = True):
        return AttrDict(request_sync(self.address, self.i, "meta", {"detail": detail}))

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
        return AttrDict(await request(self.address, self.i, "announcements", data))
