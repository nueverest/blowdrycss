# python 2
from __future__ import print_function, unicode_literals
from builtins import str
# builtins
from unittest import TestCase, main
import sys
from io import StringIO
# custom
from blowdrycss.utilities import change_settings_for_testing, unittest_file_path
from blowdrycss.watchdogwrapper import FileEditEventHandler

# required for pycharm unittest feature to work under both python 2.7 and python 3.x
if sys.hexversion < 0x03000000:
    import blowdrycss.blowdrycss_settings as settings
else:
    import blowdrycss_settings as settings

change_settings_for_testing()


class TestFileEditEventHandler(TestCase):
    def test_print_status(self):
        file_types = '(' + ', '.join(settings.file_types) + ')'

        substrings = [
            '-' * 96,
            'The blowdrycss watchdog is watching all ' + str(file_types) + ' files',
            '\nin the project directory: ' + settings.project_directory,
            'Pressing Ctrl + C stops the process.'
        ]

        event_handler = FileEditEventHandler(
                patterns=list(file_types),
                ignore_patterns=[],
                ignore_directories=True
        )

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            event_handler.print_status()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

    def test_excluded_True(self):
        excluded_true = [
            unittest_file_path(folder='test_examplesite', filename='clashing_aliases.html'),
            unittest_file_path(folder='test_examplesite', filename='property_aliases.html'),
        ]
        file_types = '(' + ', '.join(settings.file_types) + ')'
        event_handler = FileEditEventHandler(
                patterns=list(file_types),
                ignore_patterns=[],
                ignore_directories=True
        )
        for excluded in excluded_true:
            self.assertTrue(event_handler.excluded(src_path=excluded))

    def test_excluded_False(self):
        excluded_false = [
            unittest_file_path(folder='test_examplesite', filename='index.html'),
            unittest_file_path(folder='test_examplesite', filename='test.html'),
        ]
        file_types = '(' + ', '.join(settings.file_types) + ')'
        event_handler = FileEditEventHandler(
                patterns=list(file_types),
                ignore_patterns=[],
                ignore_directories=True
        )
        for excluded in excluded_false:
            self.assertFalse(event_handler.excluded(src_path=excluded))

if __name__ == '__main__':
    main()
