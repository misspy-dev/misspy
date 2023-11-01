# Quickstart

## install
### Prerequisites 
misspy supports Python3.8 and later.

Python2 and Python3.7 and earlier are not supported.
### Installation 
Other:
```
python3 -m pip install -U misspy
```
Windows:
```
py -3 -m pip install -U misspy
```

Additional components can be installed to speed up the process.
Other:
```
python3 -m pip install -U misspy[speedups]
```
Windows:
```
py -3 -m pip install -U misspy[speedups]
```
### Basic concepts 
misspy is a mechanism for sending API requests using methods.

At least you can start using misspy by specifying the instance address.

What is returned by misspy is basically not a dictionary type, and you can get the value using a method similar to JavaScript's dot notation.

```python
import misspy

bot = misspy.Bot("mi.example.com")

meta = bot.meta()

print(meta.name)
```

misspy requires an instance address to instantiate a class.


The instance address can also optionally include a URL protocol.
```python
import misspy

bot = misspy.Bot("mi.example.com")

bot_procotol = misspy.Bot("http://mi.example.com")
```
# Use tokens 
misspy requires a token when executing methods such as notes.create. This can be assigned at instantiation time.

```python
import misspy

bot = misspy.Bot("mi.example.com", i="token")
```
# Post
You can create a note using the following syntax. It can also include [additional arguments](../reference/notes/#misspynotes).
```python
import asyncio

import misspy

bot = misspy.Bot("mi.example.com")

async def misskeybot():
    note = await bot.notes.create("Hello, World!")
    print(note.createdNote.id)
    
asyncio.run(misskeybot())
```