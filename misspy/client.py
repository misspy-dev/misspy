from __future__ import annotations
import asyncio

try:
    import orjson as json
except ModuleNotFoundError:
    import json
from attrdictionary import AttrDict

from .channels import channels
from .clips import clips
from .drive import drive
from .federation import federation

from .pages import pages
from .core.http import request
from .MiWeb import MiWeb
from .hashtags import hashtags
from .reaction import reactions
from .notes import notes
from .server import server
from .user import i, users, following
from .core.ws import MiWS
from .hook import hook

class Bot:
    """
    Class used to connect and interact with the Misskey Streaming API.
    """

    def __init__(self, address, token=None, ssl=True) -> None:
        self.ssl = ssl

        http = "http://"
        https = "https://"
        if not address.startswith(http) and not address.startswith(https):
            self.address = http + address
            if ssl:
                self.address = https + address
            self.address_raw = address
        else:
            self.address = address
            self.address_raw = address.replace(https, "").replace(http, "")
        self.__i = token
        self.ws = MiWS(self.address_raw, self.__i, self.ssl)
        self.reactions = reactions(self.address, self.__i, self.ssl)
        self.notes = notes(self.address, self.__i, self.ssl)
        self.server = server(self.address, self.__i, self.ssl)
        self.users = users(self.address, self.__i, self.ssl)
        self.following = following(self.address, self.__i, self.ssl)
        self.misskey_web = MiWeb(self.address, self.__i, self.ssl)
        self.hashtags = hashtags(self.address, self.__i, self.ssl)
        self.pages = pages(self.address, self.__i, self.ssl)
        self.drive = drive(self.address, self.__i, self.ssl)
        self.federation = federation(self.address, self.__i, self.ssl)
        self.channels = channels(self.address, self.__i, self.ssl)
        self.clips = clips(self.address, self.__i, self.ssl)
        self.i = i(self.address, self.__i, self.ssl)
        self.mi = self.server.user()
        self.add_hook = hook.add
        self.remove_hook = hook.remove
        self.reload_hook = hook.reload

        self.set_ui()

    def run(self):
        asyncio.run(self.ws.ws_handler())

    def set_ui(self):
        self.id = self.mi.id  # ment__ions
        self.name = self.mi.name
        self.username = self.mi.username

    async def connect(self, channel):
        await self.ws.connection.send_str(
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
        await self.ws.connection.send_str(
            json.dumps(
                {
                    "type": "unsubNote",
                    "body": {"id": noteId},
                }
            )
        )

    async def subNote(self, noteId):
        await self.ws.connection.send_str(
            json.dumps(
                {
                    "type": "subNote",
                    "body": {"id": noteId},
                }
            )
        )


    async def pinned_users(self):
        return AttrDict(request(self.address, self.__i, "pinned-users", {}))
