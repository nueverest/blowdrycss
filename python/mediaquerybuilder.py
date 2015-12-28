from breakpointparser import BreakpointParser
from scalingparser import ScalingParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class MediaQueryBuilder(object):
    def __init__(self):
        # Takes a set of classes that contain media query flags
        # Invalidates classes that contain mixed syntax ``small-down-s`` or ``font-size-28-medium-only-s``
        # i.e. mixing breakpoint and scaling syntax is not allowed.
        pass
