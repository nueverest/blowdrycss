# python 3
import atexit
from time import time
from datetime import timedelta, datetime
__author__ = 'paul, nicojo, chad nelson'
__project__ = 'blow dry css'


# Reference: http://stackoverflow.com/questions/1557571/how-to-get-time-of-a-python-program-execution
# This is a modified version of Paul and Nicojo's answers.
def seconds_to_string(_time):
    return str(timedelta(seconds=_time).total_seconds())


def log(elapsed=None):
    completed_at = '\nCompleted @ ' + str(datetime.now())
    border = "=" * len(completed_at)
    print(completed_at)
    print(border)
    if elapsed:
        print("It took:", elapsed, "seconds")
    print(border)


def end_log():
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