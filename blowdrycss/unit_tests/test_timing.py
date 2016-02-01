from unittest import TestCase, main
import sys
from datetime import datetime
from time import time
from string import digits
from io import StringIO
# custom
import timing
import unittest_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestTiming(TestCase):
    def test_seconds_to_string(self):
        allowed = set(digits + '.')
        time_string = timing.seconds_to_string(elapsed=time())
        self.assertTrue(set(time_string) <= allowed)

    def test_log(self):
        # Checks variable date components and constant string output.
        time_string = timing.seconds_to_string(elapsed=time())
        substrings = [
            'Completed @', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
            str(datetime.now().day)
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            timing.log(elapsed=time_string)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring)
        finally:
            sys.stdout = saved_stdout

    def test_end_log(self):
        # Checks variable date components and constant string output.
        substrings = [
            'Completed @', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
            str(datetime.now().day)
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            timing.end_log()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()
