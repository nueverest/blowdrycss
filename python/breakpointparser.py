from cssutils.css import Property
# custom
from settings import use_em, xxsmall, xsmall, small, medium, large, xlarge, xxlarge, giant, xgiant, xxgiant
from utilities import deny_empty_or_whitespace
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class BreakpointParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Standard screen breakpoints xxsmall through xgiant:**

    - ``'name--breakpoint_values--limit_key'`` -- General Format
    - ``'inline-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit_key for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit_key
      for ``medium`` size screens.

    **Custom user defined breakpoint limit_key.**

    - ``'block-480px-down'`` -- Only displays the HTML element as a block for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.

        - **Note:** If unit conversion is enabled i.e. ``use_em`` is ``True``, then 624px would be converted to 39em.

    **Important Note about cssutils and media queries**

    Currently, ``cssutils`` does not support parsing media queries. Therefore, media queries need to be built, minified,
    and appended separately.

    :type css_class: str
    :type css_property: Property

    :param css_class: Potentially encoded css class that may or may not be parsable. May not be empty or None.
    :param css_property: Valid CSS Property as defined by ``cssutils.css.Property``.

    :return: None

    **Examples:**

    >>> from cssutils.css import Property
    >>> from xml.dom import SyntaxErr
    >>> # value='inherit' since we do not know if the class is valid yet.
    >>> name = 'display'
    >>> value = 'inherit'
    >>> priority = ''
    >>> inherit_property = Property(name=name, value=value, priority=priority)
    >>> breakpoint_parser = BreakpointParser(
            css_class='large-up',
            css_property=inherit_property
        )
    >>> print(breakpoint_parser.breakpoint_key)
    large
    >>> print(breakpoint_parser.limit_key)
    -up
    >>> # Validate encoded syntax.
    >>> is_breakpoint = breakpoint_parser.is_breakpoint
    >>> if is_breakpoint:
    >>>     clean_css_class = breakpoint_parser.strip_breakpoint_limit()
    >>>     # Change value to 'none' as display media queries use reverse logic.
    >>>     value = 'none'
    >>> # Build CSS Property
    >>> try:
    >>>     css_property = Property(name=name, value=value, priority=priority)
    >>>     if css_property.valid:
    >>>         if is_breakpoint and breakpoint_parser:
    >>>             breakpoint_parser.css_property = css_property
    >>>             media_query = breakpoint_parser.build_media_query()
    >>>     else:
    >>>         print(' (cssutils invalid property value: ' + value + ')')
    >>> except SyntaxErr:
    >>>     print('(cssutils SyntaxErr invalid property value: ' + value + ')')
    >>> print(media_query)
    @media only screen and (max-width: 45.0625em) {
        .large-up {
            display: none;
        }
    }

    """
    def __init__(self, css_class='', css_property=Property()):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace(css_property.cssText, variable_name='name')

        self.css_class = css_class
        self.css_property = css_property
        self.units = 'em' if use_em else 'px'

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

        self.is_breakpoint = True       # Naively assume True. set_breakpoint_key and set_limit_key can change to False.
        self.set_breakpoint_key()
        self.set_limit_key()

        self.limit_key_methods = {
            '-only': self.css_for_only,
            '-down': self.css_for_down,
            '-up': self.css_for_up,
        }

    def set_breakpoint_key(self):
        """ If ``self.css_class`` contains one of the keys in ``self.breakpoint_dict``, then
        set ``self.breakpoint_values`` to a breakpoint_values tuple for the matching key. Otherwise,
        set ``is_breakpoint = False``.

        **Rules:**

        - Before a comparison is made each key is wrapped in dashes i.e. ``-key-`` since the key must appear in the
          middle of a ``self.css_class``.

            - This also prevents false positives since searching for ``small`` could match ``xxsmall``, ``xsmall``,
              and ``small``.

        - The length of ``self.css_class`` must be greater than the length of the key + 2.  This prevents a
          ``css_class`` like ``'-xsmall-'`` or ``'-xxlarge-up'`` from being accepted as valid by themselves.

        - The ``key`` minus the preceeding dash is allowed if it the key is the first word in the string. This allows
          the shorthand cases, for example: ``small-only``, ``medium-up``, ``giant-down``.  These cases imply that
          the CSS property name is ``display``.

        - These rules do not catch all cases, and prior validation of the css_class is assumed.

        - Set ``is_breakpoint = False`` if none of the keys in ``self.breakpoint_dict`` are found in
            ``self.css_class``.

        :return: None

        **Examples:**

        >>> from cssutils.css import Property
        >>> # value='inherit' since we do not know if the class is valid yet.
        >>> name = 'display'
        >>> value = 'inherit'
        >>> priority = ''
        >>> inherit_property = Property(name=name, value=value, priority=priority)
        >>> breakpoint_parser = BreakpointParser(
                css_class='padding-1em-giant-down',
                css_property=inherit_property
            )
        >>> # BreakpointParser() sets breakpoint_key.
        >>> print(breakpoint_parser.breakpoint_key)
        giant

        """
        for key, value in self.breakpoint_dict.items():
            _key = key + '-'
            if (_key in self.css_class and len(self.css_class) > len(_key) + 2) or self.css_class.startswith(_key[1:]):
                self.breakpoint_key = key
                return
        self.is_breakpoint = False

    def set_limit_key(self):
        """ If one of the values in ``self.limit_set`` is contained in ``self.css_class``, then
        Set ``self.limit_key`` to the value of the string found. Otherwise, set ``is_breakpoint = False``.

        **Rules:**

        - The ``limit_key`` may appear in the middle of ``self.css_class`` e.g. ``'padding-10-small-up-s-i'``.

        - The ``limit_key`` may appear at the end of ``self.css_class`` e.g. ``'margin-20-giant-down'``.

        - The length of ``self.css_class`` must be greater than the length of the limit_key + 2.  This prevents a
          ``css_class`` like ``'-up-'`` or ``'-only-'`` from being accepted as valid by themselves.

        - These rules do not catch all cases, and prior validation of the css_class is assumed.

        - Set ``is_breakpoint = False`` if none of the members of ``self.limit_set`` are found in
            ``self.css_class``.

        :return: None

        **Examples:**

        >>> from cssutils.css import Property
        >>> # value='inherit' since we do not know if the class is valid yet.
        >>> name = 'display'
        >>> value = 'inherit'
        >>> priority = ''
        >>> inherit_property = Property(name=name, value=value, priority=priority)
        >>> breakpoint_parser = BreakpointParser(
                css_class='padding-1em-giant-down',
                css_property=inherit_property
            )
        >>> # BreakpointParser() sets limit_key.
        >>> print(breakpoint_parser.limit_key)
        -down

        """
        for limit_key in self.limit_key_set:
            in_middle = (limit_key + '-') in self.css_class and len(self.css_class) > len(limit_key + '-') + 2
            at_end = self.css_class.endswith(limit_key)
            if in_middle or at_end:
                self.limit_key = limit_key
                return
        self.is_breakpoint = False

    def strip_breakpoint_limit(self):
        """ Removes breakpoint and limit keywords from ``css_class``.

        **Rules:**

        - Return ``''`` if breakpoint limit key pair == ``css_class``.
            - ``'xlarge-only'`` becomes ``''``.

        - Return ``property_name + property_value - breakpoint_key - limit_key``.
            - ``'bold-large-up'`` becomes ``'bold'``.

        :return: (*str*) -- Returns a modified version ``css_class`` with breakpoint and limit key syntax removed.

        **Examples:**

        >>> from cssutils.css import Property
        >>> # value='inherit' since we do not know if the class is valid yet.
        >>> name = 'display'
        >>> value = 'inherit'
        >>> priority = ''
        >>> inherit_property = Property(name=name, value=value, priority=priority)
        >>> breakpoint_parser = BreakpointParser(
                css_class='xlarge-only',
                css_property=inherit_property
            )
        >>> breakpoint_parser.strip_breakpoint_limit()
        ''
        >>> inherit_property = Property(name='font-weight', value=value, priority=priority)
        >>> breakpoint_parser.css_class='bold-large-up'
        >>> breakpoint_parser.strip_breakpoint_limit()
        'bold'

        """
        if self.css_class.startswith(self.breakpoint_key[1:]):
            return self.css_class.replace(self.breakpoint_key[1:], '').replace(self.limit_key, '')
        else:
            return self.css_class.replace(self.breakpoint_key, '').replace(self.limit_key, '')

    def is_display(self):
        """ Tests if ``css_class`` contains character patterns that match the special case when the property name is
        ``display``.

        :return: (*bool*) -- Returns true if one of the cases is ``true``. Otherwise it returns ``false``.

        **Examples:**

        >>> from cssutils.css import Property
        >>> # value='inherit' since we do not know if the class is valid yet.
        >>> name = 'display'
        >>> value = 'inherit'
        >>> priority = ''
        >>> inherit_property = Property(name=name, value=value, priority=priority)
        >>> breakpoint_parser = BreakpointParser(
                css_class='xlarge-only',
                css_property=inherit_property
            )
        >>> breakpoint_parser.strip_breakpoint_limit()
        ''
        >>> inherit_property = Property(name='font-weight', value=value, priority=priority)
        >>> breakpoint_parser.css_class='bold-large-up'
        >>> breakpoint_parser.strip_breakpoint_limit()
        'bold'

        """
        pair = self.breakpoint_key + self.limit_key
        case1 = 'display' + pair == self.css_class
        case2 = pair[1:] == self.css_class
        case3 = pair[1:] + '-i' == self.css_class

        return case1 or case2 or case3

    def css_for_only(self):
        """ Generates css

        **Handle Cases:**

        - Special Usage with ``display``
            - The css_class ``display-large-only`` is a special case. The CSS property name ``display``
              without a value is used to show/hide content. For ``display`` reverse logic is used.
              The reason for this special handling of ``display`` is that we do not
              know what the current ``display`` setting is if any. This implies that the only safe way to handle it
              is by setting ``display`` to ``none`` for everything outside of the desired breakpoint limit.
            - Shorthand cases, for example: ``small-only``, ``medium-up``, ``giant-down`` are allowed.
              These cases imply that the CSS property name is ``display``.
              This is handled in the ``if-statement`` via ``pair[1:] == self.css_class``.
            - *Note:* ``display + value + pair`` is handled under the General Usage case.
              For example, ``display-inline-large-only`` contains a value for ``display`` and only used to alter
              the way an element is displayed.

        - General Usage

            - The css_class ``padding-100-large-down`` applies ``padding: 100px`` for screen sizes less than
              the lower limit of ``large``.

        **Note:** Unit conversions for pixel-based ``self.value`` is required **before** the
        BreakpointParser is instantiated.

        **Media Query Examples**

        - *Special Case:* Generated CSS for ``display-large-only`` or ``large-only``::

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

        - *General Usage Case:* Generated CSS for ``padding-100-large-only``::

            @media only screen and (min-width: 721px) and (max-width: 1024px) {
                .padding-100-large-only {
                    padding: 100px;
                }
            }

        - *Priority !important Case:* Generated CSS for ``large-only-i``::

            @media only screen and (max-width: 721px) {
                .display-large-only {
                    display: none !important;
                }
            }

            @media only screen and (min-width: 1024px) {
                .display-large-only {
                    display: none !important;
                }
            }

        :return: None

        """
        if self.limit_key == '-only':
            lower_limit = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key][0])
            upper_limit = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key][1])

            # Special 'display' usage case min/max reverse logic
            if self.is_display():
                css = (
                    '@media only screen and (max-width: ' + lower_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n' +
                    '@media only screen and (min-width: ' + upper_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
            # General usage case
            else:
                css = (
                    '@media only screen and (min-width: ' + lower_limit + ') and (max-width: ' + upper_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
        else:
            css = ''

        return css

    def css_for_down(self):
        """ Only display the element, or apply a property rule ``below`` a given screen breakpoint.
        Returns the generated css.

        **Handle Cases:**

        - Special Usage with ``display``
            - The css_class ``display-medium-down`` is a special case. The CSS property name ``display``
              without a value is used to show/hide content. For ``display`` reverse logic is used.
              The reason for this special handling of ``display`` is that we do not
              know what the current ``display`` setting is if any. This implies that the only safe way to handle it
              is by setting ``display`` to ``none`` for everything outside of the desired breakpoint limit.
            - Shorthand cases, for example: ``small-only``, ``medium-up``, ``giant-down`` are allowed.
              These cases imply that the CSS property name is ``display``.
              This is handled in the ``if-statement`` via ``pair[1:] == self.css_class``.
            - *Note:* ``display + value + breakpoint + limit`` is handled under the General Usage case.
              For example, ``display-inline-medium-down`` contains a value for ``display`` and only used to alter
              the way an element is displayed.

        - General Usage

            - The css_class ``padding-100-medium-down`` applies ``padding: 100px`` for screen sizes less than
              the lower limit of ``medium``.

        **Note:** Unit conversions for pixel-based ``self.value`` is required **before** the
        BreakpointParser is instantiated.

        **Media Query Examples**

        - *Special Case:* Generated CSS for ``display-medium-down``::

            @media only screen and (min-width: 720px) {
                .display-medium-down {
                    display: none;
                }
            }

        - *General Usage Case:* Generated CSS for ``padding-100-medium-down``::

            @media only screen and (max-width: 720px) {
                .padding-100-medium-down {
                    padding: 100px;
                }
            }

        :return: None

        """
        if self.limit_key == '-down':
            upper_limit = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key])

            # Special 'display' usage case min/max reverse logic
            if self.is_display():
                css = (
                    '@media only screen and (min-width: ' + upper_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
            # General usage case
            else:
                css = (
                    '@media only screen and (max-width: ' + upper_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
        else:
            css = ''

        return css

    def css_for_up(self):
        """ Only display the element, or apply a property rule ``above`` a given screen breakpoint.
        Returns the generated css.

        **Handle Cases:**

        - Special Usage with ``display``
            - The css_class ``display-small-up`` is a special case. The CSS property name ``display``
              without a value is used to show/hide content. For ``display`` reverse logic is used.
              The reason for this special handling of ``display`` is that we do not
              know what the current ``display`` setting is if any. This implies that the only safe way to handle it
              is by setting ``display`` to ``none`` for everything outside of the desired breakpoint limit.
            - Shorthand cases, for example: ``small-only``, ``medium-up``, ``giant-down`` are allowed.
              These cases imply that the CSS property name is ``display``.
              This is handled in the ``if-statement`` via ``pair[1:] == self.css_class``.
            - *Note:* ``display + value + breakpoint + limit`` is handled under the General Usage case.
              For example, ``display-inline-small-up`` contains a value for ``display`` and only used to alter
              the way an element is displayed.

        - General Usage

            - The css_class ``padding-100-small-up`` applies ``padding: 100px`` for screen sizes less than
              the lower limit of ``small``.

        **Note:** Unit conversions for pixel-based ``self.value`` is required **before** the
        BreakpointParser is instantiated.

        **Media Query Examples**

        - *Special Case:* Generated CSS for ``display-small-up``::

            @media only screen and (max-width: 241px) {
                .display-small-up {
                    display: none;
                }
            }

        - *General Usage Case:* Generated CSS for ``padding-100-small-up``::

            @media only screen and (min-width: 241px) {
                .padding-100-small-up {
                    padding: 100px;
                }
            }

        :return: None

        """
        if self.limit_key == '-up':
            lower_limit = str(self.breakpoint_dict[self.breakpoint_key][self.limit_key])

            # Special 'display' usage case min/max reverse logic
            if self.is_display():
                css = (
                    '@media only screen and (max-width: ' + lower_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
            # General usage case
            else:
                css = (
                    '@media only screen and (min-width: ' + lower_limit + ') {\n' +
                    '\t.' + self.css_class + ' {\n' +
                    '\t\t' + self.css_property.cssText + ';\n' +
                    '\t}\n' +
                    '}\n\n'
                )
        else:
            css = ''

        return css

    def build_media_query(self):
        """ Pick the css generation method based on the ``limit_key`` found in ``css_class``.

        :return: Return CSS media queries as CSS Text.

        **Examples:**

        >>> from cssutils.css import Property
        >>> # value='inherit' since we do not know if the class is valid yet.
        >>> name = 'display'
        >>> value = 'inherit'
        >>> priority = ''
        >>> inherit_property = Property(name=name, value=value, priority=priority)
        >>> breakpoint_parser = BreakpointParser(
                css_class='padding-1em-giant-down',
                css_property=inherit_property
            )
        >>> css_property = Property(name='padding', value='1em', priority='')
        >>> if breakpoint_parser.is_breakpoint and css_property.valid:
        >>>     breakpoint_parser.css_property = css_property
        >>>     media_query = breakpoint_parser.build_media_query()
        >>> print(media_query)
        @media only screen and (max-width: 160.0em) {
            .padding-1em-giant-down {
                padding: 1em;
            }
        }

        """
        if self.limit_key in self.limit_key_methods:
            return self.limit_key_methods[self.limit_key]()     # Calls the method in dict.

        return ''
