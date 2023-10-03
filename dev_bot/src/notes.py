import asyncio

from .bot import bot
from .pages import page_create

async def on_note(ctx):
    if ctx.user.isBot:
        return
    if ctx.text == "test":
        await bot.reactions_create(ctx.id, "👍")
        with open("./assets/test.png", "rb") as f:
            file = await bot.drive_files_create(f)
            print("uploaded. ")
            await bot.notes_create("test")
            print("noted. ")
            await bot.notes_create("test", replyid=ctx.id, fileid=[file.id])
            print("replyed. ")
            await bot.notes_create(renoteId=ctx.id)
            print("renoted. ")
            #await asyncio.sleep(10)
            #await bot.drive_files_delete(file.id)
            #print("deleted.")
            await page_create()
            print("page created. ")