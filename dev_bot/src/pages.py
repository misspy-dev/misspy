import random

from sqids import Sqids

from .bot import bot

async def page_create():
    sqids = Sqids(alphabet="FxnXM1kBN6cuhsAvjW3Co7l2RePyY8DwaU04Tzt9fHQrqSVKdpimLGIJOgb5ZE", min_length=16)
    id = sqids.encode([random.randint(0, random.randint(0, 100)), random.randint(0, random.randint(0, 100)), random.randint(0, random.randint(0, 100))]) # "B4aajs"
    await bot.pages_create("test: " + id, "test: " + id, "$[tada " + id + "]")