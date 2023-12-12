import asyncio

try:
    import orjson as json
except ModuleNotFoundError:
    import json

from .ws import MiWS
from .hook import cmdHook

from ...channels import channels
from ...clips import clips
from ...drive import drive
from ...federation import federation

from ...pages import pages
from ...MiWeb import MiWeb
from ...hashtags import hashtags
from ...reaction import reactions
from ...notes import notes
from ...server import server
from ...user import i, users, following


class Bot:

    def __init__(self, address, __i=None, ssl=True) -> None:
        self.address = address
        self.__i = __i
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

        self.add_hook = cmdHook.add_hook
        self.remove_hook = cmdHook.remove_hook
        self.reload_hook = cmdHook.reload_hook

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

        self.set_ui()
        self.index_cmd = "cmd_" + self.username

        self.ws = MiWS(self.address_raw, self.__i, self.ssl, ui={"id": self.id, "name": self.name, "username": self.username})
        

    def set_ui(self):
        self.id = self.mi.id  # ment__ions
        self.name = self.mi.name
        self.username = self.mi.username
        return {"id": self.id, "name": self.name, "username": self.username}

    def start(self):
        asyncio.run(self.ws.ws_handler())

    async def connect(self, channel):
        await self.ws.connection.send(
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

    async def unsubNote(self, note_id):
        await self.ws.connection.send(
            json.dumps(
                {
                    "type": "unsubNote",
                    "body": {"__id": note_id},
                }
            )
        )

    async def subNote(self, note_id):
        await self.ws.connection.send(
            json.dumps(
                {
                    "type": "subNote",
                    "body": {"id": note_id},
                }
            )
        )
