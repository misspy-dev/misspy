import httpx
from attrdictionary import AttrDict

import uuid

from ..core import exception


class MiAuth:
    def __init__(self, address) -> None:
        if not address.startswith("http://") and not address.startswith("https://"):
            self._address: str = "https://" + address
        else:
            self._address: str = address

    def generate_url(
        self,
        name,
        icon=None,
        callback=None,
        permission: list = [
            "read:account",
            "write:account",
            "read:blocks",
            "write:blocks",
            "read:drive",
            "write:drive",
            "read:favorites",
            "write:favorites",
            "read:following",
            "write:following",
            "read:messaging",
            "write:messaging",
            "read:mutes",
            "write:mutes",
            "write:notes",
            "read:notifications",
            "write:notifications",
            "write:reactions",
            "write:votes",
            "read:pages",
            "write:pages",
            "write:page-likes",
            "read:page-likes",
            "write:gallery-likes",
            "read:gallery-likes",
        ],
    ):
        self.session_id = uuid.uuid4()
        if callback is not None:
            callback = f"&callback={callback}"
        else:
            callback = ""
        if icon is not None:
            icon = f"&icon={icon}"
        else:
            icon = ""

        url = f"{self._address}/miauth/{self.session_id}?name={name}{callback}{icon}&permission={','.join(permission)}"
        return url

    def check(self):
        res = httpx.post(f"{self._address}/api/miauth/{self.session_id}/check").json()
        if res.get("token") is not None:
            return AttrDict(res)
        else:
            raise exception.MiAuthFailed(res)
