import os
from os.path import join, dirname

import misspy
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join("../.env")
load_dotenv(dotenv_path)

bot = misspy.Bot("localhost:3000", os.environ.get("MISSKEY_TOKEN"), ssl=False)
