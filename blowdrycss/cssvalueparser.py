# python 2
from __future__ import absolute_import
# plugins
from cssutils.css import Property
from xml.dom import SyntaxErr
# custom
from blowdrycss.utilities import contains_a_digit
from blowdrycss.datalibrary import property_alias_dict
from blowdrycss.colorparser import ColorParser
from blowdrycss.fontparser import FontParser
from blowdrycss.unitparser import UnitParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class CSSPropertyValueParser(object):
    """
    Accepts a ``property_name`` and ``use_em`` unit conversion flag.

    Contains multiple parsers and methods that decodes the CSS property_value.

    :type property_name: str

    :param property_name: A CSS property name.
    :return: None

    **Attributes:**

    **property_name** (*str*) -- A CSS property name. Not allowed to be ``''`` or None.

    **color_parser** (*ColorParser*) -- Parses encoded color values.

    **unit_parser** (*UnitParser*) -- Parses encoded unit values, and handles unit conversion.

    **Important note about methods:**

    These methods are intended to be called in the order they are defined inside the class.

    """

    def __init__(self, property_name=''):
        self.property_name = property_name
        self.color_parser = ColorParser(property_name=property_name)
        self.unit_parser = UnitParser(property_name=property_name)

    def is_built_in(self, value=''):
        """ Checks if the encoded ``value`` identically matches a value built-in to the CSS standard.
        Returns True if ``value`` matches a CSS built-in valued and False if it does not.

        Examples include: 'bold', 'italic', 'w-resize', 'arial', etc.

        :type value: str

        :param value: Encoded CSS property value.
        :return: (*bool*)

            - Returns ``True`` if ``value`` matches a CSS built-in valued and ``False`` if it does not.
            - The values 'bold', 'italic', 'w-resize', 'arial' all return ``True``.
            - The values '-bold', 'fw-', 'color-' all return ``False``.
            - Invalid ``self.property_name`` also returns ``False`` (KeyError Case).

        **Examples:**

        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='font-weight', use_em=True
        >>> )
        >>> value_parser.is_built_in('bold')
        True
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.is_built_in('7-4-7-4')
        False
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='InvalidCSSPropertyName', use_em=True
        >>> )
        >>> value_parser.is_built_in('italic')
        False

        """
        if value.startswith('-') or value.endswith('-'):
            return False
        try:
            aliases = property_alias_dict[self.property_name]
            return True if value in aliases else False
        except KeyError:
            return False

    @staticmethod
    def replace_dashes(value=''):
        """ Remove leading and trailing dashes. Replace internal dashes with spaces. Return the modified value.

        ``-`` becomes either ``''`` or ``' '``.

        :type value: str

        :param value: Encoded CSS property value.
        :return: (*str*) -- Return the value with dashes removed if necessary.

        >>> # Delete leading dash '-bold' --> 'bold'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='font-weight', use_em=True
        >>> )
        >>> value_parser.replace_dashes('-bold')
        'bold'
        >>> #
        >>> # Delete trailing 'white-' --> 'white'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='color', use_em=True
        >>> )
        >>> value_parser.replace_dashes('white-')
        'white'
        >>> #
        >>> # Replace internal '1-5-1-5' --> '1 5 1 5'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.replace_dashes('1-5-1-5')
        '1 5 1 5'

        """
        value = value[1:] if value.startswith('-') else value
        value = value[:-1] if value.endswith('-') else value
        return value.replace('-', ' ')

    @staticmethod
    def replace_underscore_with_decimal(value=''):
        """ Replace underscore with decimal point. Underscores are used to encode a decimal point

        ``'_'`` becomes ``'.'``

        :type value: str

        :param value: Encoded CSS property value.
        :return: (*str*) -- Return the value with decimal points added if necessary.

        **Example**

        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.replace_underscore_with_decimal('1_32rem')
        '1.32rem'

        """
        if contains_a_digit(string=value):
            value = value.replace('_', '.')
        return value

    @staticmethod
    def replace_p_with_percent(value=''):
        """ Replace ``'p'`` suffix with ``'%'`` if found at the end of any substring containing digits.

        ``'p '`` becomes ``'%'``

        Mind the space

        :type value: str

        :param value: Encoded CSS property value.
        :return: (*str*) -- Return the value with percent signs added if necessary.

        **Example:**

        >>> # Multi-value: '1p 10p 3p 1p' --> '1% 10% 3% 1%'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.replace_p_with_percent(value='1p 10p 3p 1p')
        '1% 10% 3% 1%'
        >>> #
        >>> # Single value ' 1p' --> ' 1%'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.replace_p_with_percent(value=' 1p')
        ' 1%'

        """
        if contains_a_digit(string=value):
            value = value.replace('p ', '% ')
            if value.endswith('p'):
                value = value[:-1] + '%'    # chop last character and add percentage sign
        return value

    @staticmethod
    def replace_n_with_minus(value=''):
        """ If a space plus the letter ``' n'`` is immediately followed by a digit replace it with ``' -'``.
        If ``n`` is the first letter of the string and followed by digits replace it with ``-``.
        The letter ``n`` is an encoding for a negative sign. Leaves other ``n's`` unmodified.

        | ``' n2'`` becomes ``' -2'``  Mind the space.
        | ``'n5'`` becomes ``'-5'``

        :type value: str

        :param value: Encoded CSS property value.
        :return: (*str*) -- Return the value with minus signs added if necessary.

        **Example:**

        >>> # Multi-value: 'n5cm n6cm' --> '-5cm -6cm'
        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.replace_n_with_minus('n5cm n6cm')
        '-5cm -6cm'
        >>> #
        >>> # 'n9in' --> '-9in' (note that the 'n' at the end is not touched)
        >>> value_parser.replace_n_with_minus('n9in')
        '-9in'

        """
        if contains_a_digit(string=value):
            value = value.replace(' n', ' -')
            if value.startswith('n'):
                value = '-' + value[1:]     # add minus sign and chop first character
        return value

    # Put everything together.
    def decode_property_value(self, value=''):
        """
        Decode the encoded property ``value`` input e.g. 'bold', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px',
        'n5_25cm-n6_1cm'. Returns parsed, but non-validated CSS property value.

        :type value: str

        :param value: An encoded CSS property value.
        :return: (*str*) -- Returns the decoded, but non-validated CSS property value.

        **Examples:**

        >>> value_parser = CSSPropertyValueParser(
        >>>     property_name='padding', use_em=True
        >>> )
        >>> value_parser.decode_property_value(value='1-5-1-5')
        '0.0625em 0.3125em 0.0625em 0.3125em'
        >>> value_parser.unit_parser.use_em = False
        >>> value_parser.decode_property_value(value='1-5-1-5')
        '1px 5px 1px 5px'

        """

        # Skip values that are built-in to the CSS standard, and represent the literal property value.
        if not self.is_built_in(value=value):
            # Apply to all non-built-in values.
            value = self.replace_dashes(value=value)

            # These only apply if value contains a digit.
            value = self.replace_underscore_with_decimal(value=value)
            value = self.replace_p_with_percent(value=value)
            value = self.replace_n_with_minus(value=value)

            # Parse color and units
            value = self.color_parser.replace_h_with_hash(value=value)
            value = self.color_parser.add_color_parenthetical(value=value)
            value = self.unit_parser.add_units(property_value=value)
        else:
            # Generate web safe font-family fallback strings.
            if self.property_name == 'font-family':
                font_parser = FontParser(font_value=value)
                value = font_parser.generate_fallback_fonts()
        return value

    @staticmethod
    def property_is_valid(name='', value='', priority=''):
        """ Detects if a given property name, value, and priority combination is valid. Returns True if the
        combination is valid, and false otherwise.

        Validation occurs after the property value is decoded.

        :param name: CSS property name
        :param value: Decoded CSS property value
        :param priority: CSS priority designator
        :return: (*bool*) -- Returns True if the CSS property name, value, and priority
            combination is valid, and false otherwise.

        **Examples:**

        >>> value_parser = CSSPropertyValueParser()
        >>> value_parser.property_is_valid(
        >>>     name='padding', value='1px', priority=''
        >>> )
        True
        >>> value_parser.property_is_valid(
        >>>     name='padding', value='invalid', priority=''
        >>> )
        False

        """
        try:
            css_property = Property(name=name, value=value, priority=priority)
            is_valid = css_property.valid
            return is_valid
        except SyntaxErr:
            return False

# TODO: Are URIs ridiculous? or should we implement syntax.  For now YES they are ridiculous
# background-image-url-image.png --> background-image: url("image.png")
# background-image-url-_home_images_sample_image.png --> background-image: url("/home/images/sample/image.png")
# IN THE LAST CASE images with underscores would not work could use a double underscore to represent final directory
# but this is getting ridiculous example double underscore signifies final directory
# allowing underscore in file name:
# background-image-url-_home_images_sample__image_1.png --> background-image: url("/home/images/sample/image_1.png")
