# ドライブにファイルをアップロードする
ドライブにファイルをアップロードする場合、以下のコードでアップロードすることができます。
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

## ファイルを削除する
ドライブからファイルを削除する場合、`drive_files_delete`で削除することができます。
```
import asyncio

import misspy

bot = misspy.Bot("mi.example.com", i="token")

async def misskeybot():
    await bot.drive_files_delete("fileId")
    
asyncio.run(misskeybot())
```