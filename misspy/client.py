import asyncio
import json

import httpx
import websockets
from attrdictionary import AttrDict

from .http import request
from .http import request_sync
from . import notes


class Bot:
    """
    Class used to connect and interact with the Misskey Streaming API.
    """

    def __init__(self, address, i=None) -> None:
        self.__address = address
        if not address.startswith("http://") and not address.startswith("https://"):
            self.address = "https://" + address
        self.ws = None
        self.__i = i
        self.bot = self.user()

    def user(self):
        res = httpx.post(f"{self.address}/api/i")
        return AttrDict(res.json())

    def meta(self, detail: bool = True):
        return AttrDict(
            request_sync(self.address, self.__i, "meta", {"detail": detail})
        )

    def run(self):
        asyncio.run(self.recv())

    async def announcements(
        self,
        limit: int = 10,
        withUnreads: bool = True,
        sinceId: str = None,
        untilId: str = None,
    ):
        async with httpx.AsyncClient() as client:
            data = {"i": self.__i, "limit": limit, "withUnreads": withUnreads}
            if sinceId is not None:
                data["sinceId"] = sinceId
            if untilId is not None:
                data["untilId"] = untilId

            res = await client.post(f"{self.address}/api/announcements", json=data)
            res = await res.json()

    async def recv(self):
        async with websockets.connect(
            f"wss://{self.__address}/streaming?i={self.__i}"
        ) as self.ws:
            try:
                await self.on_ready()
            except AttributeError:
                pass
            await self.ws.send(
                json.dumps(
                    {
                        "type": "connect",
                        "body": {"channel": "localTimeline", "id": "test"},
                    }
                )
            )
            while True:
                recv = json.loads(await self.ws.recv())
                if recv["type"] == "channel":
                    if recv["body"]["type"] == "note":
                        try:
                            try:
                                if recv["body"]["body"]["renote"] is None:
                                    recv["body"]["body"]["reply"] = self.notes_create(
                                        replyid=recv["body"]["body"]
                                    )
                                    await self.on_note(AttrDict(recv["body"]["body"]))
                                else:
                                    await self.on_renote(AttrDict(recv["body"]["body"]))
                            except KeyError:
                                recv["body"]["body"]["reply"] = self.notes_create
                                await self.on_note(AttrDict(recv["body"]["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "notification":
                        if recv["body"]["body"]["type"] == "reaction":
                            try:
                                await self.on_reacted(AttrDict(recv["body"]["body"]))
                            except AttributeError:
                                pass
                        elif recv["body"]["body"]["type"] == "reaction":
                            try:
                                await self.on_reacted(AttrDict(recv["body"]["body"]))
                            except AttributeError:
                                pass
                    elif recv["body"]["type"] == "follow":
                        try:
                            await self.on_following(AttrDict(recv["body"]["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "followed":
                        try:
                            await self.on_followed(AttrDict(recv["body"]["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "unfollow":
                        try:
                            await self.on_unfollowing(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "mention":
                        try:
                            await self.on_mention(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "reply":
                        try:
                            await self.on_reply(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "renote":
                        try:
                            await self.on_renote(AttrDict(recv["body"]))
                        except AttributeError:
                            pass

                if recv["type"] == "noteUpdated":
                    if recv["body"]["type"] == "reacted":
                        try:
                            await self.on_reacted(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "unreacted":
                        try:
                            await self.on_unreacted(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "pollVoted":
                        try:
                            await self.on_voted(AttrDict(recv["body"]))
                        except AttributeError:
                            pass
                    elif recv["body"]["type"] == "deleted":
                        try:
                            await self.on_note_delete(AttrDict(recv["body"]))
                        except AttributeError:
                            pass

    async def connect(self, channel):
        await self.ws.send(
            json.dumps(
                {
                    "type": 'connect',
                    "body": {
                        "channel": channel,
                        "id": channel,
                    }
                }
            )
        )

    async def unsubNote(self, noteId):
        await self.ws.send(
            json.dumps(
                {
                    "type": "unsubNote",
                    "body": {"id": noteId},
                }
            )
        )

    async def subNote(self, noteId):
        await self.ws.send(
            json.dumps(
                {
                    "type": "subNote",
                    "body": {"id": noteId},
                }
            )
        )

    async def notes_children(
        self,
        noteId: str,
        sinceId: str = None,
        untilId: str = None,
        limit: int = 10,
    ):
        return AttrDict(
            await notes.children(
                self.address,
                self.__i,
                noteId,
                limit,
                sinceId,
                untilId,
            )
        )

    async def notes(
        self,
        local: bool = False,
        reply: bool = None,
        renote: bool = None,
        withFiles: bool = None,
        poll: bool = None,
        limit: int = 10,
        sinceId: str = None,
        untilId: str = None,
    ):
        return AttrDict(
            await notes.note(
                self.address,
                self.__i,
                local,
                reply,
                renote,
                withFiles,
                poll,
                limit,
                sinceId,
                untilId,
            )
        )

    async def notes_create(
        self,
        text,
        visibility="public",
        visibleUserIds: list = None,
        replyid=None,
        fileid=None,
        channelId=None,
        localOnly=False,
        renoteId=None,
    ):
        """Create notes. Reply and Renote are also done with this function. However, the actual processing is done in another function.

        Args:
            text (str): note content
            visibility (str): Public scope of the note. Defaults to "public".
            visibleUserIds (list, optional): ID of the user as seen for direct notes. Defaults to None.
            replyid (_type_, optional): the id of the note to reply to. Defaults to None.
            fileid (_type_, optional): notes attached file id. Defaults to None.
            channelId (_type_, optional): The id of the channel to post to. Defaults to None.
            localOnly (bool, optional): If true, posts to local timeline only.. Defaults to False.
            renoteId (_type_, optional): the id of the note to renote to.. Defaults to None.

        Returns:
            AttrDict: You can get the contents in a format like a.b.
        """

        return AttrDict(
            await notes.create(
                self.address,
                self.__i,
                text,
                visibility,
                visibleUserIds,
                replyid,
                fileid,
                channelId,
                localOnly,
                renoteId,
            )
        )

    async def pages_create(
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
        hideTitleWhenPinned=None
    ):
        base = {
            "title": title,
            "name": name,
            "content": content,
            "variables": variables,
            "script": script
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
        return AttrDict(
            await request(
                self.address, self.__i, "pages/create", base
            )
        )

    async def pages_delete(
        self,
        pageId
    ):
        base = {
            "pageId": pageId
        }
        return AttrDict(
            await request(
                self.address, self.__i, "pages/delete", base
            )
        )     
    
    async def pages_show(
        self,
        pageId,
        name,
        username
    ):
        base = {
            "pageId": pageId,
            "name": name,
            "username": username
        }
        return AttrDict(
            await request(
                self.address, self.__i, "pages/show", base
            )
        )      

    async def drive_files_delete(
        self,
        fileId: str
    ):
        base = {"fileId": fileId}
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/delete", base
            )
        )

    async def drive_files_create(
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
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/create", base, files={"file": file}
            )
        )

    async def inf(self):
        url = f"{self.address}/api/i"
        params = {
            "i": self.__i,
        }
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=params, headers=head)
            return AttrDict(r.json())

    async def block(self, userId: str):
        url = f"{self.address}/api/blocking/create"
        params = {"i": self.__i, "userId": userId}
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=params, headers=head)
            return AttrDict(r.json())

    async def unblock(self, userId: str):
        url = f"{self.address}/api/blocking/delete"
        params = {"i": self.__i, "userId": userId}
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=params, headers=head)
            return AttrDict(r.json())

    async def blocking(self, limit: int = 30, sinceId: str = None, untilId: str = None):
        url = f"{self.address}/api/blocking/list"
        params = {
            "i": self.__i,
            "limit": limit,
        }
        if not sinceId is None:
            params["sinceId"] = sinceId
        if not untilId is None:
            params["untilId"] = untilId
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=params, headers=head)
            return AttrDict(r.json())

    async def ping(self):
        """
        pong
        """
        url = f"{self.address}/api/ping"
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, headers=head)
            return AttrDict(r.json())
