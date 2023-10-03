import asyncio

from misspy.hook import hook

from src.bot import bot
from src.notes import on_note


async def ready():
    await bot.connect("localTimeline")
    user = await bot.fetch_user("9joplblgsr")
    user.send(text="test")
    print("ready")


hook.add("ready", ready)
hook.add("note", on_note)
bot.run()
