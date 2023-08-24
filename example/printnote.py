import misspy
from misspy.ext import MiAuth


class StreamingBot(misspy.Bot):
    async def on_ready(self):
        print("running")

    async def on_note(self, message):
        print("------------")
        print(message.text)
        print("------------")

token = "TOKEN"
bot = StreamingBot("misskey.io", i=token)
bot.run()