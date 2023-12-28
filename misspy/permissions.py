class read:
    account = "read:account"
    blocks = "read:blocks"
    drive = "read:drive"
    favorites = "read:favorites"
    following = "read:following"
    messaging = "read:messaging"
    mutes = "read:mutes"
    notifications = "read:notifications"
    reactions = "read:reactions"
    pages = "read:pages"

    class page:
        likes = "read:page-likes"

    class user:
        groups = "read:user-groups"

    channels = "read:channels"

    class gallery:
        gallery = "read:gallery"
        likes = "read:gallery-likes"

    class flash:
        flash = "read:flash"
        likes = "read:flash-likes"

    class invite:
        codes = "read:invite-codes"

    class clip:
        favorite = "read:clip-favorite"

    federation = "read:federation"


class write:
    account = "write:account"
    blocks = "write:blocks"
    drive = "write:drive"
    favorites = "write:favorites"
    following = "write:following"
    messaging = "write:messaging"
    mutes = "write:mutes"
    notes = "write:notes"

    class invite:
        codes = "write:invite-codes"

    class clip:
        favorite = "write:clip-favorite"

    report = "write:report-abuse"
    notifications = "write:notifications"
    reactions = "write:reactions"
    votes = "write:votes"
    pages = "write:pages"

    class page:
        likes = "write:page-likes"

    class user:
        groups = "write:user-groups"

    channels = "write:channels"

    class gallery:
        gallery = "write:gallery"
        likes = "write:gallery-likes"

    class flash:
        flash = "write:flash"
        likes = "write:flash-likes"


# "read:admin:abuse-user-reports": "ユーザーからの通報を見る"
# "write:admin:delete-account": "ユーザーアカウントを削除する"
# "write:admin:delete-all-files-of-a-user": "ユーザーのすべてのファイルを削除する"
# "read:admin:index-stats": "データベースインデックスに関する情報を見る"
# "read:admin:table-stats": "データベーステーブルに関する情報を見る"
# "read:admin:user-ips": "ユーザーのIPアドレスを見る"
# "read:admin:meta": "インスタンスのメタデータを見る"
# "write:admin:reset-password": "ユーザーのパスワードをリセットする"
# "write:admin:resolve-abuse-user-report": "ユーザーからの通報を解決する"
# "write:admin:send-email": "メールを送る"
# "read:admin:server-info": "サーバーの情報を見る"
# "read:admin:show-moderation-log": "モデレーションログを見る"
# "read:admin:show-user": "ユーザーのプライベートな情報を見る"
# "read:admin:show-users": "ユーザーのプライベートな情報を見る"
# "write:admin:suspend-user": "ユーザーを凍結する"
# "write:admin:unset-user-avatar": "ユーザーのアバターを削除する"
# "write:admin:unset-user-banner": "ユーザーのバーナーを削除する"
# "write:admin:unsuspend-user": "ユーザーの凍結を解除する"
# "write:admin:meta": "インスタンスのメタデータを操作する"
# "write:admin:user-note": "モデレーションノートを操作する"
# "write:admin:roles": "ロールを操作する"
# "read:admin:roles": "ロールを見る"
# "write:admin:relays": "リレーを操作する"
# "read:admin:relays": "リレーを見る"
# "write:admin:invite-codes": "招待コードを操作する"
# "read:admin:invite-codes": "招待コードを見る"
# "write:admin:announcements": "お知らせを操作する"
# "read:admin:announcements": "お知らせを見る"
# "write:admin:avatar-decorations": "アバターデコレーションを操作する"
# "read:admin:avatar-decorations": "アバターデコレーションを見る"
# "write:admin:federation": "連合に関する情報を操作する"
# "write:admin:account": "ユーザーアカウントを操作する"
# "read:admin:account": "ユーザーに関する情報を見る"
# "write:admin:emoji": "絵文字を操作する"
# "read:admin:emoji": "絵文字を見る"
# "write:admin:queue": "ジョブキューを操作する"
# "read:admin:queue": "ジョブキューに関する情報を見る"
# "write:admin:promo": "プロモーションノートを操作する"
# "write:admin:drive": "ユーザーのドライブを操作する"
# "read:admin:drive": "ユーザーのドライブの関する情報を見る"
# "read:admin:stream": "管理者用のWebsocket APIを使う"
# "write:admin:ad": "広告を操作する"
# "read:admin:ad": "広告を見る"

class old:
    "古いバージョンを採用しているサーバー向け (準備中)"