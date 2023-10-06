The changelog is only available in Japanese. sorry.

ここには、2023.09.14以降のすべての変更ログが記されています。

# 2023.10.dev1
- ファイルを送信しないhttpリクエストででaiohttpを使うように変更、約78%のパフォーマンス改善([speedups]でインストールした環境の場合)
- websocketでaiohttp.wsを利用するように変更
- 2023.10.dev0でwebsocketのhookが見つからなくなるバグを修正
- [Note](https://misskey-hub.net/docs/api/entity/note.html), [User](https://misskey-hub.net/docs/api/entity/user.html), [Drive]()を実装

# 2023.10.dev0
- コードの大幅変更

# 2023.09.17
- 依存関係にhttpxを追加

# 2023.09.14
- ~~依存ライブラリからhttpxを廃止(代替としてaiohttp、requestsを利用)~~