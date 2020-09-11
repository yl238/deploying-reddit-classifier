import logging

from reddit_classifier.config.base import config
from reddit_classifier.config.base import PACKAGE_ROOT
from reddit_classifier.config import logging_config

VERSION_PATH = PACKAGE_ROOT / 'VERSION'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_config.get_console_handler())
logger.propagate = False

with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()
