import asyncio
from functools import partial
import re
import traceback

import websockets
from attrdictionary import AttrDict

try:
    import orjson as json
except ModuleNotFoundError:
    import json

from .hook import cmdHook
from ... import exception

from ...reaction import reactions
from ...notes import notes
from ...user import following


class MiWS:
    def __init__(self, address, i, ssl=True, ui={}) -> None:
        self.i = i
        self.address_ws = address
        self.ssl = ssl
        self.ui = ui
        self.parser = MiCMD(address, i, ui, ssl)

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

        self.reactions = reactions(self.address, self.i, self.ssl)
        self.notes = notes(self.address, self.i, self.ssl)
        self.following = following(self.address, self.i, self.ssl)

    async def ws_handler(self):
        try:
            procotol = "ws://"
            if self.ssl:
                procotol = "wss://"
                async for self.connection in websockets.connect(
                    f"{procotol}{self.address_ws}/streaming?i={self.i}"
                ):
                    try:
                        try:
                            await cmdHook.functions["ready"]()
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
                                        parsed = await self.parser.command_parse(
                                            recv["body"]["body"]
                                        )
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
                                        if parsed["hookname"] is None:
                                            await cmdHook.functions[
                                                recv["body"]["type"]
                                            ](recv["body"]["body"])
                                        elif parsed["args"] is None:
                                            await cmdHook.functions[parsed["hookname"]](
                                                AttrDict(ctx)
                                            )
                                        elif (
                                            parsed["args"] is not None
                                            and parsed["hookname"] is not None
                                        ):
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
                                            print("ctx setted")
                                            await cmdHook.functions[parsed["hookname"]](
                                                AttrDict(ctx), *parsed["args"]
                                            )
                                        else:
                                            await cmdHook.functions[
                                                recv["body"]["body"]["type"]
                                            ](recv["body"]["body"])
                                    elif recv["body"]["type"] == "notification":
                                        await cmdHook.functions[
                                            recv["body"]["body"]["type"]
                                        ](recv["body"]["body"])
                                    elif recv["body"]["type"] == "follow":
                                        await cmdHook.functions[recv["body"]["type"]](
                                            recv["body"]["body"]
                                        )
                                    elif recv["body"]["type"] == "followed":
                                        await cmdHook.functions[recv["body"]["type"]](
                                            recv["body"]["body"]
                                        )
                                    elif recv["type"] == "noteUpdated":
                                        await cmdHook.functions[recv["body"]["type"]](
                                            recv["body"]
                                        )
                                    else:
                                        await cmdHook.functions[recv["body"]["type"]](
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


class MiCMD:
    def __init__(
        self,
        address,
        i,
        ui,
        ssl=True,
    ) -> None:
        self.i = i
        self.address = address
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

        self.ui = ui

    async def command_parse(self, note):
        if self.ui["id"] in note["mentions"]:
            parsed = re.findall(r'(?:"[^"]*"|\S)+', note["text"])
            if len(parsed) == 1:
                return {"hookname": "cmd_" + parsed[0].replace("@", ""), "args": None}
            else:
                parsed.pop(0)
                p0 = parsed[0]
                parsed.pop(0)
                return {"hookname": "cmd_" + p0, "args": parsed}
        else:
            return {"hookname": None}
