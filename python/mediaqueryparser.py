# custom
from utilities import deny_empty_or_whitespace
from unitparser import UnitParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class MediaQueryParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Generic Screen Size Triggers:**

    - ``'inline-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit
      for ``medium`` size screens.

    **Custom Usage: Set a specific pixel limit.**

    - ``'block-480px-down'`` -- Only displays the HTML element as a block for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.

        - **Note:** If unit conversion is enabled i.e. ``px_to_em`` is ``True``, then 624px would be converted to 39em.

    **Responsive Flag:**

    Append ``'-r'`` to the end of an encoded property values to scale the value up and down based on screen size.

    Note: This only works on property values containing distance--based units (pixels, em, etc).

    - General format: ``<name>-<value>-r``

    - Specific case: ``font-size-24-r``

    - Priority ``!important`` case: ``font-size-24-r-i``

        - (``'-i'`` *is always last*)

    **Responsive Scaling Ratios:**

    - Assuming ``font-size-24-r`` is the encoded css class, the font-size will respond to the screen size according
      to the following table:

        +-------------+---------------+----------------+------+-------+
        | Screen Size | Trigger Range | Scaling Factor |  px  | em    |
        +-------------+---------------+----------------+------+-------+
        | Large       |    > 720px    |        1       |  24  | 1.5   |
        +-------------+---------------+----------------+------+-------+
        | Medium      |    < 720px    |      1.125     | 21.3 | 1.333 |
        +-------------+---------------+----------------+------+-------+
        | Small       |    < 480px    |      1.25      | 19.2 | 1.2   |
        +-------------+---------------+----------------+------+-------+

    - Generated CSS for ``font-size-24-r``::

        .font-size-24-r {
            font-size: 24px;

            // medium screen font size reduction
            @media only screen and (max-width: 720px) {
                font-size: 21.3px;
            }

            // small screen font size reduction
            @media only screen and (max-width: 480px) {
                font-size: 19.2px;
            }
        }

    **Important Note about cssutils**

    Currently, ``cssutils`` does not support parsing media queries. Therefore, media queries need to be built, minified,
    and appended separately.

    :type css_class: str
    :type name: str
    :type value: str
    :type px_to_em: bool

    :param css_class: Potentially encoded css class that may or may not be parsable. May not be empty or None.
    :param name: Valid CSS property name. May not be empty or None.
    :param value: Valid CSS property name. May not be empty or None.
    :param px_to_em: A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion (default).
        False disables unit conversions meaning any pixel value remains unchanged.
    :return: None

    **Examples:**

    >>> 'WARNING: NOT IMPLEMENTED YET'

    """
    def __init__(self, css_class='', name='', value='', px_to_em=True):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace(name, variable_name='name')
        deny_empty_or_whitespace(value, variable_name='value')

        self.css_class = css_class
        self.name = name
        self.value = value
        self.px_to_em = px_to_em

        # Default Screen Breakpoints / Transition Triggers
        # Tuple Format (Lower Limit, Upper Limit) in pixels.
        # Note: These values do not change even if unit conversion is enabled i.e. ``px_to_em`` is ``True``.
        # Common Screen Resolutions: https://en.wikipedia.org/wiki/List_of_common_resolutions
        self.xxsmall = (0, 120)
        self.xsmall = (121, 240)
        self.small = (241, 480)
        self.medium = (481, 720)            # Typical mobile device break point @ 720px.
        self.large = (721, 1024)
        self.xlarge = (1025, 1366)
        self.xxlarge = (1367, 1920)
        self.giant = (1921, 2560)
        self.xgiant = (2561, 10**10)

        self.breakpoint_dict = {
            'xxsmall': self.xxsmall,
            'xsmall': self.xxsmall,
            'small': self.small,
            'medium': self.medium,
            'large': self.large,
            'xlarge': self.xlarge,
            'xxlarge': self.xxlarge,
            'giant': self.giant,
            'xgiant': self.xgiant,
        }

        self.direction_set = {'-only', '-down', '-up', }

        self.breakpoint = ()
        self.direction = ''

    def set_breakpoint(self):
        pass

    def set_direction(self):
        pass

    def generate_css_with_breakpoint(self):
        pass

    def is_responsive(self):
        """ Return False if ``self.property_name`` does not have default units of ``'px'``.
        Test if ``self.css_class`` contains the responsive flag ``-r``. Returns True if ``-r`` is found and
        False otherwise.

        **Rules:**

        - The ``self.property_name`` must possess units of pixels ``'px'``.
        - If no property priority is set the encoded ``css_class`` must end with ``-r``.
        - If priority is set the encoded ``css_class`` must end with ``-r-i``.

        :return: (*bool*) -- Returns True if ``-r`` is found and False otherwise.

        **Examples**

        >>> responsive_parser = MediaQueryParser(css_class='font-weight-24-r')
        >>> responsive_parser.is_responsive()
        True
        >>> responsive_parser.css_class = 'font-weight-24-r-i'
        >>> responsive_parser.is_responsive()
        True
        >>> responsive_parser.css_class = 'font-weight-24'
        >>> responsive_parser.is_responsive()
        False

        """
        unit_parser = UnitParser(property_name=self.name, px_to_em=self.px_to_em)
        if unit_parser.default_units() != 'px':
            return False
        else:
            return self.css_class.endswith('-r') or self.css_class.endswith('-r-i')

    def generate_responsive_css(self):
        _max = 1
        small_max = self.small[_max]
        medium_max = self.medium[_max]
        pass
