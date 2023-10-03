
from attrdictionary import AttrDict

from .util import nonecheck
from .http import request

class pages:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def create(
        self,
        title,
        name,
        content,
        variables,
        script,
        summary=None,
        eyeCatchingImageId=None,
        font=None,
        alignCenter=None,
        hideTitleWhenPinned=None,
    ):
        base = {
            "title": title,
            "name": name,
            "content": content,
            "variables": variables,
            "script": script,
        }
        if summary is not None:
            base["summary"] = summary
        if eyeCatchingImageId is not None:
            base["eyeCatchingImageId"] = eyeCatchingImageId
        if font is not None:
            base["font"] = font
        if alignCenter is not None:
            base["alignCenter"] = alignCenter
        if hideTitleWhenPinned is not None:
            base["hideTitleWhenPinned"] = hideTitleWhenPinned
        return AttrDict(await request(self.address, self.__i, "pages/create", base))

    async def delete(self, pageId):
        base = {"pageId": pageId}
        return AttrDict(await request(self.address, self.__i, "pages/delete", base))

    async def show(self, pageId, name, username):
        base = {"pageId": pageId, "name": name, "username": username}
        return AttrDict(await request(self.address, self.__i, "pages/show", base))
