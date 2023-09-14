# misspy
Misskey API library for Python with StreamingAPI support.

# example
**Other examples can be found in the examples directory.**

## send note
```python
import misspy

mi = misspy.Bot(address, i=token)
```

## Output notes text to the console
```python
import misspy
from misspy.ext import MiAuth


class StreamingBot(misspy.Bot):
    async def on_ready(self):
        print("running")

    async def on_note(self, message):
        print("------------")
        print(message.text)
        print("------------")


bot = StreamingBot("misskey.io", i=token)
bot.run()
```

## MiAuth
```python
from misspy.ext import MiAuth

mia = MiAuth("misskey.io")
print(mia.generate_url("example app"))
while True:
    input("enter to continue...")
    try:
        token = mia.check()
        break
    except misspy.MiAuthFailed:
        pass
print(token)
```


# docs
Documentation can be found at:
https://misspy.sonyakun.com/docs
