""" Basic logging configuration utilities.

Allows logging to std.stdout at the console and logging to a file.

"""

# python 2.7
from __future__ import absolute_import, unicode_literals, print_function

# builtins
import logging
import sys
from logging.handlers import RotatingFileHandler
from os import path

# custom
from blowdrycss.utilities import make_directory
import blowdrycss_settings as settings


try:                                            # Python 2.7+ log.py
    from logging import NullHandler
except ImportError:                             # Python 3.3+ log.py
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


def enable():
    """ Enable logging in accordance with the settings defined in ``blowdrycss_settings.py``.

    :return: None

    """
    if settings.logging_enabled:
        logger = logging.getLogger('')
        logger.setLevel(settings.logging_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        if settings.log_to_console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            logging.info('Console logging enabled.')
        # else:
        #     logger.propagate = False        # Prevent printing to stderr.

        if settings.log_to_file:
            make_directory(directory=settings.log_directory)
            log_file_path = path.join(settings.log_directory, settings.log_file_name)
            rotating_file_handler = RotatingFileHandler(
                filename=log_file_path,
                maxBytes=settings.log_file_size,
                backupCount=settings.log_backup_count
            )
            rotating_file_handler.setFormatter(formatter)
            logger.addHandler(rotating_file_handler)
            logging.info('Rotating file logging enabled.' + '\nLog file location: ' + log_file_path)
    else:
        print('Logging disabled because settings.logging_enabled is False.')
