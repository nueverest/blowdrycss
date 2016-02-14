"""
Simple code performance timer that allows for the execution time to be recorded

**Credit:**

- This is a modified version of Paul's and Nicojo's answers on stackoverflow.
- Reference: http://stackoverflow.com/questions/1557571/how-to-get-time-of-a-python-program-execution

**Usage Case:**

>>> # At the beginning of the chunk of code to be timed.
>>> import timing
>>> # Once the program finish execution it will print
>>> # temporal metadata in this form.
Completed @ 2015-12-14 16:56:08.665080
=======================================
It took: 0.17296 seconds
=======================================

"""
# python 2
from __future__ import print_function, division, unicode_literals
from builtins import str
# builtins
from time import time
from datetime import timedelta, datetime

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class Timer(object):
    def __init__(self):
        """

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
        self.start = time()
        self.end = time()

    @staticmethod
    def seconds_to_string(seconds):
        """ Converts the amount of time elapsed to seconds, and returns it as a string.

        :type seconds: float
        :param seconds: ΔT value.
        :return: (*str*) -- Returns a string version of the total time elapsed in seconds.

        """
        return str(timedelta(seconds=seconds).total_seconds())

    @property
    def elapsed(self):
        """ Calculates the amount of time elapsed (ΔT) by subtracting start ``time()`` from end ``time()``.

        **Math:** elapsed = ΔT = end - start

        :return: (*str*) -- Returns ΔT in units of seconds as a string.

        """
        seconds_elapsed = self.end - self.start
        return self.seconds_to_string(seconds=seconds_elapsed)

    def print_time(self):
        """ Prints temporal metadata to the console. Including the completion timestamp and ΔT in seconds.

        :return: None

        **Example**

        >>> # Example Output
        Completed 2015-12-14 16:56:08.665080
        =====================================
        It took: 0.17296 seconds
        =====================================

        """
        completed_at = '\nCompleted ' + str(datetime.now())
        border = '=' * len(completed_at)
        print(str(completed_at))
        print(str(border))
        print('It took: ' + self.elapsed + 'seconds')
        print(str(border))

    def report(self):
        """ Sets ``end`` time and prints the time elapsed (ΔT).

        -
        - Calls ``log()``, so that, the temporal metadata is printed.

        :return: None

        """
        self.end = time()
        self.print_time()
