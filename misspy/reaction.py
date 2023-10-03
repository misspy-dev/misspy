from typing import Any
from .http import request


class reactions:
    
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

    async def create(address, i, noteId, reaction):
        """create reaction.

        Args:
            address (string): instance address
            i (string): user token
            noteId (string): noteId
            reaction (string): Specify reaction. Reactions are Unicode emojis or custom emojis. For custom emoji, enclose the emoji name with a colon.

        Returns:
            dict: Misskey API response
        """
        return await request(
            address, i, "notes/reactions/create", {"noteId": noteId, "reaction": reaction}
        )


    async def delete(address, i, noteId):
        """delete reaction.

        Args:
            address (string): instance address
            i (string): user token
            noteId (string): noteId

        Returns:
            dict: Misskey API response
        """
        return await request(address, i, "notes/reactions/delete", {"noteId": noteId})