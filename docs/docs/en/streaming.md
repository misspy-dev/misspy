# Using StreamingAPI
In misspy, the methods that can use streamingAPI are implemented in `misspy.Bot`.

## Receiving notes
If you just want to receive notes, you can implement it with only the following code.
````
import misspy

class StreamingBot(misspy.Bot):.

    async def on_ready(self):
        await self.connect("localTimeline")

    async def on_note(self, message):
        print("------------")
        print(message.text)
        print("------------")

bot = StreamingBot("mi.example.com", i="token")
bot.run()
```
## Capture notes
MISSSPY allows you to capture misskey posts.
Capturing can be implemented with the following code.
```
import misspy

class StreamingBot(misspy.Bot):.

    async def on_ready(self):
        await self.connect("localTimeline")
        await self.subNote("noteId")

    async def on_reacted():
        print("reaction detected")

bot = StreamingBot("mi.example.com", i="token")
bot.run()
````
Captchas can also be deactivated with the following method.
```
await self.unsubNote("noteId")
```