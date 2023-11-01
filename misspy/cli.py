import threading
import time
import sys
import subprocess
import os
import logging
import ctypes

from colorama import Fore, Back, Style
import fire
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class Live_Bot(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        self._target(*self.args, **self.kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread_id), ctypes.py_object(SystemExit)
        )
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            print("Failure in raising exception")


def start():
    subprocess.run("python main.py", shell=True)


class LEH(LoggingEventHandler):
    def on_created(self, event):
        lb.raise_exception()
        lb.start()

    def on_deleted(self, event):
        lb.raise_exception()
        lb.start()


class progress:
    def __init__(self):
        self.work_ended = False

    def anim(self):
        while not self.work_ended:
            sys.stdout.write("\b" + "|")
            sys.stdout.flush()
            time.sleep(0.12)
            sys.stdout.write("\b" + "/")
            sys.stdout.flush()
            time.sleep(0.12)
            sys.stdout.write("\b" + "-")
            sys.stdout.flush()
            time.sleep(0.12)
            sys.stdout.write("\b" + "\\")
            sys.stdout.flush()
            time.sleep(0.12)
        sys.stdout.write("\b" + " ")
        sys.stdout.flush()

    def multithread_processing(self, text, targ, tp, name, fast):
        prg.work_ended = False
        print(text + ":  ", end="")
        t1 = threading.Thread(target=self.anim)
        t2 = threading.Thread(
            target=targ,
            args=(
                tp,
                name,
                fast,
            ),
        )
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        sys.stdout.write("\b" + "done\n")
        sys.stdout.flush()


prg = progress()
lb = Live_Bot(target=start)


def cmd(tp, name, fast):
    if tp == "1":
        subprocess.run(f"python -m venv .venv", shell=True, stdout=subprocess.DEVNULL)
    if tp == "2":
        if fast:
            subprocess.run(
                "pip install misspy[speedups]", shell=True, stdout=subprocess.DEVNULL
            )
        else:
            subprocess.run("pip install misspy", shell=True, stdout=subprocess.DEVNULL)
    if tp == "3":
        with open("main.py", "w") as f:
            text = [
                "import misspy\n",
                "from misspy.hook import hook\n",
                "\n",
                'token = ""\n',
                'bot = misspy.Bot("", i=token)\n',
                "\n",
                "async def on_ready():\n",
                '   bot.connect("localTimeline")\n',
                '   await bot.notes.create("Hello, World!")\n',
                "\n",
                "async def on_note(message):\n",
                '   print("------------")\n',
                "   print(message.text)\n",
                '   print("------------")\n',
                "\n",
                'hook.add("note", on_note)\n',
                'hook.add("ready", on_ready)\n',
                "bot.run()\n",
            ]
            f.writelines(text)
    prg.work_ended = True


def create(name, fast=False):
    if os.path.isdir(".venv"):
        va = input("venv already exists. Do you want to overwrite it? (n): ")
        if va == "y":
            pass
        else:
            sys.exit()
    if os.path.exists("./main.py"):
        va = input("main.py already exists. Do you want to overwrite it? (n): ")
        if va == "y":
            pass
        else:
            sys.exit()
    prg.multithread_processing("creating a venv", cmd, "1", name, fast)
    prg.multithread_processing("installing misspy", cmd, "2", name, fast)
    prg.multithread_processing("creating files", cmd, "3", name, fast)
    print("\n✨ Done!")


def run(path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    event_handler = LEH()
    observer = Observer()  # 監視オブジェクト生成
    observer.schedule(event_handler, path, recursive=True)  # 監視設定
    observer.start()  # 監視開始
    try:
        while True:  # ctrl-Cが押されるまで実行
            time.sleep(1)  # 1秒停止
    except KeyboardInterrupt:  # ctrl-C実行時
        observer.stop()  # 監視修了
        lb.raise_exception()
    observer.join()


def main():
    fire.Fire({"create": create, "run": run})
