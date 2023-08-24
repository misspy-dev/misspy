import json

import httpx

async def request(address, i, endpoint, jobj: dict, header: dict={"Content-Type": "application/json"}):
    """request (internal function)

    Args:
        address (string): instance address
        i (string): user token
        endpoint (string): endpoint (example: notes/create)
        jobj (dict): request params. Do not include the i.
        header (dict, optional): request header. Defaults to {"Content-Type": "application/json"}.

    Returns:
        dict: request result
    """
    async with httpx.AsyncClient() as client:
        jobj["i"] = i
        res = await client.post(
            address + "/api/" + endpoint, json=json.dumps(jobj, ensure_ascii=False), headers=json.dumps(header, ensure_ascii=False)
        )
        return res.json()
    
async def request_guest(address, endpoint, jobj: dict, header: dict={"Content-Type": "application/json"}):
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
            address + "/api/" + endpoint, json=json.dumps(jobj, ensure_ascii=False), headers=json.dumps(header, ensure_ascii=False)
        )
        return res.json()