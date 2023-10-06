import datetime
import logging
import sys

LOG_COLORS = {
    logging.DEBUG: "\033[94m",
    logging.INFO: "\033[36m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[95m",
}
enablelog = True


class ColoredStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            self.stream.write(LOG_COLORS[record.levelno])
            super().emit(record)
        finally:
            self.stream.write("\033[0m")



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dt = datetime.datetime.now()
formatter = logging.Formatter(
    "[{}] %(levelname)s %(message)s".format(dt.strftime("%H:%M:%S"))
)
handler = ColoredStreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)