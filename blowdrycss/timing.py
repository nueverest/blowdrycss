"""
Simple code performance timer that allows for the execution time to be recorded

**Credit:**

- This is a modified version of Paul's and Nicojo's answers on stackoverflow.
- Reference: http://stackoverflow.com/questions/1557571/how-to-get-time-of-a-python-program-execution

**Usage Case:**

>>> # At the beginning of the chunk of code to be timed.
>>> from blowdrycss.timing import Timer
>>> timer = Timer()
>>> timer.report()
Completed @ 2015-12-14 16:56:08.665080
=======================================
It took: 0.17296 seconds
=======================================

"""
# python 2
from __future__ import absolute_import, print_function, division, unicode_literals
from builtins import str

# builtins
from time import time
from datetime import timedelta, datetime
from os import path

# custom
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class Timer(object):
    """ A performance Timer that reports the amount of time it took to run a block of code.

    :return: None

    **Example**

    >>> from blowdrycss.timing import Timer
    >>> timer = Timer()
    >>> timer.report()
    Completed 2015-12-14 16:56:08.665080
    =====================================
    It took: 0.17296 seconds
    =====================================
    >>> timer.reset()       # Resets start time to now.
    >>> timer.report()
    Completed 2015-12-14 17:05:12.164030
    =====================================
    It took: 1.45249 seconds
    =====================================

    """
    def __init__(self):
        self.start = time()
        self.end = time()

    @staticmethod
    def seconds_to_string(seconds_elapsed=0.00):
        """ Converts the amount of time elapsed to seconds_elapsed, and returns it as a string.

        :type seconds_elapsed: float
        :param seconds_elapsed: A time() value in units of seconds_elapsed.
        :return: (*str*) -- Returns a string version of the total time elapsed in seconds_elapsed.

        """
        return str(timedelta(seconds=seconds_elapsed).total_seconds())

    @property
    def elapsed(self):
        """ Calculates the amount of time elapsed (delta T) by subtracting start ``time()`` from end ``time()``.

        **Math:** elapsed = delta T = end - start

        :return: (*str*) -- Returns delta T in units of seconds as a string.

        """
        seconds_elapsed = self.end - self.start
        return self.seconds_to_string(seconds_elapsed=seconds_elapsed)

    def print_time(self):
        """ Prints temporal metadata to the console. Including the completion timestamp and delta T in seconds.

        :return: None

        """
        completed_at = '\nCompleted ' + str(datetime.now())
        border = '=' * len(completed_at)
        print(str(completed_at))
        print(str(border))
        print('It took: ' + self.elapsed + 'seconds')
        print(str(border))

    def report(self):
        """ Sets ``end`` time and prints the time elapsed (delta T).  Calls ``print_time()``, and prints temporal metadata.

        :return: None

        """
        self.end = time()
        self.print_time()


class LimitTimer(object):
    """ Timer governs when to perform a full and comprehensive run of blowdrycss.main().

    .. note::   This is independent of file modification watchdog triggers which only scan the file(s) that changed
        since the last run.

    :return: None

    **Example**

    >>> from blowdrycss.timing import LimitTimer
    >>> limit_timer = LimitTimer()
    >>> if limit_timer.limit_exceeded:
    >>>     print("30 minutes elapses.")
    >>>     limit_timer.reset()
    """
    def __init__(self):
        self.start = time()
        self.time_limit = settings.time_limit

    @property
    def limit_exceeded(self):
        """ Compares the current time to the start time, and returns True if ``self.time_limit``
        is exceeded and False otherwise.

        :return: (*bool*) -- Returns True if ``self.time_limit`` is exceeded and False otherwise.

        """
        return time() - self.start >= self.time_limit

    def reset(self):
        """ Resets ``self.start`` to the current time.

        :return: None

        """
        self.start = time()
