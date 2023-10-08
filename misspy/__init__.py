import pkg_resources

from .client import Bot
from .auth import app

from . import http
from . import util
from .core import exception
try:
    from misspy_core_fast import ws
    from misspy_core_fast import http
except ModuleNotFoundError:
    from .core import ws
    from .core import http
from .hook import hook

__version__ = pkg_resources.get_distribution("misspy").version
