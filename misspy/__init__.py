import pkg_resources

from .client import Bot
from .auth import app

from . import http
from . import util
from . import exception
from .hook import hook

try:
    __version__ = pkg_resources.get_distribution("misspy").version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0.ldev"
