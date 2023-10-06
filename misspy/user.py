from attrdictionary import AttrDict

from .util import nonecheck
from .http import request, request_sync


class i:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl
        
    async def get(self):
        r = await request(self.address, self.i, "i", {})
        return AttrDict(r)

    async def favorites(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "i/favorites", base))

    async def gallery_likes(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "i/gallery/likes", base))

    async def gallery_posts(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "i/gallery/posts", base))

    async def get_word_muted_notes_count(
        self
    ):
        return AttrDict(
            await request(self.address, self.i, "i/get-word-muted-notes-count", {})
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
        return AttrDict(await request(self.address, self.i, "i/notifications", base))

    async def page_likes(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "i/page-likes", base))

    async def pages(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "i/pages", base))
    
    async def pin(self, noteId):
        return AttrDict(
            await request(self.address, self.i, "i/pin", {"noteId": noteId})
        )

    async def unpin(self, noteId):
        return AttrDict(
            await request(self.address, self.i, "i/unpin", {"noteId": noteId})
        )

    async def update(self, params):
        return AttrDict(await request(self.address, self.i, "i/update", params))

    async def read_all_messaging_messages(self):
        return AttrDict(
            await request(self.address, self.i, "i/read-all-messaging-messages", {})
        )

    async def read_all_unread_notes(self):
        return AttrDict(
            await request(self.address, self.i, "i/read-all-unread-notes", {})
        )

    async def read_announcement(self, announcementId):
        return AttrDict(
            await request(self.address, self.i, 
                "i/read-all-unread-notes",
                {"announcementId": announcementId},
            )
        )
    
    
class blocking:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address

    async def create(self, userId: str):
        params = {"userId": userId}
        r = await request(self.address, self.i, "blocking/create", params)
        return AttrDict(r)

    async def delete(self, userId: str):
        params = {"userId": userId}
        r = await request(self.address, self.i, "blocking/delete", params)
        return AttrDict(r)

    async def list(
        self, limit: int = 30, sinceId: str = None, untilId: str = None
    ):
        params = {
            "limit": limit,
        }
        if not sinceId is None:
            params["sinceId"] = sinceId
        if not untilId is None:
            params["untilId"] = untilId
        r = await request(self.address, self.i, "blocking/list", params)
        return AttrDict(r)

class antennas:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        
    async def create(
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
        return AttrDict(request("antennas/create", base))

    async def update(
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
        return AttrDict(request("antennas/update", base))

    async def delete(self, antennaId):
        return AttrDict(
            request("antennas/delete", {"antennaId": antennaId})
        )

    async def show(self, antennaId):
        return AttrDict(
            request("antennas/show", {"antennaId": antennaId})
        )

    async def list(self):
        return AttrDict(request("antennas/list", {}))

    async def notes(
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
        return AttrDict(await request(self.address, self.i, "federation/users", base))


class mute:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address

    async def create(self, userId, expiresAt=None):
        return AttrDict(
            await request(self.address, self.i, 
                "mute/create",
                {"userId": userId, "expiresAt": expiresAt},
            )
        )

    async def create(self, limit=30, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "mute/list", base))

    async def delete(self, userId):
        return AttrDict(
            await request(self.address, self.i, "mute/delete", {"userId": userId})
        )

class users:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        
    async def get(
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
        return AttrDict(request("users", base))

    async def users_clips(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "users/clips", base))

    async def users_followers(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "users/followers", base))

    async def users_following(self, limit=10, sinceId=None, untilId=None):
        base = {"limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "users/following", base))

    async def users_gallery_posts(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            await request(self.address, self.i, "users/gallery/posts", base)
        )

    async def users_pages(self, userId, limit=10, sinceId=None, untilId=None):
        base = {"userId": userId, "limit": limit}
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(await request(self.address, self.i, "users/pages", base))

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
        return AttrDict(await request(self.address, self.i, "users/reactions", base))

    async def users_recommendation(
        self,
        limit=10,
        offset=0,
    ):
        base = {"limit": limit, "offset": offset}
        return AttrDict(
            await request(self.address, self.i, "users/recommendation", base)
        )

    async def users_relation(self, userId):
        return AttrDict(
            await request(self.address, self.i, "users/relation", {"userId": userId})
        )

    async def users_report_abuse(self, userId, comment):
        return AttrDict(
            await request(self.address, self.i, 
                "users/report-abuse",
                {"userId": userId, "comment": comment},
            )
        )

    async def users_search_by_username_and_host(
        self, username=None, host=None, limit=10, detail=True
    ):
        return AttrDict(
            await request(self.address, self.i, 
                "users/search-by-username-and-host",
                {"username": username, "host": host, "limit": limit, "detail": detail},
            )
        )

    async def users_search(
        self, query, offset=0, limit=10, origin="combined", detail=True
    ):
        return AttrDict(
            await request(self.address, self.i, 
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

    def users_show(self, username, host=None):
        d = request_sync(
            "users/show", {"username": username, "host": None}
        )
        return AttrDict(d)

    async def users_stats(self, userId):
        return AttrDict(
            await request(self.address, self.i, "users/stats", {"userId": userId})
        )

    async def users_get_frequently_replied_users(
        self,
        userId,
        limit=10,
    ):
        base = {"userId": userId, "limit": limit}
        return AttrDict(
            await request(self.address, self.i, 
                "users/get-frequently-replied-users", base
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
        return AttrDict(await request(self.address, self.i, "users/notes", base))
    
class following:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
    
    async def create(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/create", {"userId": userId}
            )
        )

    async def delete(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/delete", {"userId": userId}
            )
        )

    async def invalidate(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/invalidate", {"userId": userId}
            )
        )

    async def requests_accept(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/requests/accept", {"userId": userId}
            )
        )

    async def requests_cancel(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/requests/cancel", {"userId": userId}
            )
        )

    async def requests_list(self):
        return AttrDict(
            await request(self.address, self.i, "following/requests/list", {})
        )

    async def requests_reject(self, userId):
        return AttrDict(
            await request(self.address, self.i, 
                "following/requests/reject", {"userId": userId}
            )
        )