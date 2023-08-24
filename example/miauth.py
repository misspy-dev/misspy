import webbrowser

from misspy.ext import MiAuth
from misspy.exception import MiAuthFailed

mia = MiAuth("misskey.io")
url = mia.generate_url(input("enter app name: "))
print(url)
input("enter to open with webbrowser...")
webbrowser.open(url)
while True:
    input("enter to continue...")
    try:
        token = mia.check()
        break
    except MiAuthFailed:
        pass
print(token)