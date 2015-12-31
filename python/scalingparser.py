# custom
from utilities import deny_empty_or_whitespace
from unitparser import UnitParser
from settings import small, medium
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# TODO: Handle negative numbers, or list as unsupported.
# TODO: Should it be possible to switch between scaling up and scaling down?
class ScalingParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Scaling Flag:**

    Append ``'-s'`` to the end of an encoded property values to scale the value up and down based on screen size.

    Note: This only works on property values containing distance--based units (pixels, em, etc).

    - General format: ``<name>-<value>-s``

    - Specific case: ``font-size-24-s``

    - Priority ``!important`` case: ``font-size-24-s-i``

        - (``'-i'`` *is always last*)

    **Responsive Scaling Ratios:**

    - Assuming ``font-size-24-s`` is the encoded css class, the font-size will respond to the screen size according
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
    :param use_em: A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion (default).
        False disables unit conversions meaning any pixel value remains unchanged.
    :return: None

    **Examples:**

    >>> 'WARNING: NOT IMPLEMENTED YET'

    """
    def __init__(self, css_class='', name=''):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace(name, variable_name='name')

        self.css_class = css_class
        self.name = name
        self.scale_dict = {
            'medium': 1.125,
            'small': 1.25,
        }
        self.scaling_flag = '-s'

    def is_scaling(self):
        """ Return False if ``self.property_name`` does not have default units of ``'px'``.
        Test if ``self.css_class`` contains the scaling flag ``-s``. Returns True if ``-s`` is found and
        False otherwise.

        **Rules:**

        - The ``self.property_name`` must possess units of pixels ``'px'``.
        - If no property priority is set the encoded ``css_class`` must end with ``-s``.
        - If priority is set the encoded ``css_class`` must end with ``-s-i``.

        :return: (*bool*) -- Returns True if ``-s`` is found and False otherwise.

        **Examples**

        >>> scaling_parser = ScalingParser(css_class='font-weight-24-s')
        >>> scaling_parser.is_scaling()
        True
        >>> scaling_parser.css_class = 'font-weight-24-s-i'
        >>> scaling_parser.is_scaling()
        True
        >>> scaling_parser.css_class = 'font-weight-24'
        >>> scaling_parser.is_scaling()
        False

        """
        unit_parser = UnitParser(property_name=self.name)
        if unit_parser.default_units() != 'px':
            return False
        else:
            return self.css_class.endswith(self.scaling_flag) or self.css_class.endswith(self.scaling_flag + '-i')

    def strip_scaling_flag(self):
        """ Remove the ``scaling_flag`` from ``css_class`` if possible and return the clean css class. Otherwise,
        return the ``css_class`` unchanged.

        **Rules**

        - Remove ``-s`` if found at end of a string
        - Remove ``-s`` if ``-s-i`` is found at the end of the string.

        :return: (*str*) -- If the ``css_class`` is scaling remove the ``scaling_flag`` and return the clean css class. Otherwise,
        return the ``css_class`` unchanged.

        **Examples:**

        >>> scaling_parser = ScalingParser(css_class='font-size-32-s', name='font-size')
        >>> scaling_parser.strip_scaling_flag()
        font-size-32
        >>> scaling_parser.css_class = 'font-size-56-s-i'
        >>> scaling_parser.strip_scaling_flag()
        font-size-56-i
        >>> scaling_parser.css_class = 'font-size-14'
        >>> scaling_parser.strip_scaling_flag()
        font-size-14

        """
        if self.css_class.endswith(self.scaling_flag):
            return self.css_class[:-2]
        if self.css_class.endswith(self.scaling_flag + '-i'):
            return self.css_class[:-4] + '-i'

        return self.css_class

    def build_media_query(self, value='', css_text=''):
        """ Returns CSS media queries that scales pixel / em values in response to screen size changes.

        **Generated CSS for ``font-size-24-s`` minus the inline comments**::

            .font-size-24-s {
                // Default size above medium
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

        **Priority !important -- Generated CSS for ``font-size-24-s-i`` minus the inline comments**::

            .font-size-24-s-i {
                // Default size above medium
                font-size: 24px !important;

                // medium screen font size reduction
                @media only screen and (max-width: 720px) {
                    font-size: 21.3px !important;
                }

                // small screen font size reduction
                @media only screen and (max-width: 480px) {
                    font-size: 19.2px !important;
                }
            }

        :param css_text:
        :type value: str

        :param value: A string that consists of digits and units of either ``px`` or ``em``
            e.g. ``'17px'`` or ``'15.0625em'``.
        :return: (*str*) -- Returns CSS media queries that scales pixel / em values in response to screen size changes.

        """
        deny_empty_or_whitespace(str(value), variable_name='value')
        float_value = float(value.replace('em', '').replace('px', ''))          # Remove units

        if 'em' in value:                                                       # Get units
            units = 'em'
        elif 'px' in value:
            units = 'px'
        else:
            units = ''

        _max = 1
        small_max = small[_max]
        medium_max = medium[_max]

        medium_value = round(float_value / self.scale_dict['medium'], 4)        # Scale to medium screen
        medium_value = str(medium_value) + units                                # Re-apply units
        small_value = round(float_value / self.scale_dict['small'], 4)          # Scale to small screen
        small_value = str(small_value) + units                                  # Re-apply units

        return (
            '.' + self.css_class + ' {\n' +
            '\t' + css_text + '\n\n' +
            '\t@media only screen and (max-width: ' + medium_max + ') {\n' +
            '\t\t' + self.name + ': ' + medium_value + ';\n' +
            '}\n\n' +
            '\t@media only screen and (max-width: ' + small_max + ') {\n' +
            '\t\t' + self.name + ': ' + small_value + ';\n' +
            '\t}\n' +
            '}\n\n'
        )
