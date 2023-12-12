import traceback
from functools import partial

from attrdictionary import AttrDict
import websockets
try:
    import orjson as json
except ModuleNotFoundError:
    import json

from ..hook import hook
from ..reaction import reactions
from ..notes import notes
from ..user import following

from . import exception


class MiWS:
    def __init__(self, address, i, ssl=True) -> None:
        self.i = i
        self.address = address
        self.ssl = ssl

        self.reactions = reactions(self.address, self.i, self.ssl)
        self.notes = notes(self.address, self.i, self.ssl)
        self.following = following(self.address, self.i, self.ssl)

    async def ws_handler(self):
        try:
            procotol = "ws://"
            if self.ssl:
                procotol = "wss://"
                async for self.connection in websockets.connect(
                    f"{procotol}{self.address}/streaming?i={self.i}"
                ):
                    try:
                        try:
                            await hook.functions["ready"]()
                        except KeyError:
                            pass
                        while True:
                            try:
                                recv = json.loads(await self.connection.recv())
                            except AttributeError:
                                pass
                            try:
                                if recv["type"] == "channel":
                                    if recv["body"]["type"] == "note":
                                        ctx = {}
                                        ctx["id"] = recv["body"]["body"]["id"]
                                        ctx["reply"] = partial(
                                            self.notes.create, replyid=ctx["id"]
                                        )
                                        ctx["renote"] = partial(
                                            self.notes.create, replyid=ctx["id"]
                                        )
                                        ctx["add_reaction"] = partial(
                                            self.reactions.create, noteId=ctx["id"]
                                        )
                                        ctx[
                                            "remove_reaction"
                                        ] = await self.reactions.delete(ctx["id"])
                                        await hook.functions[
                                            recv["body"]["body"]["type"]
                                        ](AttrDict(ctx), recv["body"]["body"])
                                    elif recv["body"]["type"] == "notification":
                                        await hook.functions[
                                            recv["body"]["body"]["type"]
                                        ](recv["body"]["body"])
                                    elif recv["body"]["type"] == "follow":
                                        await hook.functions[recv["body"]["type"]](
                                            recv["body"]["body"]
                                        )
                                    elif recv["body"]["type"] == "followed":
                                        await hook.functions[recv["body"]["type"]](
                                            recv["body"]["body"]
                                        )
                                    elif recv["type"] == "noteUpdated":
                                        await hook.functions[recv["body"]["type"]](
                                            recv["body"]
                                        )
                                    else:
                                        await hook.functions[recv["body"]["type"]](
                                            recv["body"]
                                        )
                            except KeyError:
                                pass
                    except (websockets.ConnectionClosedError, Exception):
                        continue
        except Exception as e:
            # warnings.warn(e, exception.WebsocketError)
            print(traceback.format_exc())
            pass