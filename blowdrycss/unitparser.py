# python 2
from __future__ import absolute_import

# builtins
from string import digits

# custom
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class UnitParser(object):
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

        The foremost tool for writing scalable style sheets is the "em" unit, and it therefore goes on top of
        the list of guidelines that we will compile throughout this chapter: use ems to make scalable style sheets.
        Named after the letter "M", the em unit has a long-standing tradition in typography where it has been used
        to measure horizontal widths.
        ...
        In CSS, the em unit is a general unit for measuring lengths, for example page margins and padding
        around elements. You can use it both horizontally and vertically, and this shocks traditional
        typographers who always have used em exclusively for horizontal measurements. By extending the em unit
        to also work vertically, it has become a very powerful unit - so powerful that you seldom have to
        use other length units.

        **Source:** Wikipedia -- https://en.wikipedia.org/wiki/Em_%28typography%29

        An em is a unit in the field of typography, equal to the currently specified point size. For example,
        one em in a 16-point typeface is 16 points. Therefore, this unit is the same for all typefaces at a
        given point size.

    """

    def __init__(self, property_name=''):
        self.property_name = property_name
        self.allowed = set(digits + '-.px')

        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        # Extracted all properties containing Values of <angle>, <percentage>, <length>, <time>, <frequency>
        # IDEA: Build webscraper that auto-extracts these. May not be deterministic enough.  Would need to build a
        # Page based on the standard that includes all property name/value combos.
        self.default_property_units_dict = {     # Number of possible values:
            'background-position': '%',          # single or double

            # 'border': 'px',                    # single   Shorthand Property unit addition Not implemented
            'border-top': 'px',                  # single
            'border-right': 'px',                # single
            'border-bottom': 'px',               # single
            'border-left': 'px',                 # single
            'border-spacing': 'px',              # single

            'border-width': 'px',                # single
            'border-top-width': 'px',            # single
            'border-right-width': 'px',          # single
            'border-bottom-width': 'px',         # single
            'border-left-width': 'px',           # single
            'border-radius': 'px',               # single
            'border-top-left-radius': 'px',      # single
            'border-top-right-radius': 'px',     # single
            'border-bottom-right-radius': 'px',  # single
            'border-bottom-left-radius': 'px',

            'elevation': 'deg',                  # single

            # 'font': 'px',                      # single    Shorthand Property unit addition Not implemented
            'font-size': 'px',                   # single

            'height': 'px',                      # single
            'max-height': 'px',                  # single
            'min-height': 'px',                  # single

            'letter-spacing': 'px',              # single
            'word-spacing': 'px',                # single

            'line-height': 'px',                 # single

            'top': 'px',                         # single
            'right': 'px',                       # single
            'bottom': 'px',                      # single
            'left': 'px',                        # single

            'margin': 'px',                      # single, double, quadruple
            'margin-top': 'px',                  # single
            'margin-right': 'px',                # single
            'margin-bottom': 'px',               # single
            'margin-left': 'px',                 # single

            # 'outline': 'px',                   # single    Shorthand Property unit addition Not implemented
            'outline-width': 'px',               # single

            'padding': 'px',                     # single, double, quadruple
            'padding-top': 'px',                 # single
            'padding-right': 'px',               # single
            'padding-bottom': 'px',              # single
            'padding-left': 'px',                # single

            'pause': 'ms',                       # single, double
            'pause-after': 'ms',                 # single
            'pause-before': 'ms',                # single

            'pitch': 'Hz',                       # single

            'text-indent': 'px',                 # single
            'text-shadow': 'px',                 # single, double, triple

            'vertical-align': '%',               # single

            'volume': '%',                       # single

            'width': 'px',                       # single
            'max-width': 'px',                   # single
            'min-width': 'px',                   # single
        }

    def default_units(self):
        """ Returns the default units "if any" for the assigned ``self.property_name``.

        :return: (*str*) -- Returns default units for the assigned ``self.property_name`` if they exist. Otherwise,
            return an empty string ``''``.

        """
        if self.property_name in self.default_property_units_dict:
            return self.default_property_units_dict[self.property_name]
        else:
            return ''

    def add_units(self, property_value=''):
        """ If the property_name requires units, then apply the default units defined in default_property_units_dict.

        **Rules:**

        - If use_em is False apply the default units for the property name by looking it up in
          default_property_units_dict.
        - Unit that have default units of ``px`` are converted to ``em`` if use_em is True.
        - If ``property_value`` has multiple property values, then split it apart.
        - If the value already has units, then pass it through unchanged.
        - The value provided shall possess negative signs and decimal points.
        - Mixed units are allowed, but **not recommended**.
        - Values shall only contain [] e.g. -1.25 can be processed, but n1_25 cannot be processed.

        :type property_value: str

        :param property_value: A string containing one or more space delimited alphanumeric characters.
        :return: (str) -- Returns the property value with the default or converted units added.

        >>> # Convert 'px' to 'em'
        >>> unit_parser = UnitParser(property_name='padding', use_em=True)
        >>> unit_parser.add_units('1 2 1 2')
        0.0625em 0.125em 0.0625em 0.125em
        >>> # Use default units
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('1 2 1 2')
        1px 2px 1px 2px
        >>> # Values already have units or are not parsable pass through
        >>> # True produces the same output.
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('55zp')
        55zp
        >>> unit_parser.add_units('17rem')
        17rem
        >>> # Unitless ``property_name``
        >>> # causes ``property_value`` to pass through.
        >>> unit_parser.property_name = 'font-weight'
        >>> unit_parser.add_units('200')
        200
        >>> # Mixed units cases - Not a Recommended Practice,
        >>> # but represent valid CSS. Be careful.
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('5em 6 5em 6')
        5em 6px 5em 6px
        >>> unit_parser.use_em = True
        >>> unit_parser.add_units('1em 100 4cm 9rem')
        1em 6.25em 4cm 9rem

        """
        new_value = []
        try:
            default_units = self.default_property_units_dict[self.property_name]    # See if property_name has units.
            for val in property_value.split():                                      # single, double and quadruple
                if set(val) <= self.allowed:
                    val = val.replace('px', '')                                     # Handle 'px' units case.
                    if settings.use_em and default_units == 'px':                   # Convert units if required.
                        new_value.append(settings.px_to_em(pixels=val))
                    else:
                        new_value.append(val + default_units)                       # Use default units.
                else:                                                               
                    new_value.append(val)                                           # Pass through and ignore value.
            property_value = ' '.join(new_value)                                    # Put the new values back together.
        except KeyError:
            pass                                                                    # Property is unitless.        
        return property_value
