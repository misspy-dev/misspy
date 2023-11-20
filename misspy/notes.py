from .util import nonecheck

from .core.http import request
from .types import User, Note

class notes:
    """misskey notes class.
    
    """

    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl
        
    async def note(
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
        """Retrieves the list of notes.

        Args:
            local (bool, optional): Only locally created notes are retrieved. Defaults to False.
            reply (bool, optional): If `true`, only replies are retrieved; if `false`, non-replies are retrieved. If no value is set, notes are retrieved regardless of whether they are replies or not. Defaults to None.
            renote (bool, optional): If `true`, only renotes are retrieved; if `false`, non-renotes are retrieved. If no value is set, notes are retrieved regardless of whether they are replies or not. Defaults to None.
            withFiles (bool, optional): If `true`, only notes with attachments will be retrieved; if `false`, only notes without attachments will be retrieved. If no value is set, notes are retrieved with or without attachments. Defaults to None.
            poll (bool, optional): If `true`, only notes with votes will be retrieved; if `false`, only notes without votes will be retrieved. If no value is set, notes are retrieved with or without votes. Defaults to None.
            limit (int, optional): Specifies the maximum number of notes to be retrieved. Defaults to 10.
            sinceId (str, optional): If specified, returns notes whose id is greater than its value. Defaults to None.
            untilId (str, optional): If specified, returns notes whose id is less than the value. Defaults to None.

        Returns:
            List (in Dict): notes dict
        """
        base = {"i": self.i, "local": local, "limit": limit}
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
        return await request(self.address, self.i, "notes", base)


    async def conversation(self, noteId: str, limit: int = 10, offset: int = 0):
        """Retrieve relevant notes.

        Args:
            noteId (str): noteId.
            limit (int, optional): limit of Retrieve. Defaults to 10.
            offset (int, optional): Skip the first offset of the result. Defaults to 0.

        Returns:
            _type_: _description_
        """
        return await request(
            self.address,
            self.i, 
            "notes/conversation",
            {"noteId": noteId, "limit": limit, "offset": offset},
        )


    async def global_timeline(
        self,
        withFiles=False,
        limit=10,
        sinceId=None,
        untilId=None,
        sinceDate=None,
        untilDate=None,
    ):
        """Get the Global Timeline (GTL). The global timeline contains all public posts received by the server.

        Args:
            withFiles (bool, optional): If set to true, only notes with files attached will be retrieved.
            limit (int, optional): Specifies the maximum number of notes to be retrieved. Defaults to 10.
            sinceId (str, optional): If specified, returns notes whose id is greater than its value. Defaults to None.
            untilId (str, optional): If specified, returns notes whose id is less than the value. Defaults to None.
            sinceDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created after that date and time.
            untilDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created before that date and time.

        Returns:
            List (in Dict): notes dict
        """
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
        """Get the social Timeline (STL). The social timeline includes all public notes in the server and those of users you follow.

        Args:
            limit (int, optional): Specifies the maximum number of notes to be retrieved. Defaults to 10.
            sinceId (str, optional): If specified, returns notes whose id is greater than its value. Defaults to None.
            untilId (str, optional): If specified, returns notes whose id is less than the value. Defaults to None.
            sinceDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created after that date and time.
            untilDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created before that date and time.
            includeMyRenotes (bool, optional): If true, include the renotes made by the currently logged in user.
            includeRenotedMyNotes (bool, optional): If true, include the Renotes posted by the currently logged in user.
            includeLocalRenotes (bool, optional): If true, include the renotes made by local users.
            withFiles (bool, optional): If set to true, only notes with files attached will be retrieved.

        Returns:
            List (in Dict): notes dict
        """
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
        """Get Home Timeline (HTL). The home timeline contains the notes of the users you follow.

        Args:
            limit (int, optional): Specifies the maximum number of notes to be retrieved. Defaults to 10.
            sinceId (str, optional): If specified, returns notes whose id is greater than its value. Defaults to None.
            untilId (str, optional): If specified, returns notes whose id is less than the value. Defaults to None.
            sinceDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created after that date and time.
            untilDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created before that date and time.
            includeMyRenotes (bool, optional): If true, include the renotes made by the currently logged in user.
            includeRenotedMyNotes (bool, optional): If true, include the Renotes posted by the currently logged in user.
            includeLocalRenotes (bool, optional): If true, include the renotes made by local users.
            withFiles (bool, optional): If set to true, only notes with files attached will be retrieved.

        Returns:
            List (in Dict): notes dict
        """
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
        """Get the Local Timeline (LTL). The local timeline contains all public notes in the server.
        
        Args:
            withFiles (bool, optional): If set to true, only notes with files attached will be retrieved.
            fileType (bool, optional): Retrieve only those posts with files of the specified type attached.
            excludeNsfw (bool, optional): If true, excludes notes with CWs and notes with NSFW-specified files attached, effective only if fileType is specified (notes with CWs without attachments are not excluded).
            limit (int, optional): Specifies the maximum number of notes to be retrieved. Defaults to 10.
            sinceId (str, optional): If specified, returns notes whose id is greater than its value. Defaults to None.
            untilId (str, optional): If specified, returns notes whose id is less than the value. Defaults to None.
            sinceDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created after that date and time.
            untilDate (int, optional): If you specify a date and time in epoch seconds, it returns notes created before that date and time.
            includeMyRenotes (bool, optional): If true, include the renotes made by the currently logged in user.
            includeRenotedMyNotes (bool, optional): If true, include the Renotes posted by the currently logged in user.
            includeLocalRenotes (bool, optional): If true, include the renotes made by local users.

        Returns:
            List (in Dict): notes dict
        """
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
        """Retrieves highlighted notes. Results are sorted in descending order of note creation time (latest first).

        Args:
            limit (int, optional): Maximum number of notes to be retrieved. Defaults to 10.
            offset (int, optional): The first offset of the search result is skipped. Defaults to 0.

        Returns:
            List (Dict): _description_
        """
        return await request(
            self.address, self.i, "notes/featured", {"limit": limit, "offset": offset}
        )


    async def favorites_create(self, noteId):
        """create favorites.

        Args:
            noteId (str): noteId.

        Returns:
            Dict: _description_
        """
        return await request(self.address, self.i, "notes/favorites/create", {"noteId": noteId})


    async def favorites_delete(self, noteId):
        """delete favorites

        Args:
            noteId (str): noteId.

        Returns:
            Dict: _description_
        """
        return await request(self.address, self.i, "notes/favorites/delete", {"noteId": noteId})


    async def polls_recommendation(self, limit=10, offset=0):
        """Get a list of recommended notes with a survey.

        Args:
            limit (int, optional): Maximum number of notes to be retrieved. Defaults to 10.
            offset (int, optional): The first offset of the search result is skipped. Defaults to 0.

        Returns:
            _type_: _description_
        """
        return await request(
            self.address, self.i, "notes/polls/recommendation", {"limit": limit, "offset": offset}
        )


    async def polls_vote(self, noteId, choice):
        """Vote in the notebook poll. To vote for multiple choices, change the choice and make multiple requests.

        Args:
            noteId (str): ID of the note to which the survey is attached.
            choice (str): Choices to vote on.

        Returns:
            _type_: _description_
        """
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
        self, noteId: str, sinceId: str = None, untilId: str = None, limit: int = 10
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
        return await request(self.address, self.i, "notes/thread-muting/create", {"noteId": noteId})


    async def thread_muting_delete(self, noteId):
        return await request(self.address, self.i, "notes/thread-muting/delete", {"noteId": noteId})


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
        self, following=False, limit=10, sinceId=None, untilId=None, visibility=None
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
            dict: Misskey API response
        """
        base = {
            "visibility": visibility,
            "localOnly": localOnly,
            "noExtractMentions": noExtractMentions,
            "noExtractEmojis": noExtractEmojis,
            "cw": cw
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
        req = await request(
            self.address, self.i, "notes/create", base, header={"Content-Type": "application/json"}
        )
        return req


    async def delete(self, noteId):
        return await request(self.address, self.i, "notes/delete", {"noteId": noteId})


    async def children(self, noteId, limit, sinceId, untilId):
        base = {"noteId": noteId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return await request(self.address, self.i, "notes/children", base)
