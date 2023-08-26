# StreamingAPIを利用する
misspyでは、streamingAPIを利用することができるメソッドが`misspy.Bot`に実装されています。
## ノートを受信する
ノートを受信するだけなら以下のコードのみで実装できます。
```
import misspy

class StreamingBot(misspy.Bot):

    async def on_ready(self):
        await self.connect("localTimeline")

    async def on_note(self, message):
        print("------------")
        print(message.text)
        print("------------")

bot = StreamingBot("mi.example.com", i="token")
bot.run()
```
## ノートのキャプチャ
misspyではmisskeyの投稿をキャプチャすることができます。
キャプチャは以下のコードで実装することができます。
```
import misspy

class StreamingBot(misspy.Bot):

    async def on_ready(self):
        await self.connect("localTimeline")
        await self.subNote("noteId")

    async def on_reacted():
        print("reaction detected")

bot = StreamingBot("mi.example.com", i="token")
bot.run()
```
また、キャプチャは以下のメソッドで解除することができます。
```
await self.unsubNote("noteId")
```