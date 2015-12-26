# custom
from utilities import deny_empty_or_whitespace
from datalibrary import xxsmall, xsmall, small, medium, large, xlarge, xxlarge, giant, xgiant, xxgiant
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class BreakpointParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Generic Screen Breakpoints xxsmall through xgiant:**

    - ``'name--breakpoint_values--limit'`` -- General Format
    - ``'inline-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit
      for ``medium`` size screens.

    **Custom Usage: Set a specific pixel limit.**

    - ``'block-480px-down'`` -- Only displays the HTML element as a block for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.

        - **Note:** If unit conversion is enabled i.e. ``px_to_em`` is ``True``, then 624px would be converted to 39em.

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

        self.breakpoint_dict = {
            'xxsmall': xxsmall,
            'xsmall': xsmall,
            'small': small,
            'medium': medium,
            'large': large,
            'xlarge': xlarge,
            'xxlarge': xxlarge,
            'giant': giant,
            'xgiant': xgiant,
            'xxgiant': xxgiant,
        }

        self.limit_dict = {
            '-only': (),
            '-down': (),
            '-up': (),
        }

        self.breakpoint_key = ''
        self.breakpoint_values = ()
        self.limit = ''

    def set_breakpoint(self):
        """ If ``self.css_class`` contains one of the keys in ``self.breakpoint_dict``, then
        set ``self.breakpoint_values`` to a breakpoint_values tuple for the matching key. Otherwise, raise a ValueError.

        **Rules:**

        - Before a comparison is made each key is wrapped in dashes i.e. ``-key-`` since the key must appear in the
          middle of a ``self.css_class``.

            - This also prevents false positives since searching for ``small`` could match ``xxsmall``, ``xsmall``,
              and ``small``.

        - The length of ``self.css_class`` must be greater than the length of the key + 2.  This prevents a
          ``css_class`` like ``'-xsmall-'`` or ``'-xxlarge-up'`` from being accepted as valid by themselves.

        - These rules do not catch all cases, and prior validation of the css_class is assumed.

        :raises ValueError: Raises a ValueError if none of the keys in ``self.breakpoint_dict`` are found in
            ``self.css_class``.

        :return: None

        """
        for key, value in self.breakpoint_dict.items():
            _key = '-' + key + '-'
            if _key in self.css_class and len(self.css_class) > len(_key) + 2:
                self.breakpoint_key = key
                self.breakpoint_values = value
                return
        raise ValueError(
                'The BreakpointParser.css_class ' + self.css_class +
                ' does not match a breakpoint_values in breakpoint_dict.'
        )

    def set_limit(self):
        """ If one of the values in ``self.limit_set`` is contained in ``self.css_class``, then
        Set ``self.limit`` to the value of the string found. Otherwise, raise a ValueError.

        **Rules:**

        - The ``limit`` may appear in the middle of ``self.css_class`` e.g. ``'padding-10-small-up-s-i'``.

        - The ``limit`` may appear at the end of ``self.css_class`` e.g. ``'margin-20-giant-down'``.

        - The length of ``self.css_class`` must be greater than the length of the limit + 2.  This prevents a
          ``css_class`` like ``'-up-'`` or ``'-only-'`` from being accepted as valid by themselves.

        - These rules do not catch all cases, and prior validation of the css_class is assumed.

        :raises ValueError: Raises a ValueError if none of the members of ``self.limit_set`` are found in
            ``self.css_class``.

        :return: None

        """
        for limit in self.limit_dict:
            in_middle = (limit + '-') in self.css_class and len(self.css_class) > len(limit + '-') + 2
            at_end = self.css_class.endswith(limit)
            if in_middle or at_end:
                self.limit = limit
                return
        raise ValueError(
                'The BreakpointParser.css_class ' + self.css_class + ' does not match a limit in limit_set.'
        )

    def breakpoint_limit_pair_is_valid(self):
        """ Tests whether the breakpoint_key and limit pair is correct together.

        **Rules:**

        - The ``breakpoint_key`` and ``limit`` must appear together in the form: ``breakpoint_key + limit``.
            - ``breakpoint_key + 'some string' + limit`` is invalid.
        - The pair may appear in the middle of the string if it is at least
          two characters longer than ``self.css_class``.
        - The pair may appear at the end of the string.

        :return: Returns True if the breakpoint_key and limit pair conforms to the rules above.
            Otherwise, it returns False.

        """
        pair = self.breakpoint_key + self.limit
        in_middle = pair in self.css_class and len(self.css_class) > len('-' + pair + '-') + 2
        at_end = self.css_class.endswith(pair)
        return in_middle or at_end

    def generate_css_with_breakpoint(self):
        pass
