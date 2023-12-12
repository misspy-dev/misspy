# misspy
![Supported Python Version](https://img.shields.io/pypi/pyversions/misspy?style=flat-square) [![PyPI version](https://badge.fury.io/py/misspy.svg?style=flat-square)](https://badge.fury.io/py/misspy) [![PyPI Downloads](https://img.shields.io/pypi/dm/misspy.svg?style=flat-square)](https://badge.fury.io/py/misspy) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black) 
[![Misskey-API](https://img.shields.io/badge/Misskey-555555.svg?logo=Misskey&style=flat-square)](https://misskey-hub.net)

Misskey API library for Python with StreamingAPI support.

# supported software
Misskey forks not listed below are supported only in the latest version **__provided they are API compatible__**.
* [misskey](https://github.com/misskey-dev/misskey)
* [misskey (misskey.io)](https://github.com/misskeyIO/misskey)
* [firefish (calckey)](https://codeberg.org/firefish/firefish) (Some APIs may not be compatible with some APIs due to missing documentation regarding firefish API specifications.)

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

bot = commands.Bot("misskey.example", "token")

async def on_ready():
    print("loggedin: ")
    print("id: "+ bot.id)
    print("name: "+ bot.name)
    print("username: "+ bot.username)
    await bot.connect(misspy.localTimeline) # supported args: misspy.homeTimeline, misspy.localTimeline, misspy.socialTimeline or misspy.hybridTimeline, misspy.globalTimeline and Conventional Method


async def on_note(ctx, message):
    if message["text"] == "test":
        await ctx.add_reaction(":test:")
    print("------------")
    print(message)
    print("------------")

bot.add_hook("ready", on_ready)
bot.add_hook("note", on_note)

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

# Other

## docs
Documentation can be found at:
https://docs.misspy.xyz/

## supported python version
|                          | below 3.7 | 3.8 ~ 3.11          | 3.12             | 
| ------------------------ | --------- | ------------------- | ---------------- | 
| supported                | ❌        | ⭕                  | ❌ (Beta)        | 
| supported misspy version | ❌        | 2023.8.24rc1~latest | 2023.11.0-beta.1 | 

## supported misskey versions
This library is developed based on the API specification for Misskey v13 or later, so v12 and earlier are not supported (but you may still be able to use this library).