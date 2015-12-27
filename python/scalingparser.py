# custom
from utilities import deny_empty_or_whitespace
from unitparser import UnitParser
from datalibrary import small, medium
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

    - Generated CSS for ``font-size-24-s``::

        .font-size-24-s {
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
    def __init__(self, css_class='', name='', px_to_em=True):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace(name, variable_name='name')

        self.css_class = css_class
        self.name = name
        self.px_to_em = px_to_em

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
        unit_parser = UnitParser(property_name=self.name, use_em=self.px_to_em)
        if unit_parser.default_units() != 'px':
            return False
        else:
            return self.css_class.endswith('-s') or self.css_class.endswith('-s-i')

    def generate_scaling_css(self, value):
        deny_empty_or_whitespace(value, variable_name='value')

        _max = 1
        small_max = small[_max]
        medium_max = medium[_max]
        pass
