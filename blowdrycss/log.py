""" Basic logging configuration utilities.

Allows logging to std.stdout at the console and logging to a file.

"""

# python 2.7
from __future__ import unicode_literals
# builtins
import logging
import sys
from logging.handlers import RotatingFileHandler
from os import path
# custom
from blowdrycss.utilities import make_directory
import blowdrycss_settings as settings


def enable():
    """ Enable logging in accordance with the settings defined in ``blowdrycss_settings.py``.

    :return: None

    """
    if settings.logging_enabled:
        logger = logging.getLogger('')
        logger.setLevel(settings.logging_level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

        if settings.log_to_console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            logging.debug('Console logging enabled.')

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
            logging.debug('Rotating file logging enabled.')
    else:
        error_message = 'Logging could not be enabled because settings.logging_enabled is False.'
        logging.error(error_message)
        raise ValueError(error_message)
