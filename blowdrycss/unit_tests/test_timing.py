# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
import sys
from datetime import datetime
from time import time, sleep
from string import digits
from io import StringIO

# custom
from blowdrycss.timing import Timer, LimitTimer
from blowdrycss.utilities import change_settings_for_testing
import blowdrycss_settings as settings

change_settings_for_testing()

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
        allowed = set(digits + '.eE-+')
        timer.end = time()
        self.assertTrue(set(timer.elapsed) <= allowed, msg=str(timer.elapsed) + '\nAllowed: ' + str(allowed))

    def test_elapsed_end_not_set(self):
        # On Ubuntu timer.elapsed is return in scientific notation e.g. '1e-2'
        # On windows timer.elapsed is return in decimal notation e.g. '0.01'
        timer = Timer()
        allowed = set(digits + '.eE-+')
        self.assertTrue(set(timer.elapsed) <= allowed, msg=str(timer.elapsed) + '\nAllowed: ' + str(allowed))

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

    def test_limit_exceeded(self):
        time_limit = settings.time_limit                    # original time limit
        settings.time_limit = 0.0001                        # in seconds
        limit_timer = LimitTimer()
        sleep(0.001)
        self.assertTrue(limit_timer.limit_exceeded, msg=limit_timer.start_time)
        settings.time_limit = time_limit                    # reset time limit

    def test_reset(self):
        limit_timer = LimitTimer()
        start1 = limit_timer.start_time
        sleep(0.001)
        limit_timer.reset()
        start2 = limit_timer.start_time
        self.assertTrue(start1 < start2)


if __name__ == '__main__':
    main()
