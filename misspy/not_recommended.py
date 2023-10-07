from .http import request_sync


def request_reset_password(instance, username, email):
    return request_sync(
        instance, None, "request-reset-password", {"username": username, "email": email}
    )


def reset_password(instance, i, password):
    return request_sync(
        instance, None, "request-reset-password", {"token": i, "password": password}
    )
