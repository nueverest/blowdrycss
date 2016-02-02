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
import atexit
from time import time
from datetime import timedelta, datetime
# from utilities import print_blow_dryer
# custom
# from blowdrycss_settings import minify
# from utilities import print_css_stats

__author__ = 'paul, nicojo, chad nelson'
__project__ = 'blowdrycss'


def seconds_to_string(elapsed):
    """ Converts the amount of time elapsed to seconds, and returns it as a string.

    :type elapsed: float
    :param elapsed: A time delta value.
    :return: (str) -- Returns a string version of the total time elapsed in seconds.

    """
    return str(timedelta(seconds=elapsed).total_seconds())


def log(elapsed=None):
    """ Prints the temporal metadata to the console.

    :type elapsed: str
    :param elapsed: A string containing the number of seconds elapsed after the ``import timing`` statement
        was declared.
    :return: None

    >>> # Example Output
    Completed @ 2015-12-14 16:56:08.665080
    =======================================
    It took: 0.17296 seconds
    =======================================

    """
    completed_at = '\nCompleted @ ' + str(datetime.now())
    border = '=' * len(completed_at)
    print(str(completed_at))
    print(str(border))
    if elapsed:
        print('It took: ' + str(elapsed) + 'seconds')
    # if minify:
    #     print_css_stats(file_name='blowdry')
    print(str(border))
    # print_blow_dryer()


def end_log():
    """
    - Calculates the amount of time elapsed by subtracting start ``time()`` from end ``time()``.
    - Calls ``log()``, so that, the temporal metadata is printed.

    :return: None

    """
    end = time()
    elapsed = end - start
    log(elapsed=seconds_to_string(elapsed))


# print_blow_dryer()
start = time()
atexit.register(end_log)