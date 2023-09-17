import misspy

class MyMisskeyBot(misspy.Bot):

    async def on_ready(self):
        await self.connect("localTimeline")
        print("ready")

    async def on_note(self, message):
        print(message.user.name)
        print(message.text)
        print("--------------------")

# インスタンス化して実行
bot = MyMisskeyBot("8080-acefed-gitpodmisskey-etifwxfnh5d.ws-us104.gitpod.io", "MVsDf8iQkT6MZIdY3rIgJ2pqRCb0naOr")
bot.run()