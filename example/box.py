import misspy

bot = misspy.Bot("misskey.io")

meta = bot.meta()

print(meta.name)