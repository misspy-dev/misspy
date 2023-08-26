Misspy requires an instance address to instantiate a class.

Also, the instance address can optionally include the URL protocol.
```
import misspy

bot = misspy.Bot("mi.example.com")

bot_procotol = misspy.Bot("http://mi.example.com")
```

# use the token
misspy requires a token when executing methods such as notes_create. 

It can be assigned at instantiation time.
```
import misspy

bot = misspy.Bot("mi.example.com", i="token")
```

# post
You can create a note with the following syntax. It can also contain additional arguments.

[See the misskey documentation for this. (japanese)](https://misskey-hub.net/docs/api/endpoints/notes/create.html)
```
import asyncio

import misspy

bot = misspy.Bot("mi.example.com")

async def misskeybot():
    note = await bot.notes_create("Hello, World!")
    print(note.createdNote.id)
    
asyncio.run(misskeybot())
```