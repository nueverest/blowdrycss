# python 2
from __future__ import absolute_import, print_function, unicode_literals, with_statement
import _thread

# builtins
from unittest import TestCase, main
import logging
import sys
from io import StringIO, open
from time import sleep
from os import path, remove

# plugins
from blowdrycss.utilities import unittest_file_path, change_settings_for_testing, make_directory
from blowdrycss import watchdogwrapper
import blowdrycss_settings as settings

change_settings_for_testing()


class TestWatchdogWrapperMain(TestCase):
    passing = True
    non_matching = ''
    output = ''

    def monitor_delete_stop(self, file_path_to_delete):
        """ Monitor console output. Delete file at file_path_to_delete. Stop watchdogwrapper.main()
        Reference: http://stackoverflow.com/questions/7602120/sending-keyboard-interrupt-programmatically

        """
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
        ]
        html_text = '<html></html>'

        saved_stdout = sys.stdout           # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            # Wait for main() to start.
            while 'Ctrl + C' not in out.getvalue():
                sleep(0.05)

            # Delete the file.
            remove(file_path_to_delete)

            # IMPORTANT: Must wait for output otherwise test will fail.  0.25
            count = 0
            while substrings[-1] not in out.getvalue():
                if count > 100:             # Max wait is 5 seconds = 100 count * 0.05 sleep
                    break
                else:
                    sleep(0.05)
                    count += 1

            output = out.getvalue()

            for substring in substrings:
                if substring not in output:
                    self.passing = False
                    self.non_matching = substring
                    self.output = output
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout
            _thread.interrupt_main()        # Stop watchdogwrapper.main().

    def test_main_auto_generate_True(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        html_text = '<html></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        self.assertTrue(path.isdir(test_examplesite))

        # Create file delete.html
        with open(delete_dot_html, 'w') as _file:
            _file.write(html_text)

        # Double check to ensure it got created.
        self.assertTrue(path.isfile(delete_dot_html))

        auto_generate = settings.auto_generate          # original
        settings.auto_generate = True
        _thread.start_new_thread(self.monitor_delete_stop, (delete_dot_html,))
        watchdogwrapper.main()    # Caution: Nothing will run after this line unless _thread.interrupt_main() is called.
        self.assertTrue(self.passing, msg=self.non_matching + ' not found in output:\n' + self.output)
        settings.auto_generate = auto_generate          # reset setting

    def test_main_auto_generate_False(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
        ]
        html_text = '<html></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')
        auto_generate = settings.auto_generate          # original

        # Directory must be created for Travis CI case
        if not path.isdir(test_examplesite):
            make_directory(test_examplesite)

        self.assertTrue(path.isdir(test_examplesite))

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
            settings.auto_generate = auto_generate          # reset setting


if __name__ == '__main__':
    main()

