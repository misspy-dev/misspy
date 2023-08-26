misspyでは、クラスをインスタンス化するためにインスタンスアドレスが必須です。

また、インスタンスアドレスには必要に応じてURLプロコトルを含めることもできます。
```
import misspy

bot = misspy.Bot("mi.example.com")

bot_procotol = misspy.Bot("http://mi.example.com")
```

# トークンを利用する
misspyではnotes_createなどのメソッドを実行する際はトークンが必要です。
これはインスタンス化時に代入することができます。
```
import misspy

bot = misspy.Bot("mi.example.com", i="token")
```

# 投稿する
以下の構文でノートを作成することができます。
また、追加の引数を含めることができます。[これはmisskeyのドキュメントを参照してください。](https://misskey-hub.net/docs/api/endpoints/notes/create.html)
```
import asyncio

import misspy

bot = misspy.Bot("mi.example.com")

async def misskeybot():
    note = await bot.notes_create("Hello, World!")
    print(note.createdNote.id)
    
asyncio.run(misskeybot())
```