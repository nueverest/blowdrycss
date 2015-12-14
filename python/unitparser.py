"""
**Used in these cases:**

- No units are provided and default units need to be added to make it valid css.
- The user wants their pixel (px) based units to be converted to em or root em (rem)
  so that their page scales / zooms properly.

**Assumption:** The value provided already has negative signs and decimal points. There are no dashes or
underscores present in the value e.g. -1.25 can be processed, but n1_25 cannot be processed.

**Contains a ``default_property_units_dict``** which maps property names to their default units.

**Note:** Shorthand properties are not supported.

**Why do I want to use em (named after the sound for the letter 'M') or root em (rem)?:**

    *Because your webpage will scale with browser and device size.*

|

.. http://snook.ca/archives/html_and_css/font-size-with-rem
   https://css-tricks.com/rems-ems/

**What does (em) actually stand for?:**
    **Source:** W3C -- http://www.w3.org/WAI/GL/css2em.htm

    The foremost tool for writing scalable style sheets is the "em" unit, and it therefore goes on top of the list of
    guidelines that we will compile throughout this chapter: use ems to make scalable style sheets. Named after the
    letter "M", the em unit has a long-standing tradition in typography where it has been used to measure
    horizontal widths.
    ...
    In CSS, the em unit is a general unit for measuring lenghts, for example page margins and padding around elements.
    You can use it both horizontally and vertically, and this shocks traditional typographers who always have used
    em exclusively for horizontal measurements. By extending the em unit to also work vertically, it has become
    a very powerful unit - so powerful that you seldom have to use other length units.

------------

    **Source:** Wikipedia -- https://en.wikipedia.org/wiki/Em_%28typography%29

    An em is a unit in the field of typography, equal to the currently specified point size. For example, one em in a
    16-point typeface is 16 points. Therefore, this unit is the same for all typefaces at a given point size.

"""

from string import digits
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class UnitParser(object):
    def __init__(self, property_name='', base=16, px_to_em=True):
        self.property_name = property_name
        self.base = float(base)               # Default: 16px = 1rem
        self.px_to_em = px_to_em
        self.allowed = set(digits + '-.px')

        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        # Extracted all properties containing Values of <angle>, <percentage>, <length>, <time>, <frequency>
        # IDEA: Build webscraper that auto-extracts these. May not be deterministic enough.  Would need to build a
        # Page based on the standard that includes all property name/value combos.
        self.default_property_units_dict = {  # Number of possible values:
            'azimuth': 'deg',                 # single
            'background-position': '%',       # single or double

            # 'border': 'px',                 # single   Shorthand Property unit addition Not implemented
            'border-top': 'px',               # single
            'border-right': 'px',             # single
            'border-bottom': 'px',            # single
            'border-left': 'px',              # single
            'border-spacing': 'px',           # single

            'border-width': 'px',             # single
            'border-top-width': 'px',         # single
            'border-right-width': 'px',       # single
            'border-bottom-width': 'px',      # single
            'border-left-width': 'px',        # single

            'elevation': 'deg',               # single

            # 'font': 'px',                   # single    Shorthand Property unit addition Not implemented
            'font-size': 'px',                # single

            'height': 'px',                   # single
            'max-height': 'px',               # single
            'min-height': 'px',               # single

            'letter-spacing': 'px',           # single
            'word-spacing': 'px',             # single

            'line-height': 'px',              # single

            'top': 'px',                      # single
            'right': 'px',                    # single
            'bottom': 'px',                   # single
            'left': 'px',                     # single

            'margin': 'px',                   # single, double, quadruple
            'margin-top': 'px',               # single
            'margin-right': 'px',             # single
            'margin-bottom': 'px',            # single
            'margin-left': 'px',              # single

            # 'outline': 'px',                # single    Shorthand Property unit addition Not implemented
            'outline-width': 'px',            # single

            'padding': 'px',                  # single, double, quadruple
            'padding-top': 'px',              # single
            'padding-right': 'px',            # single
            'padding-bottom': 'px',           # single
            'padding-left': 'px',             # single

            'pause': 'ms',                    # single, double
            'pause-after': 'ms',              # single
            'pause-before': 'ms',             # single

            'pitch': 'Hz',                    # single

            'text-indent': 'px',              # single

            'vertical-align': '%',            # single

            'volume': '%',                    # single

            'width': 'px',                    # single
            'max-width': 'px',                # single
            'min-width': 'px',                # single
        }

    def add_units(self, property_value=''):
        """
        If the property_name requires units, then apply the default units defined in default_property_units_dict.

        **Rules:**

        - If px_to_em is False apply the default units for the property name by looking it up in
        default_property_units_dict.
        - If ``property_value`` has multiple property values, then split it apart.
        - If the value already has units, then pass it through unchanged.
        - The value provided shall possess negative signs and decimal points.
        - Values shall only contain [] e.g. -1.25 can be processed, but n1_25 cannot be processed.

        :type property_value: str

        :param property_value: A string containing one or more space delimited numeric values.
        :return: (str) - Returns the property value with the default or converted units added.

        Handles cases input like: '12', '1 2 1 2', '5px 1 2px 13'
        Unconverted Outputs: '12px', '1px 2px 1px 2px', '5px 1px 2px 13px'
        'em' Converted Outputs: '0.75em', '0.0625em 0.125em 0.0625em 0.125em', '0.3125em 0.0625em 0.125em 0.8125em'
        'px' is converted to 'em' if px_to_em is True.
        Invalid input like '12a', '55zp', '42u3' are passed through and ignored.
        """
        new_value = []
        try:
            default_units = self.default_property_units_dict[self.property_name]    # See if property_name has units.
            for val in property_value.split():                                      # single, double and quadruple
                if set(val) <= self.allowed:
                    val = val.replace('px', '')                                     # Handle 'px' units case.
                    if self.px_to_em and default_units == 'px':                     # Convert units if required.
                        new_value.append(self.convert_px_to_em(pixels=val))
                    else:
                        new_value.append(val + default_units)                       # Use default units.
                else:                                                               
                    new_value.append(val)                                           # Pass through and ignore value.
            property_value = ' '.join(new_value)                                    # Put the new values back together.
        except KeyError:
            pass                                                                    # Property is unitless.        
        return property_value

    def convert_px_to_em(self, pixels):
        """
        Convert value from px to em using self.base.

        **Rule:**
        - ``pixels`` shall only contain [0-9.-].
        - Inputs that contain any other value are simply passed through.

        Round float to a maximum of 4 decimal places.

        :type pixels: str, int, or float

        :param pixels: A numeric value with the units stripped.
        :return: (str)
        """
        if set(str(pixels)) <= set(digits + '-.'):
            em = float(pixels) / float(self.base)
            em = round(em, 4)
            em = str(em) + 'em'                                                         # Add 'em'.
            return em
        return pixels

