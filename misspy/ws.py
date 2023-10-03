import asyncio
import json

from attrdictionary import AttrDict
import websockets

from .client import hook
from . import exception

class MiWS:
    
    def __init__(self, address, i) -> None:
        self.i = i
        self.address = address
    
    async def ws_handler(self):
        try:
            procotol = "ws://"
            if self.ssl:
                procotol = "wss://"
            async with websockets.connect(
                f"{procotol}{self.address}/streaming?i={self.i}"
            ) as self.connection:
                try:
                    await hook.functions["ready"]()
                except KeyError:
                    pass
                while True:
                    recv = json.loads(await self.connection.recv())
                    try:
                        if recv["type"] == "channel":
                            if recv["body"]["type"] == "note":
                                await hook.functions[recv["body"]["type"]](
                                    AttrDict(recv["body"]["body"])
                                )
                            elif recv["body"]["type"] == "notification":
                                await hook.functions[recv["body"]["body"]["type"]](
                                    AttrDict(recv["body"]["body"])
                                )
                            elif recv["body"]["type"] == "follow":
                                await hook.functions[recv["body"]["type"]](
                                    AttrDict(recv["body"]["body"])
                                )
                            elif recv["body"]["type"] == "followed":
                                await hook.functions[recv["body"]["type"]](
                                    AttrDict(recv["body"]["body"])
                                )
                            elif recv["type"] == "noteUpdated":
                                await hook.functions[recv["body"]["type"]](
                                    AttrDict(recv["body"])
                                )
                            else:
                                await hook.functions[recv["body"]["type"]](
                                    AttrDict(recv["body"])
                                )
                    except KeyError:
                        pass
        except Exception as e:
            raise exception.WebsocketError(e)