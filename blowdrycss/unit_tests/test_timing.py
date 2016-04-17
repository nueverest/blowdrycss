# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
import sys
from datetime import datetime
from time import time
from string import digits
from io import StringIO

# custom
from blowdrycss.timing import Timer

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestTiming(TestCase):
    def test_seconds_to_string(self):
        timer = Timer()
        allowed = set(digits + '.')
        time_string = timer.seconds_to_string(seconds_elapsed=time())
        self.assertTrue(set(time_string) <= allowed)

    def test_elapsed_end_set(self):
        # set(str(float(timer.elapsed)) is required to be compatible with Ubuntu.
        # On windows set(timer.elapsed) is sufficient.
        timer = Timer()
        allowed = set(digits + '.')
        timer.end = time()
        self.assertTrue(set(str(float(timer.elapsed))) <= allowed, msg=str(timer.elapsed) + '\nAllowed: ' + str(allowed))

    def test_elapsed_end_not_set(self):
        # set(str(float(timer.elapsed)) is required to be compatible with Ubuntu.
        # On windows set(timer.elapsed) is sufficient.
        timer = Timer()
        allowed = set(digits + '.')
        self.assertTrue(set(str(float(timer.elapsed))) <= allowed, msg=str(timer.elapsed) + '\nAllowed: ' + str(allowed))

    def test_print_time(self):
        timer = Timer()

        # Checks variable date components and constant string output.
        substrings = [
            'Completed ', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
            str(datetime.now().day)
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            timer.print_time()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring)
        finally:
            sys.stdout = saved_stdout

    def test_report(self):
        timer = Timer()

        # Checks variable date components and constant string output.
        substrings = [
            'Completed ', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
            str(datetime.now().day)
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            timer.report()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()
