import uuid
import urllib.parse

import httpx
from attrdictionary import AttrDict

from ..core import exception


class MiAuth:
    """MiAuth extension.
    """
    def __init__(self, address) -> None:
        if not address.startswith("http://") and not address.startswith("https://"):
            self._address: str = "https://" + address
        else:
            self._address: str = address

    def generate_url(
        self,
        name,
        icon=None,
        callback: str=None,
        permission: list = [],
    ):
        """generate MiAuth URL.

        Args:
            name (str): Application name.
            icon (str, optional): Application icon url. Defaults to None.
            callback (str, optional): Application callback url. Defaults to None.
            permission (list | None, optional): Application Permission.

        Returns:
            str: MiAuth url.
        """
        self.session_id = uuid.uuid4()
        if callback is not None:
            callback = f"&callback={callback}"
        else:
            callback = ""
        if icon is not None:
            icon = f"&icon={icon}"
        else:
            icon = ""

        url = f"{self._address}/miauth/{self.session_id}?name={urllib.parse.quote(name)}{urllib.parse.quote(callback)}{icon}&permission={','.join(permission)}"
        return url

    def check(self):
        """If authenticated, AttrDict is returned.

        Raises:
            exception.MiAuthFailed: If not authenticated.

        Returns:
            AttrDict: MiAuth result.
        """
        res = httpx.post(f"{self._address}/api/miauth/{self.session_id}/check").json()
        if res.get("token") is not None:
            return AttrDict(res)
        else:
            raise exception.MiAuthFailed(res)
