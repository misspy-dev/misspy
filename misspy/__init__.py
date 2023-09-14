import pkg_resources

from .client import Bot
from .auth import app

from . import http
from . import util
from . import exception
from .hook import hook

__version__ = pkg_resources.get_distribution("misspy").version
