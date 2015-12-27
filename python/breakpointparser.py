# custom
import settings
from utilities import deny_empty_or_whitespace
from datalibrary import xxsmall, xsmall, small, medium, large, xlarge, xxlarge, giant, xgiant, xxgiant
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class BreakpointParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Generic Screen Breakpoints xxsmall through xgiant:**

    - ``'name--breakpoint_values--limit_key'`` -- General Format
    - ``'inline-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit_key for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit_key
      for ``medium`` size screens.

    **Custom Usage: Set a specific pixel limit_key.**

    - ``'block-480px-down'`` -- Only displays the HTML element as a block for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.

        - **Note:** If unit conversion is enabled i.e. ``use_em`` is ``True``, then 624px would be converted to 39em.

    **Important Note about cssutils**

    Currently, ``cssutils`` does not support parsing media queries. Therefore, media queries need to be built, minified,
    and appended separately.

    :type css_class: str
    :type name: str
    :type value: str

    :param css_class: Potentially encoded css class that may or may not be parsable. May not be empty or None.
    :param name: Valid CSS property name. May not be empty or None.
    :param value: Valid CSS property name. May not be empty or None.

    :return: None

    **Examples:**

    >>> 'WARNING: NOT IMPLEMENTED YET'

    """
    def __init__(self, css_class='', name='', value=''):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace(name, variable_name='name')
        deny_empty_or_whitespace(value, variable_name='value')

        self.css_class = css_class
        self.name = name
        self.value = value
        self.units = 'em' if settings.use_em else 'px'

        # Dictionary of Breakpoint Dictionaries {'-only': (), '-down': [1], '-up': [0], }
        # '-only': ('min-width', 'max-width'),    # Lower and Upper Limits of the size.
        # '-down': ('max-width'),                 # Upper limit_key of size.
        # '-up': ('min-width'),                   # Lower Limit of size.
        self.breakpoint_dict = {
            '-xxsmall': {'-only': xxsmall, '-down': xxsmall[1], '-up': xxsmall[0], },
            '-xsmall': {'-only': xsmall, '-down': xsmall[1], '-up': xsmall[0], },
            '-small': {'-only': small, '-down': small[1], '-up': small[0], },
            '-medium': {'-only': medium, '-down': medium[1], '-up': medium[0], },
            '-large': {'-only': large, '-down': large[1], '-up': large[0], },
            '-xlarge': {'-only': xlarge, '-down': xlarge[1], '-up': xlarge[0], },
            '-xxlarge': {'-only': xxlarge, '-down': xxlarge[1], '-up': xxlarge[0], },
            '-giant': {'-only': giant, '-down': giant[1], '-up': giant[0], },
            '-xgiant': {'-only': xgiant, '-down': xgiant[1], '-up': xgiant[0], },
            '-xxgiant': {'-only': xxgiant, '-down': xxgiant[1], '-up': xxgiant[0], },
        }

        self.limit_key_set = {'-only', '-down', '-up', }

        self.breakpoint_key = ''
        self.limit_key = ''

    def set_breakpoint_key(self):
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
            _key = key + '-'
            if _key in self.css_class and len(self.css_class) > len(_key) + 2:
                self.breakpoint_key = key
                return
        raise ValueError(
            'The BreakpointParser.css_class ' + self.css_class +
            ' does not match a breakpoint_values in breakpoint_dict.'
        )

    def set_limit_key(self):
        """ If one of the values in ``self.limit_set`` is contained in ``self.css_class``, then
        Set ``self.limit_key`` to the value of the string found. Otherwise, raise a ValueError.

        **Rules:**

        - The ``limit_key`` may appear in the middle of ``self.css_class`` e.g. ``'padding-10-small-up-s-i'``.

        - The ``limit_key`` may appear at the end of ``self.css_class`` e.g. ``'margin-20-giant-down'``.

        - The length of ``self.css_class`` must be greater than the length of the limit_key + 2.  This prevents a
          ``css_class`` like ``'-up-'`` or ``'-only-'`` from being accepted as valid by themselves.

        - These rules do not catch all cases, and prior validation of the css_class is assumed.

        :raises ValueError: Raises a ValueError if none of the members of ``self.limit_set`` are found in
            ``self.css_class``.

        :return: None

        """
        for limit_key in self.limit_key_set:
            in_middle = (limit_key + '-') in self.css_class and len(self.css_class) > len(limit_key + '-') + 2
            at_end = self.css_class.endswith(limit_key)
            if in_middle or at_end:
                self.limit_key = limit_key
                return
        raise ValueError(
            'The BreakpointParser.css_class ' + self.css_class + ' does not match a limit_key in limit_set.'
        )

    def css_for_only(self):
        """ Generates css


        **Handle Cases:**

        - Special Usage with ``display``
            - The css_class ``display-large-only`` is a special case. The CSS property name ``display``
              without a value is used to show/hide content. For ``display`` reverse logic is used.
              The reason for this special handling of ``display`` is that we do not
              know what the current ``display`` setting is if any. This implies that the only safe way to handle it
              is by setting ``display`` to ``none`` for everything outside of the desired breakpoint limit.
            - *Note:* ``display + value + pair`` is handled under the General Usage case.
              For example, ``display-inline-large-only`` contains a value for ``display`` and only used to alter
              the way an element is displayed.
        - General Usage
            - The css_class ``padding-100-large-down`` applies ``padding: 100px`` for screen sizes less than
              the lower limit of ``large``.

        **CSS Media Queries**

        - *Special Case:* Generated CSS for ``display-large-only``::

        @media only screen and (max-width: 721px) {
            .display-large-only {
                display: none;
            }
        }

        @media only screen and (min-width: 1024px) {
            .display-large-only {
                display: none;
            }
        }

        -------------------------

        @media only screen and (min-width: 721px) and (max-width: 1024px) {
            .padding-100-large-only {
                padding: 100px;
            }
        }

        :return: None

        """
        if self.limit_key is '-only':
            pair = self.breakpoint_key + self.limit_key

            if 'display' + pair is self.css_class:          # Special 'display' usage case min/max reverse logic
                min_width = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key][1]) + self.units
                max_width = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key][0]) + self.units

                css = (
                    '@media only screen and (max-width: ' + max_width + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\tdisplay: none;\n' +
                    '\t}\n' +
                    '}\n\n' +
                    '@media only screen and (min-width: ' + min_width + ') {\n' +
                    '\t.display-large-only {\n' +
                    '\t\tdisplay: none;\n' +
                    '\t}\n' +
                    '}\n\n'
                )
                return css
            else:                                           # General usage case
                pass
        else:
            return ''

    def css_for_down(self):
        pass

    def css_for_up(self):
        pass

    def build_media_query(self):
        pass
