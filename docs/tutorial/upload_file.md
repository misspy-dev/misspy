# Uploading files
If you want to upload a file to Drive, you can use the code below.

```python
import asyncio

import misspy

bot = misspy.Bot("mi.example.com", i="token")

async def misskeybot():
    with open(f"./file.png", "rb") as f:
        data = await bot.drive.files_create(f)
        print(data.id)
        
    
asyncio.run(misskeybot())
```

## Delete a file 

If you want to delete a file from your drive, drive_files_deleteyou can delete it with .
```python
import asyncio

import misspy

bot = misspy.Bot("mi.example.com", i="token")

async def misskeybot():
    await bot.drive.files_delete("fileId")
    
asyncio.run(misskeybot())
```