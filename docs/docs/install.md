# misspyのインストール
## 前提条件
misspyはPython3.8以降をサポートします。

Python2やPython3.7以前はサポートされていません。
## インストール

!!! 開発版をインストールする場合
    今後のバージョンでリリースされる新機能は、安定版がリリースされるまで開発版をインストールする必要があります。
    ```
    python3 -m pip install -U misspy --pre
    ```
    Windowsを利用している場合:
    ```
    py -3 -m pip install -U misspy --pre
    ```
ライブラリはPyPIから取得できます。
```
python3 -m pip install -U misspy
```
Windowsを利用している場合:
```
py -3 -m pip install -U misspy
```

# 基本概念
misspyはAPIリクエストをメソッドで送信する仕組みです。

少なくともインスタンスアドレスを指定するだけでmisspyの利用を開始することができます。

misspyで返されるものは基本的に辞書型ではなく、javascriptのドット記法のような方法で値を取得することができます。
```
import misspy

bot = misspy.Bot("mi.example.com")

meta = bot.meta()

print(meta.name)
```