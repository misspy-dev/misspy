from attrdictionary import AttrDict

from .notes import create
from . import reaction

async def add_reaction(address, token, Id):
    async def inner(reactionId):
        return await reaction.create(address, token, Id, reactionId)
        
    return AttrDict(inner)

async def remove_reaction(address, token, Id):
    return AttrDict(await reaction.delete(address, token, Id))

async def reply(address, token, Id):
    async def inner(
        text: str = None,
        visibility="public",
        visibleUserIds: list = None,
        fileid=None,
        channelId=None,
        localOnly: bool = False,
        noExtractMentions: bool = False,
        noExtractEmojis: bool = False,
        poll = None,
    ):
        return await create(address, token, text, visibility, visibleUserIds, Id, fileid, channelId, localOnly, None, noExtractMentions, noExtractEmojis, poll)
    return AttrDict(inner)

async def renote(address, token, Id):
    async def inner(
        text: str = None,
        visibility="public",
        visibleUserIds: list = None,
        fileid=None,
        channelId=None,
        localOnly: bool = False,
        noExtractMentions: bool = False,
        noExtractEmojis: bool = False,
        poll = None,
    ):
        return await create(address, token, text, visibility, visibleUserIds, None, fileid, channelId, localOnly, Id, noExtractMentions, noExtractEmojis, poll)
    return AttrDict(inner)