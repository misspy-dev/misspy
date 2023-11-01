# Using StreamingAPI 
`misspy.Bot` misspy implements methods that can use the streaming API.

## Receive notes 
If you just want to receive notes, you can implement it using only the code below.

```python
import misspy
from misspy import hook

async def on_ready():
    await bot.connect("localTimeline")

async def on_note(,message):
    print("------------")
    print(message.text)
    print("------------")

bot = misspy.Bot("mi.example.com", i="token")
hook.add("ready", on_ready)
hook.add("notes", on_note)
bot.run()
```

## Capturing notes 
misspy allows you to capture misskey's posts. Capture can be implemented with the code below.

```python
import misspy

async def on_ready():
    await bot.connect("localTimeline")
    await bot.subNote("noteId")

async def on_reacted():
    print("reaction detected")

bot = misspy.Bot("mi.example.com", i="token")
hook.add("ready", on_ready)
hook.add("reacted", on_reacted)
bot.run()
```

In addition, capture can be canceled using the following method.

```python
await bot.unsubNote("noteId")
```