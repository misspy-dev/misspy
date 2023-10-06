import json
import requests

import aiohttp
import httpx

from .exception import HTTPException, ClientException, RateLimitError


def request_sync(
    address,
    i=None,
    endpoint="test",
    jobj: dict = {"required": True},
    header: dict = {"Content-Type": "application/json"},
    ssl: bool=True
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
    url = address + "/api/" + endpoint
    if i is not None:
        jobj["i"] = i
    res = requests.post(url, data=json.dumps(jobj, ensure_ascii=False), headers=header, verify=ssl)
    try:
        return res.json()
    except:
        return True


async def request(
    address,
    i=None,
    endpoint="ping",
    jobj: dict = {},
    files=None,
    header={"content-type": "application/json"},
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
    async with aiohttp.ClientSession() as client:
        url = address + "/api/" + endpoint
        if i is not None:
            jobj["i"] = i
        if files is not None:
            async with httpx.AsyncClient() as client:
                if header is not None:
                    res = await client.post(
                        url,
                        data=jobj,
                        files=files,
                        headers=header,
                    )
                else:
                    res = await client.post(url, files=files, data=jobj)
            try:
                resp = res.json()
            except json.JSONDecodeError:
                resp = json.loads(res.text)
        else:
            if header is not None:
                res = await client.post(
                    url, data=json.dumps(jobj, ensure_ascii=False), headers=header
                )
                try:
                    return await res.json()
                except json.JSONDecodeError:
                    return True
            else:
                res = await client.post(url, data=json.dumps(jobj, ensure_ascii=False))
            try:
                resp = await res.json()
            except json.JSONDecodeError:
                resp = json.loads(await res.text)
        if resp.get("error").get("kind") is not None:
            if resp["error"]["code"] == "RATE_LIMIT_EXCEEDED":
                raise RateLimitError("We are being rate limited. Please try again in a few moments.")
            raise ClientException(
                resp["error"]["message"]
                + "\nid: "
                + resp["error"]["id"]
            )
        else:
            print(type(resp))
            return resp

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
    async with aiohttp.ClientSession() as client:
        res = await client.post(
            address + "/api/" + endpoint,
            data=json.dumps(jobj, ensure_ascii=False),
        )
        return res.json()
