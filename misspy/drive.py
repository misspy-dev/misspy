from attrdictionary import AttrDict

from .util import nonecheck
from .http import request, request_sync

class drive:

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl
        
    def drive(self):
        return AttrDict(request_sync(self.address, self.__i, "drive", {}))

    async def stream(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/stream", base))

    async def folders(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/folders", base))

    async def files(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/files", base))

    async def files_attached_notes(self, fileId):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/attached-notes", {"fileId": fileId}
            )
        )

    async def files_check_existence(self, md5):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/check-existence", {"md5": md5}
            )
        )

    async def files_find_by_hash(self, md5):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/find-by-hash", {"md5": md5}
            )
        )

    async def files_find(self, name, foldorId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/files/find",
                {"name": name, "foldorId": foldorId},
            )
        )

    async def folders_find(self, name, parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/find",
                {"name": name, "parentId": parentId},
            )
        )

    async def files_show(self):
        return AttrDict(await request(self.address, self.__i, "drive/files/show", {}))

    async def folders_show(self, folderId):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/folders/show", {"folderId": folderId}
            )
        )

    async def folders_update(self, folderId, name, parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/update",
                {"folderId": folderId, "name": name, "parentId": parentId},
            )
        )

    async def folders_create(self, name="Untitled", parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/create",
                {"name": name, "parentId": parentId},
            )
        )

    async def files_delete(self, folderId: str):
        base = {"folderId": folderId}
        return AttrDict(
            await request(self.address, self.__i, "drive/folders/delete", base)
        )

    async def files_delete(self, fileId: str):
        base = {"fileId": fileId}
        return AttrDict(
            await request(self.address, self.__i, "drive/files/delete", base)
        )

    async def files_create(
        self,
        file,
        folderId: str = None,
        name: str = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        base = {}
        if not is_sensitive == False:
            base["is_sensitive"] = is_sensitive
        if not is_sensitive == False:
            base["force"] = force
        if folderId is not None:
            base["folderId"] = folderId
        if name is not None:
            base["name"] = name
        AttrDict()
        return await request(
            self.address, self.__i, "drive/files/create", base, files={"file": file}
        )

    async def files_upload_from_url(
        self,
        url,
        folderId: str = None,
        name: str = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        base = {"url": url}
        if not is_sensitive == False:
            base["is_sensitive"] = is_sensitive
        if not is_sensitive == False:
            base["force"] = force
        if folderId is not None:
            base["folderId"] = folderId
        if name is not None:
            base["name"] = name
        return AttrDict(
            await request(self.address, self.__i, "drive/files/upload-from-url", base)
        )

    async def files_update(
        self,
        fileId,
        folderId: str = None,
        name: str = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        base = {"fileId": fileId}
        if not is_sensitive == False:
            base["is_sensitive"] = is_sensitive
        if not is_sensitive == False:
            base["force"] = force
        if folderId is not None:
            base["folderId"] = folderId
        if name is not None:
            base["name"] = name
        return AttrDict(
            await request(self.address, self.__i, "drive/files/update", base)
        )