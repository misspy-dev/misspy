# Upload files to Drive
If you want to upload a file to Drive, you can upload it with the code below.

```
import asyncio

import misspy

bot = misspy.Bot("mi.example.com", i="token")

async def misskeybot():
    with open(f"./file.png", "rb") as f:
        data = await bot.drive_files_create(f)
        print(data.id)
        
    
asyncio.run(misskeybot())
```

## Deleting Files
To delete a file from a drive, you can use `drive_files_delete`.

```
import asyncio

import misspy

bot = misspy.Bot("mi.example.com", i="token")

async def misskeybot():
    await bot.drive_files_delete("fileId")
    
asyncio.run(misskeybot())
```