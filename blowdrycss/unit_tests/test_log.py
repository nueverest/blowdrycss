# python 2.7
from __future__ import absolute_import, unicode_literals, with_statement

# builtins
from unittest import TestCase, main
import sys
from io import StringIO, open
from os import path
import logging

# custom
from blowdrycss.utilities import change_settings_for_testing, unittest_file_path
from blowdrycss import log
import blowdrycss_settings as settings

change_settings_for_testing()


class TestEnable(TestCase):
    def test_enable_logging_log_to_console_enabled(self):
        expected = 'Console logging enabled.\n'
        settings.logging_enabled = True
        settings.log_to_console = True
        settings.log_to_file = False
        settings.logging_level = logging.DEBUG

        saved_stdout = sys.stdout                                                       # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            log.enable()

            output = out.getvalue()

            self.assertTrue(output.endswith(expected), msg=expected + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

    def test_enable_logging_log_to_file_enabled(self):
        settings.logging_enabled = True
        settings.log_to_console = False
        settings.log_to_file = True
        settings.log_directory = unittest_file_path(folder='log')       # Create the log directory inside of unit_tests.
        settings.logging_level = logging.DEBUG
        log_file_path = path.join(settings.log_directory, settings.log_file_name)
        expected = 'Rotating file logging enabled.' + '\nLog file location: ' + log_file_path + '\n'

        if path.isfile(log_file_path):                                                  # Clear log file.
            with open(log_file_path, 'w'):
                pass

        log.enable()

        self.assertTrue(path.isfile(log_file_path), msg=log_file_path)                  # Log file exists.

        with open(log_file_path, 'r') as _file:
            file_as_string = _file.read()

        self.assertTrue(file_as_string.endswith(expected), msg=file_as_string)          # Contents match.

    def test_enable_logging_log_to_console_and_file_enabled(self):
        settings.logging_enabled = True
        settings.log_to_console = True
        settings.log_to_file = True
        settings.logging_level = logging.DEBUG
        settings.log_directory = unittest_file_path(folder='log')       # Create the log directory inside of unit_tests.
        log_file_path = path.join(settings.log_directory, settings.log_file_name)
        expected_console_output = 'Console logging enabled.'
        expected_console_and_file_output = (
            'Rotating file logging enabled.' + '\nLog file location: ' + log_file_path + '\n'
        )

        if path.isfile(log_file_path):                                                  # Clear log file.
            with open(log_file_path, 'w'):
                pass

        saved_stdout = sys.stdout                                                       # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            log.enable()

            output = out.getvalue()

            self.assertTrue(expected_console_output in output, msg=expected_console_output + '\noutput:\n' + output)
            self.assertTrue(
                output.endswith(expected_console_and_file_output),
                msg=expected_console_and_file_output + '\noutput:\n' + output
            )
        finally:
            sys.stdout = saved_stdout

        self.assertTrue(path.isfile(log_file_path), msg=log_file_path)                  # Log file exists.

        with open(log_file_path, 'r') as _file:
            file_as_string = _file.read()

        self.assertTrue(                                                                # Contents match
            file_as_string.endswith(expected_console_and_file_output), msg=file_as_string
        )

    def test_enable_logging_log_to_console_disabled(self):
        settings.logging_enabled = False
        settings.log_to_console = True                                                  # Should produce no effect.
        settings.log_to_file = True                                                     # Should produce no effect.
        expected_console_output = 'Logging disabled because settings.logging_enabled is False.\n'

        saved_stdout = sys.stdout                                                       # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            log.enable()

            output = out.getvalue()

            self.assertTrue(expected_console_output == output, msg=expected_console_output + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout


    def test_logging_level_INFO(self):
        not_expected = 'Console logging enabled.\n'
        info_message = 'Testing 123. This should get logged.'
        settings.logging_enabled = True
        settings.log_to_console = True
        settings.log_to_file = False
        settings.logging_level = logging.INFO

        saved_stdout = sys.stdout                                                       # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            log.enable()
            logging.info(msg=info_message)

            output = out.getvalue()

            self.assertFalse(output.endswith(not_expected), msg=not_expected + '\noutput:\n' + output)
            self.assertTrue(info_message in output, msg=info_message + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()
