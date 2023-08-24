import httpx

from .util import nonecheck
from .http import request
from .types import poll


async def note(
    address,
    i,
    local: bool = False,
    reply: bool = None,
    renote: bool = None,
    withFiles: bool = None,
    poll: bool = None,
    limit: int = 10,
    sinceId: str = None,
    untilId: str = None,
):
    base = {"i": i, "local": local, "limit": limit}
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
    return await request(address, i, "notes", base)


async def conversation(address, i, noteId: str, limit: int = 10, offset: int = 0):
    return await request(
        address,
        i,
        "notes/conversation",
        {"noteId": noteId, "limit": limit, "offset": offset},
    )


async def create(
    address,
    i,
    text: str = None,
    visibility="public",
    visibleUserIds: list = None,
    replyid=None,
    fileid=None,
    channelId=None,
    localOnly: bool = False,
    renoteId=None,
    noExtractMentions: bool = False,
    noExtractEmojis: bool = False,
    poll: poll = None,
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
        base["fileid"] = fileid
    if channelId is not None:
        base["channelId"] = channelId
    if renoteId is not None:
        base["renoteId"] = renoteId
    return await request(address, i, "notes/create", base)


async def delete(address, i, noteId):
    return await request(address, i, "notes/delete", {"noteId": noteId})


async def children(address, i, noteId, limit, sinceId, untilId):
    base = {"noteId": noteId, "limit": limit}
    if nonecheck(sinceId):
        base["sinceId"] = sinceId
    if nonecheck(untilId):
        base["untilId"] = untilId
    return await request(address, i, "notes/children", base)
