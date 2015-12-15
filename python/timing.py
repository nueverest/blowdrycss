"""
Simple timing system that allows for the execution time to be recorded

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

# python 3
import atexit
from time import time
from datetime import timedelta, datetime
__author__ = 'paul, nicojo, chad nelson'
__project__ = 'blow dry css'


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
    border = "=" * len(completed_at)
    print(completed_at)
    print(border)
    if elapsed:
        print("It took:", elapsed, "seconds")
    print(border)


def end_log():
    """
    - Calculates the amount of time elapsed by subtracting start ``time()`` from end ``time()``.
    - Calls ``log()``, so that, the temporal metadata is printed.

    :return: None

    """
    end = time()
    elapsed = end - start
    log(elapsed=seconds_to_string(elapsed))


start = time()
atexit.register(end_log)


# python 2.x
#
# import atexit
# from time import clock
#
# def secondsToStr(t):
#     return "%d:%02d:%02d.%03d" % \
#         reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
#             [(t*1000,),1000,60,60])
#
# line = "="*40
# def log(s, elapsed=None):
#     print line
#     print secondsToStr(clock()), '-', s
#     if elapsed:
#         print "Elapsed time:", elapsed
#     print line
#     print
#
# def endlog():
#     end = clock()
#     elapsed = end-start
#     log("End Program", secondsToStr(elapsed))
#
# def now():
#     return secondsToStr(clock())
#
# start = clock()
# atexit.register(endlog)
# log("Start Program")