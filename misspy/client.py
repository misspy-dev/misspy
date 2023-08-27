import asyncio
import json

import httpx
import websockets
from attrdictionary import AttrDict

from .http import request
from .http import request_sync
from .util import nonecheck
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
                                    await self.on_note(AttrDict(recv["body"]["body"]))
                                else:
                                    await self.on_renote(AttrDict(recv["body"]["body"]))
                            except KeyError:
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
                            await self.on_reply(AttrDict())
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
                    "type": "connect",
                    "body": {
                        "channel": channel,
                        "id": channel,
                    },
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

    async def reactions_create(self, noteId, reaction):
        """create reaction.

        Args:
            noteId (string): noteId
            reaction (string): Specify reaction. Reactions are Unicode emojis or custom emojis. For custom emoji, enclose the emoji name with a colon.

        Returns:
            dict: Misskey API response
        """
        return await request(
            self.address,
            self.__i,
            "notes/reactions/create",
            {"noteId": noteId, "reaction": reaction},
            header={"Content-Type": "application/json"},
        )

    async def reactions_delete(self, noteId):
        """delete reaction.

        Args:
            noteId (string): noteId

        Returns:
            dict: Misskey API response
        """
        return await request(
            self.address,
            self.__i,
            "notes/reactions/delete",
            {"noteId": noteId},
            header={"Content-Type": "application/json"},
        )

    async def favorites(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "i/favorites", base))

    async def gallery_likes(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "i/gallery/likes", base))

    async def gallery_posts(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "i/gallery/posts", base))

    async def gallery_posts(
        self,
    ):
        return AttrDict(
            await request(self.address, self.__i, "i/get-word-muted-notes-count", {})
        )

    async def notifications(
        self,
        limit=10,
        sinceId=None,
        untilId=None,
        following=False,
        unreadOnly=False,
        markAsRead=True,
        includeTypes=None,
        excludeTypes=None,
    ):
        base = {
            "limit": limit,
            "following": following,
            "unreadOnly": unreadOnly,
            "markAsRead": markAsRead,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(includeTypes):
            base["includeTypes"] = includeTypes
        if nonecheck(excludeTypes):
            base["excludeTypes"] = excludeTypes
        return AttrDict(await request(self.address, self.__i, "i/notifications", base))

    async def page_likes(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "i/page-likes", base))

    async def pages(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "i/pages", base))

    async def fedration_followers(self, host, limit=10, sinceId=None, untilId=None):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "federation/followers", base)
        )

    async def fedration_following(self, host, limit=10, sinceId=None, untilId=None):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "federation/following", base)
        )

    async def federation_instances(
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

    async def federation_show_instance(self, host):
        return AttrDict(
            await request(
                self.address, self.__i, "federation/show-instance", {"host": host}
            )
        )

    async def federation_stats(self, limit=10):
        return AttrDict(
            await request(self.address, self.__i, "federation/stats", {"limit": limit})
        )

    async def federation_update_remote_user(self, userId):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "federation/update-remote-user",
                {"userId": userId},
            )
        )

    async def federation_users(self, host, sinceId=None, untilId=None, limit=10):
        base = {"host": host, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "federation/users", base))

    async def antennas_create(
        self,
        name,
        src,
        keywords,
        excludeKeywords,
        users,
        caseSensitive,
        withReplies,
        withFile,
        notify,
        userListId=None,
    ):
        base = {
            "name": name,
            "src": src,
            "keywords": keywords,
            "excludeKeywords": excludeKeywords,
            "users": users,
            "caseSensitive": caseSensitive,
            "withReplies": withReplies,
            "withFile": withFile,
            "notify": notify,
        }
        if nonecheck(userListId):
            base["userListId"] = userListId
        return AttrDict(request(self.address, self.__i, "antennas/create", base))

    async def antennas_update(
        self,
        name,
        src,
        keywords,
        excludeKeywords,
        users,
        caseSensitive,
        withReplies,
        withFile,
        notify,
        userListId=None,
    ):
        base = {
            "name": name,
            "src": src,
            "keywords": keywords,
            "excludeKeywords": excludeKeywords,
            "users": users,
            "caseSensitive": caseSensitive,
            "withReplies": withReplies,
            "withFile": withFile,
            "notify": notify,
        }
        if nonecheck(userListId):
            base["userListId"] = userListId
        return AttrDict(request(self.address, self.__i, "antennas/update", base))

    async def antennas_delete(self, antennaId):
        return AttrDict(
            request(self.address, self.__i, "antennas/delete", {"antennaId": antennaId})
        )

    async def antennas_show(self, antennaId):
        return AttrDict(
            request(self.address, self.__i, "antennas/show", {"antennaId": antennaId})
        )

    async def antennas_list(self):
        return AttrDict(request(self.address, self.__i, "antennas/list", {}))

    async def antennas_notes(
        self,
        antennaId,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
    ):
        base = {"antennaId": antennaId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return AttrDict(await request(self.address, self.__i, "federation/users", base))

    async def mute_create(self, userId, expiresAt=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "mute/create",
                {"userId": userId, "expiresAt": expiresAt},
            )
        )

    async def mute_create(self, limit=30, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "mute/list", base))

    async def mute_delete(self, userId):
        return AttrDict(
            await request(self.address, self.__i, "mute/delete", {"userId": userId})
        )

    async def channels_create(self, name, description=None, bannerId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "channels/create",
                {"name": name, "description": description, "bannerId": bannerId},
            )
        )

    async def channels_list(self):
        return AttrDict(await request(self.address, self.__i, "channels/list", {}))

    async def channels_update(self, channelId, name, description=None, bannerId=None):
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

    async def channels_follow(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/follow", {"channelId": channelId}
            )
        )

    async def channels_unfollow(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/unfollow", {"channelId": channelId}
            )
        )

    async def channels_show(self, channelId):
        return AttrDict(
            await request(
                self.address, self.__i, "channels/show", {"channelId": channelId}
            )
        )

    async def channels_followed(self, limit=5, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "channels/followed", base)
        )

    async def channels_owned(self, limit=5, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "channels/owned", base))

    async def channels_featured(self):
        return AttrDict(await request(self.address, self.__i, "channels/featured", {}))

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

    async def notes_clips(self, noteId):
        return AttrDict(
            await request(self.address, self.__i, "notes/clips", {"noteId": noteId})
        )

    async def pin(self, noteId):
        return AttrDict(
            await request(self.address, self.__i, "i/pin", {"noteId": noteId})
        )

    async def unpin(self, noteId):
        return AttrDict(
            await request(self.address, self.__i, "i/unpin", {"noteId": noteId})
        )

    async def update(self, params):
        return AttrDict(await request(self.address, self.__i, "i/update", params))

    async def read_all_messaging_messages(self):
        return AttrDict(
            await request(self.address, self.__i, "i/read-all-messaging-messages", {})
        )

    async def read_all_unread_notes(self):
        return AttrDict(
            await request(self.address, self.__i, "i/read-all-unread-notes", {})
        )

    async def read_announcement(self, announcementId):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "i/read-all-unread-notes",
                {"announcementId": announcementId},
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

    async def pages_delete(self, pageId):
        base = {"pageId": pageId}
        return AttrDict(await request(self.address, self.__i, "pages/delete", base))

    async def pages_show(self, pageId, name, username):
        base = {"pageId": pageId, "name": name, "username": username}
        return AttrDict(await request(self.address, self.__i, "pages/show", base))

    async def drive(self):
        return AttrDict(await request(self.address, self.__i, "drive", {}))

    async def drive_stream(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/stream", base))

    async def drive_folders(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/folders", base))

    async def drive_files(
        self, limit=10, sinceId=None, untilId=None, folderId=None, type=None
    ):
        base = {"limit": limit, "folderId": folderId, "type": type}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "drive/files", base))

    async def drive_files_attached_notes(self, fileId):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/attached-notes", {"fileId": fileId}
            )
        )

    async def drive_files_check_existence(self, md5):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/check-existence", {"md5": md5}
            )
        )

    async def drive_files_find_by_hash(self, md5):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/files/find-by-hash", {"md5": md5}
            )
        )

    async def drive_files_find(self, name, foldorId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/files/find",
                {"name": name, "foldorId": foldorId},
            )
        )

    async def drive_folders_find(self, name, parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/find",
                {"name": name, "parentId": parentId},
            )
        )

    async def drive_files_show(self):
        return AttrDict(await request(self.address, self.__i, "drive/files/show", {}))

    async def drive_folders_show(self, folderId):
        return AttrDict(
            await request(
                self.address, self.__i, "drive/folders/show", {"folderId": folderId}
            )
        )

    async def drive_folders_update(self, folderId, name, parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/update",
                {"folderId": folderId, "name": name, "parentId": parentId},
            )
        )

    async def drive_folders_create(self, name="Untitled", parentId=None):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "drive/folders/create",
                {"name": name, "parentId": parentId},
            )
        )

    async def drive_files_delete(self, folderId: str):
        base = {"folderId": folderId}
        return AttrDict(
            await request(self.address, self.__i, "drive/folders/delete", base)
        )

    async def drive_files_delete(self, fileId: str):
        base = {"fileId": fileId}
        return AttrDict(
            await request(self.address, self.__i, "drive/files/delete", base)
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

    async def drive_files_upload_from_url(
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

    async def drive_files_update(
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

    async def i(self):
        r = await request(self.address, self.__i, "i", {})
        return AttrDict(r)

    async def blocking_create(self, userId: str):
        params = {"userId": userId}
        r = await request(self.address, self.__i, "blocking/create", params)
        return AttrDict(r)

    async def blocking_delete(self, userId: str):
        url = f"{self.address}/api/blocking/delete"
        params = {"userId": userId}
        r = await request(self.address, self.__i, "blocking/delete", params)
        return AttrDict(r)

    async def blocking_list(
        self, limit: int = 30, sinceId: str = None, untilId: str = None
    ):
        params = {
            "limit": limit,
        }
        if not sinceId is None:
            params["sinceId"] = sinceId
        if not untilId is None:
            params["untilId"] = untilId
        r = await request(self.address, self.__i, "blocking/list", params)
        return AttrDict(r)

    async def ping(self):
        """
        pong
        """
        url = f"{self.address}/api/ping"
        head = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, headers=head)
            return AttrDict(r.json())

    async def email_address_available(self, emailAddress):
        return AttrDict(
            request(
                self.address,
                self.__i,
                "email-address/available",
                {"emailAddress": emailAddress},
            )
        )

    async def username_available(self, username):
        return AttrDict(
            request(
                self.address, self.__i, "username/available", {"username": username}
            )
        )

    async def pinned_users(self):
        return AttrDict(request(self.address, self.__i, "pinned-users", {}))

    async def users(
        self, limit=10, offset=0, sort=None, state="all", origin="local", hostname=None
    ):
        base = {
            "limit": limit,
            "offset": offset,
            "state": state,
            "origin": origin,
            "hostname": hostname,
        }
        if nonecheck(sort):
            base["sort"] = sort
        return AttrDict(request(self.address, self.__i, "users", base))

    async def users_clips(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "users/clips", base))

    async def users_followers(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "users/followers", base))

    async def users_following(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "users/following", base))

    async def users_gallery_posts(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.__i, "users/gallery/posts", base)
        )

    async def users_pages(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "users/pages", base))

    async def users_reactions(
        self,
        userId,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
    ):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return AttrDict(await request(self.address, self.__i, "users/reactions", base))

    async def users_recommendation(
        self,
        limit=10,
        offset=0,
    ):
        base = {"limit": limit, "offset": offset}
        return AttrDict(
            await request(self.address, self.__i, "users/recommendation", base)
        )

    async def users_relation(self, userId):
        return AttrDict(
            await request(self.address, self.__i, "users/relation", {"userId": userId})
        )

    async def users_report_abuse(self, userId, comment):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "users/report-abuse",
                {"userId": userId, "comment": comment},
            )
        )

    async def users_search_by_username_and_host(
        self, username=None, host=None, limit=10, detail=True
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "users/search-by-username-and-host",
                {"username": username, "host": host, "limit": limit, "detail": detail},
            )
        )

    async def users_search(
        self, query, offset=0, limit=10, origin="combined", detail=True
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "users/search",
                {
                    "query": query,
                    "offset": offset,
                    "limit": limit,
                    "origin": origin,
                    "detail": detail,
                },
            )
        )

    async def users_show(self):
        return AttrDict(await request(self.address, self.__i, "users/show", {}))

    async def users_stats(self, userId):
        return AttrDict(
            await request(self.address, self.__i, "users/stats", {"userId": userId})
        )

    async def users_get_frequently_replied_users(
        self,
        userId,
        limit=10,
    ):
        base = {"userId": userId, "limit": limit}
        return AttrDict(
            await request(
                self.address, self.__i, "users/get-frequently-replied-users", base
            )
        )

    async def users_notes(
        self,
        userId,
        includeReplies=True,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
        includeMyRenotes=True,
        withFiles=False,
        fileType=None,
        excludeNsfw=False,
    ):
        base = {
            "userId": userId,
            "includeReplies": includeReplies,
            "limit": limit,
            "includeMyRenotes": includeMyRenotes,
            "withFiles": withFiles,
            "excludeNsfw": excludeNsfw,
        }
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        if nonecheck(withFiles):
            base["withFiles"] = withFiles
        if nonecheck(fileType):
            base["fileType"] = fileType
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.__i, "users/notes", base))

    async def following_create(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/create", {"userId": userId}
            )
        )

    async def following_delete(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/delete", {"userId": userId}
            )
        )

    async def following_invalidate(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/invalidate", {"userId": userId}
            )
        )

    async def following_requests_accept(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/requests/accept", {"userId": userId}
            )
        )

    async def following_requests_cancel(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/requests/cancel", {"userId": userId}
            )
        )

    async def following_requests_list(self):
        return AttrDict(
            await request(self.address, self.__i, "following/requests/list", {})
        )

    async def following_requests_reject(self, userId):
        return AttrDict(
            await request(
                self.address, self.__i, "following/requests/reject", {"userId": userId}
            )
        )

    async def hashtags_list(
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

    async def hashtags_search(
        self,
        query,
        limit=10,
        offset=0
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/search",
                {"query": query, "limit": limit, "offset": offset}
            )
        )
        
    async def hashtags_search(
        self,
        tag
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/show",
                {"tag": tag}
            )
        )

    async def hashtags_trend(
        self
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/trend",
                {}
            )
        )

    async def hashtags_users(
        self,
        tag,
        sort,
        limit=10,
        state="all",
        origin="local"
    ):
        return AttrDict(
            await request(
                self.address,
                self.__i,
                "hashtags/users",
                {"tag": tag, "sort": sort, "limit": limit, "state": state, "origin": origin}
            )
        )