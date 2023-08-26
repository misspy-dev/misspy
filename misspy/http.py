import json

import httpx

from .exception import HTTPException, ClientException


def request_sync(
    address,
    i=None,
    endpoint="test",
    jobj: dict = {"required": True},
    header: dict = {"Content-Type": "application/json"},
):
    """request_sync (internal function)

    Args:
        address (string): instance address
        i (string): user token
        endpoint (string): endpoint (example: notes/create)
        jobj (dict): request params. Do not include the i.
        header (dict, optional): request header. Defaults to {"Content-Type": "application/json"}.

    Returns:
        dict: request result
    """
    with httpx.Client() as client:
        url = address + "/api/" + endpoint
        if i is not None:
            jobj["i"] = i
        res = client.post(
            url, data=json.dumps(jobj, ensure_ascii=False), headers=header
        )
        return res.json()


async def request(
    address,
    i=None,
    endpoint="test",
    jobj: dict = {"required": True},
    files=None,
):
    """request (internal function)

    Args:
        address (string): instance address
        i (string): user token
        endpoint (string): endpoint (example: notes/create)
        jobj (dict): request params. Do not include the i.

    Returns:
        dict: request result
    """
    async with httpx.AsyncClient() as client:
        url = address + "/api/" + endpoint
        if i is not None:
            jobj["i"] = i
        if files is not None:
            res = await client.post(
                url,
                data=jobj,
                files=files,
            )
            try:
                try:
                    if json.loads(res.text).get("error").get("kind") is not None:
                        raise ClientException(
                            res.json()["error"]["message"]
                            + "\nid: "
                            + res.json()["error"]["id"]
                        )
                    else:
                        return res.json()
                except AttributeError:
                    return json.loads(res.text)
            except json.decoder.JSONDecodeError:
                raise HTTPException(res.status_code)
        else:
            res = await client.post(url, data=json.dumps(jobj, ensure_ascii=False))
            return res.json()


async def request_guest(
    address, endpoint, jobj: dict, header: dict = {"Content-Type": "application/json"}
):
    """request (internal function)

    Args:
        address (string): instance address
        endpoint (string): endpoint (example: notes/create)
        jobj (dict): request params. Do not include the i.
        header (dict, optional): request header. Defaults to {"Content-Type": "application/json"}.

    Returns:
        dict: request result
    """
    async with httpx.AsyncClient() as client:
        res = await client.post(
            address + "/api/" + endpoint,
            data=json.dumps(jobj, ensure_ascii=False),
        )
        return res.json()
