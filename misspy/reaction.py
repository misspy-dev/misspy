from typing import Any
from .core.http import request


class reactions:
    def __init__(self, address, i, ssl=True) -> None:
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
        self.i = i

    async def create(self, noteId, reaction):
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
            self.address, self.i, "notes/reactions/create", {"noteId": noteId, "reaction": reaction}
        )


    async def delete(self, noteId):
        """delete reaction.

        Args:
            address (string): instance address
            i (string): user token
            noteId (string): noteId

        Returns:
            dict: Misskey API response
        """
        return await request(self.address, self.i, "notes/reactions/delete", {"noteId": noteId})