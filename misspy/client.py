from __future__ import annotations
import asyncio
import json

from attrdictionary import AttrDict

from .channels import channels
from .clips import clips
from .drive import drive
from .federation import federation
from .hook import hook
from .pages import pages
from .http import request
from .MiWeb import MiWeb
from .hashtags import hashtags
from .reaction import reactions
from .notes import notes
from .server import server
from .user import i, users, following
from .ws import MiWS

class hook:
    functions = {}

    def add(event, func):
        """add

        Args:
            event (str): streaming event type. (view docs)
            func (funct): Function to call on events entered in event

        Returns:
            bool: True
        """

        hook.functions[event] = func
        return True

    def remove(event):
        """remove

        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        hook.functions[event] = None
        return True

    def reload(event):
        """reload

        Internally, it just executes remove and add.
        
        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        func = hook.functions[event]
        hook.remove(event)
        hook.add(event, func)
        return True


class Bot:
    """
    Class used to connect and interact with the Misskey Streaming API.
    """

    def __init__(self, address, token=None, ssl=True) -> None:
        self.ssl = False
        if ssl:
            self.ssl = True

        if not address.startswith("http://") and not address.startswith("https://"):
            self.address = "http://" + address
            if ssl:
                self.address = "https://" + address
        else:
            self.address = address
            self.address_raw = address.replace("https://", "").replace("http://", "")
        self.__i = token
        self.ws = MiWS(self.address_raw, self.__i)
        self.reactions = reactions(self.address, self.__i)
        self.notes = notes(self.address, self.__i)
        self.server = server(self.address, self.__i)
        self.users = users(self.address, self.__i)
        self.following = following(self.address, self.__i)
        self.misskey_web = MiWeb(self.address, self.__i)
        self.hashtags = hashtags(self.address, self.__i)
        self.pages = pages(self.address, self.__i)
        self.drive = drive(self.address, self.__i)
        self.federation = federation(self.address, self.__i)
        self.channels = channels(self.address, self.__i)
        self.clips = clips(self.address, self.__i)
        self.i = i(self.address, self.__i)
        self.bot = self.server.user()

    def run(self):
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

    async def unsubNote(self, noteId):
        await self.ws.connection.send(
            json.dumps(
                {
                    "type": "unsubNote",
                    "body": {"id": noteId},
                }
            )
        )

    async def subNote(self, noteId):
        await self.ws.connection.send(
            json.dumps(
                {
                    "type": "subNote",
                    "body": {"id": noteId},
                }
            )
        )


    async def pinned_users(self):
        return AttrDict(request(self.address, self.__i, "pinned-users", {}))