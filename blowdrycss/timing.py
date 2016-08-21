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

# custom
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class Timer(object):
    """ A performance Timer that reports the amount of time it took to run a block of code.

    | **Parameters:**

    | **start** (*time*) -- Time that the program started.

    | **end** (*time*) -- Time that the program ended.


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
        """ Sets ``end`` time and prints the time elapsed (delta T).  Calls ``print_time()``, and prints
        temporal metadata.

        :return: None

        """
        self.end = time()
        self.print_time()


class LimitTimer(object):
    """ Timer governs when to perform a full and comprehensive run of blowdry.parse().

    .. note::   This is independent of file modification watchdog triggers which only scan the file(s) that changed
        since the last run.

    ** Why is a LimitTimer needed? **

    *Understanding the Truth Table*

    #. The project only contains two files: File 1  and File 2.
    #. Each file either contains the CSS class selector 'blue' or not i.e. set().
    #. File 2 is modified. Either the class ``blue`` is added or removed i.e. set().
    #. X means don't care whether the file contains blue or set().
    #. Case #3 is the reason why the LimitTimer is required. The css class selector ``blue``
       was only defined in File 2. Then blue was removed from File 2. Since blue existed in the
       combined class_set before File 2 was modified, it will remain in the
       combined class_set after the union with set(). This is undesirable in Case #3 since ``blue`` is not
       used anymore in either of the two files. The LimitTimer runs periodically to clear these unused selectors.

    +--------+------------------+------------------+--------------------+-----------------+--------------------+
    | Case # | File 1 class_set | File 2 class_set | Combined class_set | File 2 modified | Combined class_set |
    +========+==================+==================+====================+=================+====================+
    |    1   |       blue       |       blue       |        blue        |      set()      |        blue        |
    +--------+------------------+------------------+--------------------+-----------------+--------------------+
    |    2   |       blue       |       set()      |        blue        |        X        |        blue        |
    +--------+------------------+------------------+--------------------+-----------------+--------------------+
    |    3   |       set()      |       blue       |        blue        |      set()      |        blue        |
    +--------+------------------+------------------+--------------------+-----------------+--------------------+
    |    4   |       set()      |       set()      |        set()       |       blue      |        blue        |
    +--------+------------------+------------------+--------------------+-----------------+--------------------+
    |    5   |       set()      |       set()      |        set()       |      set()      |        set()       |
    +--------+------------------+------------------+--------------------+-----------------+--------------------+

    ** Another reason why the LimitTimer is needed. **

    On windows and mac watchdog on_modify event gets triggered twice on save. In order to prevent a duplicate run
    for the same change or set of changes this class is implemented. It can also depend on the IDE being
    used since some IDEs auto-save.

    | **Members:**

    | **time_limit** (*str*) -- Number of seconds that must pass before the limit is exceeded. Default is
      settings.time_limit.

    | **start_time** (*str*) -- Time that the timer started.

    :return: None

    **Example**

    >>> from blowdrycss.timing import LimitTimer
    >>> limit_timer = LimitTimer()
    >>> if limit_timer.limit_exceeded:
    >>>     print("30 minutes elapses.")
    >>>     limit_timer.reset()
    """
    def __init__(self):
        self._time_limit = settings.time_limit
        self.start_time = time()

    @property
    def time_limit(self):
        """ Getter returns ``_time_limit``.

        :return: (*int*) -- Returns ``_time_limit``.

        """
        return self._time_limit

    @time_limit.setter
    def time_limit(self, custom_limit):
        """ Set time_limit in units of seconds.

        :type custom_limit: int
        :param custom_limit: Time limit in units of seconds.

        :return: None

        """
        self._time_limit = custom_limit

    @property
    def limit_exceeded(self):
        """ Compares the current time to the start time, and returns True if ``self.time_limit``
        is exceeded and False otherwise.

        :return: (*bool*) -- Returns True if ``self.time_limit`` is exceeded and False otherwise.

        """
        return time() - self.start_time >= self.time_limit

    def reset(self):
        """ Resets ``self.start`` to the current time.

        :return: None

        """
        self.start_time = time()
