import importlib.metadata

from .client import Bot
from .auth import app

from . import http
from . import util
from .core import exception
from .core import ws
from .core import http
from .hook import hook

__version__ = importlib.metadata.version('misspy') 