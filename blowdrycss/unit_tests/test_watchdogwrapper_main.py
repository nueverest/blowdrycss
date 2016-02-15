# python 2
from __future__ import print_function, unicode_literals, with_statement
# builtins
from unittest import TestCase, main
import logging
import sys
from io import StringIO, open
from time import sleep
from os import path, remove
# plugins
from blowdrycss.utilities import unittest_file_path, change_settings_for_testing
from blowdrycss import watchdogwrapper

# required for pycharm unittest feature to work under both python 2.7 and python 3.x
if sys.hexversion < 0x03000000:
    import blowdrycss.blowdrycss_settings as settings
else:
    import blowdrycss_settings as settings

change_settings_for_testing()


class TestWatchdogWrapperMain(TestCase):
    # Unable to test this at present as main() is in a process of its' own.
    # Need something like this http://stackoverflow.com/questions/7602120/sending-keyboard-interrupt-programmatically

    # def test_main_auto_generate_True(self):
    #     # Integration test
    #     logging.basicConfig(level=logging.DEBUG)
    #     substrings = [
    #         '~~~ blowdrycss started ~~~',
    #         'File Types: *.html',
    #         'Project Directory:',
    #         'Auto-Generated CSS',
    #         'Completed',
    #         'blowdry.css',
    #         'blowdry.min.css',
    #     ]
    #     html_text = '<html></html>'
    #     delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')
    #
    #     # Create delete.html
    #     with open(delete_dot_html, 'w') as _file:
    #         _file.write(html_text)
    #
    #     self.assertTrue(path.isfile(delete_dot_html))
    #
    #     saved_stdout = sys.stdout
    #     try:
    #         out = StringIO()
    #         sys.stdout = out
    #
    #         settings.auto_generate = True
    #         watchdogwrapper.main()
    #
    #         remove(delete_dot_html)     # Delete delete.html
    #
    #         sleep(0.25)                 # IMPORTANT: Must wait for output otherwise test will fail.
    #
    #         output = out.getvalue()
    #
    #         for substring in substrings:
    #             self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
    #     finally:
    #         sys.stdout = saved_stdout

    def test_main_auto_generate_False(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        substrings = [
            '~~~ blowdrycss started ~~~',
            'File Types: *.html',
            'Project Directory:',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
        ]
        html_text = '<html></html>'
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')

        # Create delete.html
        with open(delete_dot_html, 'w') as _file:
            _file.write(html_text)

        self.assertTrue(path.isfile(delete_dot_html))

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            settings.auto_generate = False
            watchdogwrapper.main()

            remove(delete_dot_html)     # Delete delete.html

            sleep(0.25)                 # IMPORTANT: Must wait for output otherwise test will fail.

            output = out.getvalue()

            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()

