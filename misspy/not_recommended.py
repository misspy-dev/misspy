from .http import request_guest, request

async def request_reset_password(instance, username, email):
    return await request_guest(instance, "request-reset-password", {"username": username, "email": email})

async def reset_password(instance, i, password):
    return await request_guest(instance, "request-reset-password", {"token": i, "password": password})
