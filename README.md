# misspy
![Supported Python Version](https://img.shields.io/pypi/pyversions/misspy) [![PyPI version](https://badge.fury.io/py/misspy.svg)](https://badge.fury.io/py/misspy) [![PyPI Downloads](https://img.shields.io/pypi/dm/misspy.svg)](https://badge.fury.io/py/misspy) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sonyakun_misspy&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=sonyakun_misspy) [![Upload Python Package](https://github.com/sonyakun/misspy/actions/workflows/publish.yml/badge.svg)](https://github.com/sonyakun/misspy/actions/workflows/publish.yml)

Misskey API library for Python with StreamingAPI support.

# supported software
Misskey forks not listed below are supported only in the latest version **__provided they are API compatible__**.
* [misskey](https://github.com/misskey-dev/misskey)
* [misskey (misskey.io)](https://github.com/misskeyIO/misskey)
* [firefish (calckey)](https://codeberg.org/firefish/firefish) (Some APIs may not be compatible with some APIs due to missing documentation regarding firefish API specifications.)


## supported misskey versions
This library is developed based on the API specification for Misskey v13 or later, so v12 and earlier are not supported (but you may still be able to use this library).


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
from misspy.hook import hook

bot = misspy.Bot("misskey.io", i=token)

async def on_ready():
    bot.connect("localTimeline")
    print("running")

async def on_note(message):
    print("------------")
    print(message.text)
    print("------------")


hook.add("note", on_note)
hook.add("ready", on_ready)
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
https://docs.misspy.xyz/
