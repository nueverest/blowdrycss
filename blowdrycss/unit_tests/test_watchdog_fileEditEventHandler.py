# python 2
from __future__ import absolute_import, print_function, with_statement, unicode_literals
from builtins import str

# builtins
from unittest import TestCase, main
from os import path, remove, SEEK_END
import logging
import sys
from io import StringIO, open
from time import sleep

# plugins
from watchdog.observers import Observer

# custom
from blowdrycss.utilities import change_settings_for_testing, unittest_file_path, make_directory
from blowdrycss.watchdogwrapper import FileEditEventHandler
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
            unittest_file_path(folder=str('test_examplesite'), filename=str('clashing_aliases.html')),
            unittest_file_path(folder=str('test_examplesite'), filename=str('property_aliases.html')),
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

    def test_on_modified(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        original_file = ''
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
            'The blowdrycss watchdog is watching all (*.html) files',
            '-' * 96,
        ]
        html_text = '<html></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        modify_dot_html = unittest_file_path(folder='test_examplesite', filename='modify.html')
        file_types = '(' + ', '.join(settings.file_types) + ')'

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        self.assertTrue(path.isdir(test_examplesite))

        # Add contents to modify.html
        with open(modify_dot_html, 'w', encoding='utf-8') as _file:
            _file.write(html_text)

        event_handler = FileEditEventHandler(
            patterns=list(file_types),
            ignore_patterns=[],
            ignore_directories=True
        )

        observer = Observer()
        observer.schedule(event_handler, unittest_file_path(folder='test_examplesite'), recursive=True)
        observer.start()

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            # Modify remove one character (triggers on_modified).
            with open(modify_dot_html, 'rb+') as _file:
                _file.seek(-1, SEEK_END)
                _file.truncate()

            sleep(0.25)     # IMPORTANT: Must wait for output otherwise test will fail.

            output = out.getvalue()

            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

        # Delete contents of modify.html.
        with open(modify_dot_html, 'w'):
            pass

        observer.stop()
        observer.join()

    def test_on_deleted(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
            'The blowdrycss watchdog is watching all (*.html) files',
            '-' * 96,
        ]
        html_text = '<html></html>'
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')
        file_types = '(' + ', '.join(settings.file_types) + ')'

        event_handler = FileEditEventHandler(
            patterns=list(file_types),
            ignore_patterns=[],
            ignore_directories=True
        )

        # Create delete.html
        with open(delete_dot_html, 'w', encoding='utf-8') as _file:
            _file.write(html_text)

        self.assertTrue(path.isfile(delete_dot_html))

        observer = Observer()
        observer.schedule(event_handler, unittest_file_path(folder='test_examplesite'), recursive=True)
        observer.start()

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            remove(delete_dot_html)     # Delete delete.html

            sleep(0.25)                 # IMPORTANT: Must wait for output otherwise test will fail.

            output = out.getvalue()

            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()
