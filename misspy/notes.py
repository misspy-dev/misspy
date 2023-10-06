from .util import nonecheck
from .http import request
from .types import User, Note


class notes:
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
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

    async def get(
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
        base = {"local": local, "limit": limit}
        if nonecheck(reply):
            base["reply"] = reply
        if nonecheck(renote):
            base["renote"] = renote
        if nonecheck(withFiles):
            base["withFiles"] = withFiles
        if nonecheck(poll):
            base["poll"] = poll
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        resp = await request(self.address, self.i, "notes", base)
        obj = []
        for i in resp:
            user = User(
                resp["user"]["id"],
                resp["user"]["createdAt"],
                resp["user"]["username"],
                resp["user"]["host"],
                resp["user"]["name"],
                resp["user"]["onlineStatus"],
                resp["user"]["avatarUrl"],
                resp["user"]["avatarBlurhash"],
            )
            note = Note(
                resp["id"],
                resp["createdAt"],
                resp["text"],
                resp["cw"],
                user,
                resp["userId"],
                resp["visibility"]
            )
            obj.append(note)
        return obj

    async def conversation(self, noteId: str, limit: int = 10, offset: int = 0):
        resp = await request(
            self.address,
            self.i,
            "notes/conversation",
            {"noteId": noteId, "limit": limit, "offset": offset},
        )
        obj = []
        for i in resp:
            user = User(
                resp["user"]["id"],
                resp["user"]["createdAt"],
                resp["user"]["username"],
                resp["user"]["host"],
                resp["user"]["name"],
                resp["user"]["onlineStatus"],
                resp["user"]["avatarUrl"],
                resp["user"]["avatarBlurhash"],
            )
            note = Note(
                resp["id"],
                resp["createdAt"],
                resp["text"],
                resp["cw"],
                user,
                resp["userId"],
                resp["visibility"]
            )
            obj.append(note)
        return obj

    async def global_timeline(
        self,
        withFiles=False,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
    ):
        base = {"withFiles": withFiles, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return await request(self.address, self.i, "notes/global-timeline", base)

    async def hybrid_timeline(
        self,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
        includeMyRenotes=True,
        includeRenotedMyNotes=True,
        includeLocalRenotes=True,
        withFiles=False,
    ):
        base = {
            "withFiles": withFiles,
            "limit": limit,
            "includeMyRenotes": includeMyRenotes,
            "includeRenotedMyNotes": includeRenotedMyNotes,
            "includeLocalRenotes": includeLocalRenotes,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return await request(self.address, self.i, "notes/hybrid-timeline", base)

    async def home_timeline(
        self,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
        includeMyRenotes=True,
        includeRenotedMyNotes=True,
        includeLocalRenotes=True,
        withFiles=False,
    ):
        base = {
            "withFiles": withFiles,
            "limit": limit,
            "includeMyRenotes": includeMyRenotes,
            "includeRenotedMyNotes": includeRenotedMyNotes,
            "includeLocalRenotes": includeLocalRenotes,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return await request(self.address, self.i, "notes/timeline", base)

    async def local_timeline(
        self,
        withFiles=False,
        fileType=None,
        excludeNsfw=False,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
    ):
        base = {"withFiles": withFiles, "limit": limit, "excludeNsfw": excludeNsfw}
        if nonecheck(fileType):
            base["fileType"] = fileType
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(sinceDate):
            base["sinceDate"] = sinceDate
        if nonecheck(untilDate):
            base["untilDate"] = untilDate
        return await request(self.address, self.i, "notes/local-timeline", base)

    async def featured(self, limit=10, offset=0):
        return await request(
            self.address, self.i, "notes/featured", {"limit": limit, "offset": offset}
        )

    async def favorites_create(self, noteId):
        return await request(self.address, self.i, "notes/favorites/create", {"noteId": noteId})

    async def favorites_delete(self, noteId):
        return await request(self.address, self.i, "notes/favorites/delete", {"noteId": noteId})

    async def polls_recommendation(self, limit=10, offset=0):
        return await request(
            self.address, self.i, "notes/polls/recommendation", {"limit": limit, "offset": offset}
        )

    async def polls_vote(self, noteId, choice):
        return await request(
            self.address, self.i, "notes/polls/vote", {"noteId": noteId, "choice": choice}
        )

    async def reactions(
        self,
        noteId: str,
        type: str = None,
        limit: int = 10,
        offset: int = 0,
        sinceId: str = None,
        untilId: str = None,
    ):
        base = {"noteId": noteId, "type": type, "limit": limit, "offset": offset}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/reactions", base)

    async def replies(
        self,
        noteId: str,
        sinceId: str = None,
        untilId: str = None,
        limit: int = 10,
    ):
        base = {"noteId": noteId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/replies", base)

    async def search(
        self,
        reply=False,
        renote=False,
        withFiles=False,
        poll=False,
        sinceId=None,
        untilId=None,
        limit=10,
    ):
        base = {
            "reply": reply,
            "renote": renote,
            "withFiles": withFiles,
            "poll": poll,
            "limit": limit,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/search-by-tag", base)

    async def search_by_tag(
        self,
        query,
        sinceId=None,
        untilId=None,
        limit=10,
        offset=0,
        host=None,
        userId=None,
        channelId=None,
    ):
        base = {
            "query": query,
            "offset": offset,
            "limit": limit,
            "host": host,
            "userId": userId,
            "channelId": channelId,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/search", base)

    async def state(self, noteId):
        return await request(self.address, self.i, "notes/state", {"noteId": noteId})

    async def show(self, noteId):
        return await request(self.address, self.i, "notes/show", {"noteId": noteId})

    async def thread_muting_create(self, noteId):
        return await request(
            self.address, self.i, "notes/thread-muting/create", {"noteId": noteId}
        )

    async def thread_muting_delete(self, noteId):
        return await request(
            self.address, self.i, "notes/thread-muting/delete", {"noteId": noteId}
        )

    async def translate(self, noteId, targetLang):
        return await request(
            self.address, self.i, "notes/translate", {"noteId": noteId, "targetLang": targetLang}
        )

    async def unrenote(self, noteId):
        return await request(self.address, self.i, "notes/unrenote", {"noteId": noteId})

    async def user_list_timeline(
        self,
        listId,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=0,
        untilDate=0,
        includeMyRenotes=True,
        includeRenotedMyNotes=True,
        includeLocalRenotes=True,
        withFiles=False,
    ):
        base = {
            "listId": listId,
            "limit": limit,
            "sinceDate": sinceDate,
            "untilDate": untilDate,
            "includeMyRenotes": includeMyRenotes,
            "includeRenotedMyNotes": includeRenotedMyNotes,
            "includeLocalRenotes": includeLocalRenotes,
            "withFiles": withFiles,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/user-list-timeline", base)

    async def watching_create(self, noteId):
        return await request(self.address, self.i, "notes/watching/create", {"noteId": noteId})

    async def watching_delete(self, noteId):
        return await request(self.address, self.i, "notes/watching/delete", {"noteId": noteId})

    async def mentions(
        self,
        following=False,
        limit=10,
        sinceId=None,
        untilId=None,
        visibility=None,
    ):
        base = {"following": following, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        if nonecheck(visibility):
            base["visibility"] = visibility
        return await request(self.address, self.i, "notes/mentions", base)

    async def create(
        self,
        text: str = None,
        visibility="public",
        visibleUserIds: list = None,
        cw=None,
        replyid=None,
        fileid=None,
        channelId=None,
        localOnly: bool = False,
        renoteId=None,
        noExtractMentions: bool = False,
        noExtractEmojis: bool = False,
        poll=None,
    ):  # 82行→57行に短くできた
        """Create notes. Reply and Renote are also done with this function.

        Args:
            address (str): misskey server address
            i (str): misskey api token
            text (str): note content
            visibility (str): Public scope of the note. Defaults to "public".
            visibleUserIds (list, optional): ID of the user as seen for direct notes. Defaults to None.
            replyid (_type_, optional): the id of the note to reply to. Defaults to None.
            fileid (_type_, optional): notes attached file id. Defaults to None.
            channelId (_type_, optional): The id of the channel to post to. Defaults to None.
            localOnly (bool, optional): If true, posts to local timeline only.. Defaults to False.
            renoteId (_type_, optional): the id of the note to renote to.. Defaults to None.

        Returns:
            Note: Misskey API response
        """

        base = {
            "visibility": visibility,
            "localOnly": localOnly,
            "noExtractMentions": noExtractMentions,
            "noExtractEmojis": noExtractEmojis,
            "cw": cw,
        }
        if poll is not None:
            base["poll"] = {}
            base["poll"]["choices"] = poll.choices
            base["poll"]["multiple"] = poll.multiple
            base["poll"]["expiresAt"] = poll.expiresAt
            base["poll"]["expiredAfter"] = poll.expiredAfter
        if text is not None:
            base["text"] = text
        if visibleUserIds is not None:
            base["visibleUserIds"] = visibleUserIds
        if replyid is not None:
            base["replyid"] = replyid
        if fileid is not None:
            base["fileIds"] = fileid
        if channelId is not None:
            base["channelId"] = channelId
        if renoteId is not None:
            base["renoteId"] = renoteId
        resp = await request(
            self.address, 
            self.i, 
            "notes/create",
            base,
            header={"Content-Type": "application/json"},
        )
        
        user = User(
            resp["createdNote"]["user"]["id"],
            resp["createdNote"]["user"]["createdAt"],
            resp["createdNote"]["user"]["username"],
            resp["createdNote"]["user"]["host"],
            resp["createdNote"]["user"]["name"],
            resp["createdNote"]["user"]["onlineStatus"],
            resp["createdNote"]["user"]["avatarUrl"],
            resp["createdNote"]["user"]["avatarBlurhash"],
        )
        note = Note(
            resp["createdNote"]["id"],
            resp["createdNote"]["createdAt"],
            resp["createdNote"]["text"],
            resp["createdNote"]["cw"],
            user,
            resp["createdNote"]["userId"],
            resp["createdNote"]["visibility"]
            )
        return note

    async def delete(self, noteId):
        return await request(self.address, self.i, "notes/delete", {"noteId": noteId})

    async def children(self, noteId, limit, sinceId, untilId):
        base = {"noteId": noteId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/children", base)
