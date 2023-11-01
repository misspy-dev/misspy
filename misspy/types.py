from __future__ import annotations
from typing import Any

class poll:
    def __init__(
        self,
        choices: list,
        multiple: bool = False,
        expiresAt: int = None,
        expiredAfter: int = None,
    ):
        self.choices = choices
        self.multiple = multiple
        self.expiresAt = expiresAt
        self.expiredAfter = expiredAfter

class Note:
    
    def __init__(
        self,
        id: str,
        createdAt: str,
        text: str,
        cw: str,
        user: User,
        userId: str,
        visibility: str
    ) -> None:
        self.id = id
        self.createdAt = createdAt
        self.text = text
        self.cw = cw
        self.user = user
        self.userId = userId
        self.visibility = visibility

class User:
    
    def __init__(
        self,
        id: str,
        createdAt: str,
        username: str,
        host: str,
        name: str,
        onlineStatus: str,
        avatarUrl: str,
        avatarBlurhash: str
    ) -> None:
        self.id = id
        self.createdAt = createdAt
        self.username = username
        self.host = host
        self.name = name
        self.onlineStatus = onlineStatus
        self.avatarUrl = avatarUrl
        self.avatarBlurhash = avatarBlurhash

class Drive:
    
    def __init__(
        self,
        capacity: int,
        usage: int
    ) -> None:
        self.capacity = capacity
        self.usage = usage