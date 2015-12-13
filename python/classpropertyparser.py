
# TODO: Wrap in docstrings and make this relevant.
# You instantiate a ``Triangle``
# by providing exactly three lengths ``a``, ``b``, and ``c``.
# They can either be intergers or floating-point numbers,
# and should be listed clockwise around the triangle.
# If the three lengths *cannot* make a valid triangle,
# then ``ValueError`` will be raised instead.
#
# TODO: Show example usage.
#
# >>> from classpropertyparser import ClassPropertyParser
# >>> t = Triangle(3, 4, 5)
# >>> print t.is_equilateral()
# False
# >>> print t.area()
# 6.0
#
# Triangles support the following attributes, operators, and methods.
#
# .. attribute::  a
#                 b
#                 c
#
# .. index:: pair: equality; triangle
# .. method:: triangle1 == triangle2
#
#     Returns true if the two triangles have sides of the same lengths,
#     in the same order.
#     Note that it is okay if the two triangles
#     happen to start their list of sides at a different corner;
#     ``3,4,5`` is the same triangle as ``4,5,3``
#     but neither of these are the same triangle
#     as their mirror image ``5,4,3``.

from cssutils import parseString
from string import ascii_lowercase, digits
from re import findall
# custom
from cssvalueparser import CSSPropertyValueParser
from datalibrary import ordered_property_dict, property_alias_dict, property_regex_dict
from utilities import deny_empty_or_whitespace
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ClassPropertyParser(object):
    def __init__(self, class_set=set(), px_to_em=True):
        """Parser for extracting CSS properties from an HTML Class Attribute.

        CSS Unit Reference: http://www.w3schools.com/cssref/css_units.asp
        CSS Value Reference: http://www.w3.org/TR/CSS21/propidx.html

        :param class_set (set()): set() of potential css properties.
        :param px_to_em (bool): Flag for unit conversion. True means convert ``px` to ``em``. False means do nothing.
        :return: Object of Type ClassPropertyParser
        
        """
        css = u'''/* Generated with blowdrycss. */'''
        self.px_to_em = px_to_em
        self.sheet = parseString(css)
        self.rules = []
        self.importance_designator = '-i'       # '-i' is used to designate that the priority level is '!important'
        self.removed_class_set = set()
        self.class_set = class_set
        self.clean_class_set()
        # print('clean ran')

    def class_set_to_lowercase(self):
        """
        Converts member variable self.class_set to lowercase.

        :return: None
        
        """
        self.class_set = {css_class.lower() for css_class in self.class_set}

    @staticmethod
    def underscores_valid(css_class=''):
        """
        Validate underscore usage in a single css_class.
        In general, underscores are only allowed to designate a decimal point between two numbers.

        **Rules:**
            - Strip all whitespace in front and back.
            - Underscores are only valid between digits
                - ``[0-9]_[0-9]`` allowed
                - ``_35`` not allowed
                - ``42_`` not allowed
                - ``bold_px`` not allowed
            - If found in the middle of a string it may begin and/or end with ``-``
                - ``1_2-5_75-1_2-5_75`` allowed
            - String may start with ``n`` to designate negative numbers.
                - ``n5_25cm`` allowed.
            - String may not start with ``-``
                - ``-7_2`` not allowed.
            - String may not end with ``-``
                - ``5_4-`` not allowed

        :type css_class: str

        :param css_class: Accepts a single CSS class extracted from HTML class attribute.
        :return: boolean

            **True cases:**
                >>> ClassPropertyParser.underscores_valid('6_3')
                True
                >>> ClassPropertyParser.underscores_valid('2_456em')
                True
                >>> ClassPropertyParser.underscores_valid('1_2-5_75-1_2-5_75')
                True
                >>> ClassPropertyParser.underscores_valid('n5_25cm-n6_1cm')
                True

            **False cases:**
                >>> ClassPropertyParser.underscores_valid('-7_2')
                False
                >>> ClassPropertyParser.underscores_valid('5_4-')
                False
                >>> ClassPropertyParser.underscores_valid('_b')
                False
                >>> ClassPropertyParser.underscores_valid('b_')
                False
                >>> ClassPropertyParser.underscores_valid('padding--_2')
                False
                >>> ClassPropertyParser.underscores_valid('2_rem')
                False
                >>> ClassPropertyParser.underscores_valid('m_px')
                False
                >>> ClassPropertyParser.underscores_valid('__')
                False
                
        """
        # TODO: Replace with regex.
        # The underscore and dash is not allowed to be the first or last character of css_class.
        css_class = css_class.strip()                                   # Remove any surrounding whitespace.

        if (css_class[0] == '_' or css_class[-1] == '_' or
            css_class[0] == '-' or css_class[-1] == '-'):
            return False

        # Check character before and after underscore index.
        index = css_class.find('_')
        allowed_before = set(digits)
        allowed_after = set(digits)
        if index > 0:                                                   # Underscore is not the first character.
            valid = set(css_class[index-1]) <= allowed_before           # Check Character before
            valid = valid and set(css_class[index+1]) <= allowed_after  # Check Character after.
        else:
            valid = True

        return valid

    def clean_class_set(self):
        """
        Detect and Remove invalid css classes from class_set
        Class names must abide by: http://www.w3.org/TR/CSS2/syndata.html#characters

        For purposes of this project only a SUBSET of the CSS standard is permissible as follows:
            - Encoded classes shall not be ``None`` or ``''``.
            - Encoded shall not contain whitespace (handled implicitly by subsequent rules).
            - Encoded classes are only allowed to begin with ``[a-z]``
            - Encoded classes are only allowed to end with ``[a-z0-9]``
            - Encoded classes are allowed to contain ``[_a-z0-9-]`` between the first and last characters.
            - Underscores are only valid between digits ``[0-9]_[0-9]``

        **Reference:**
            http://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters

        :return: None
        
        """
        # Normalize class data by setting all strings to lowercase first.
        self.class_set_to_lowercase()

        # Validate against character sets.
        allowed_first = set(ascii_lowercase)
        allowed_middle = set(ascii_lowercase + digits + '_-')
        allowed_last = set(ascii_lowercase + digits)

        # Gather invalid_css_classes
        invalid_css_classes = []
        reasons = []

        # 'continue' is used to prevent the same css_class from being added to the invalid_css_classes multiple times.
        for css_class in self.class_set:
            if not css_class:                                       # None or ''
                invalid_css_classes.append(css_class)
                reasons.append(' (May not be None or "".)')
                continue
            if not set(css_class[0]) <= allowed_first:              # First character
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z allowed for first character of class.)')
                continue
            if not set(css_class) <= allowed_middle:                # All characters
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z, 0-9, "_", and "-" are allowed in class name.)')
                continue
            if not set(css_class[-1]) <= allowed_last:              # Last character
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z and 0-9 allowed for last character of class.)')
                continue
            if not self.underscores_valid(css_class=css_class):     # Underscore
                invalid_css_classes.append(css_class)
                reasons.append(' (Invalid underscore usage in class.)')
                continue

        # Remove invalid_css_classes from self.class_set
        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.class_set.remove(invalid_css_class)
            self.removed_class_set.add(invalid_css_class + reasons[i])

    # Property Name Section
    #
    @staticmethod
    def get_property_name(css_class=''):
        """
        Extract a property name from a given class.

        **Rules:**
            - Classes that use css property names or aliases must set a property value.

        **Valid:**
            - ``font-weight-700`` is valid because ``700`` is a valid property value.
            - ``fw-700`` is valid because it ``fw-`` is a valid alias for ``font-weight``
            - ``bold`` is valid because the ``bold`` alias implies a property name of ``font-weight``

        **Invalid:**
            - ``font-weight`` by itself is a property name, but does not include a property value.
            - ``fw-`` by itself is a property alias, but does not include a property value.
            - ``700`` does imply ``font-weight``, but is not a valid CSS selector as it may not begin with a number.

        :type css_class: str

        :param css_class: A class name containing a property name and value pair, or just a property value from which the property name may be inferred.
        :return: (str) -- Class returns the property_name OR if unrecognized returns ``''``.
        
        """
        for property_name, aliases in ordered_property_dict.items():
            # Try identical 'key' match first. An exact css_class match must also end with a '-' dash to be valid.
            if css_class == property_name or css_class == (property_name + '-'):    # No property value included.
                return ''

            if css_class.startswith(property_name + '-'):
                return property_name

            # Sort the aliases by descending string length
            # This is necessary when the css_class == 'bolder' since 'bold' appears before 'bolder'
            aliases = sorted(aliases, key=len, reverse=True)

            # Try matching with alias. An alias is not required to end with a dash, but could if it is an abbreviation.
            for alias in aliases:
                if css_class == alias and alias.endswith('-'):                      # No property value included.
                    return ''
                if css_class.startswith(alias):
                    return property_name

            # Try matching a regex pattern.
            try:
                regexes = property_regex_dict[property_name]
                for regex in regexes:
                    if len(findall(regex, css_class)) == 1:
                        return property_name
            except KeyError:
                pass

        # No match found.
        return ''

    @staticmethod
    def strip_property_name(property_name='', css_class=''):
        """
        Strip property name from css_class if applicable and return the css_class.

        :raises ValueError: If either property_name or css_class are empty or only contain whitespace values.

        :type property_name: str
        :type css_class: str

        :param property_name: Presumed to match a key or value in the ``property_alias_dict``.
        :param css_class: This value may or may not be identical to the property_value.
        :return: (str) css_class which is the encoded property value.

        **Examples:**

        >>> ClassPropertyParser.strip_property_name('padding', 'padding-1-2-1-2')
        '1-2-1-2'
        >>> ClassPropertyParser.strip_property_name('font-weight', 'bold')
        'bold'
        >>> ClassPropertyParser.strip_property_name('', 'padding-1-2-1-2')
        ValueError
        >>> ClassPropertyParser.strip_property_name('font-weight', '    ')
        ValueError
        
        """
        deny_empty_or_whitespace(string=css_class, variable_name='css_class')
        deny_empty_or_whitespace(string=property_name, variable_name='property_name')

        property_name += '-'                                        # Append '-' to property to match the class format.

        if css_class.startswith(property_name):                     # Strip property name
            return css_class[len(property_name):]
        else:                                                       # If it doesn't have a property name ignore it.
            return css_class

    @staticmethod
    def alias_is_abbreviation(possible_alias=''):
        """
        Detects if the alias is an abbreviation e.g. ``fw-`` stands for ``font-weight-``.
        Abbreviated aliases are found in ``datalibrary.property_alias_dict``.

        :type possible_alias: str

        :param possible_alias: A value that might be an alias.
        :return: (bool) -- True if possible_alias ends with a dash ``-``.

        **Examples:**

        >>> ClassPropertyParser.alias_is_abbreviation('fw-')
        True
        >>> ClassPropertyParser.alias_is_abbreviation('bold')
        False
        
        """
        return possible_alias.endswith('-')

    def get_property_abbreviations(self, property_name=''):
        """
        Returns a list of all property abbreviations appearing in ``property_alias_dict``.

        :raises KeyError: If ``property_name`` is not found in ``property_alias_dict``.

        :param property_name:
        :return: (list) -- A list of all property abbreviations appearing in ``property_alias_dict``.

        **Example:**

        Assume the following key, value pair occurs in ``property_alias_dict``:

            ``'background-color': {'bgc-', 'bg-c-', 'bg-color-', },``

        >>> ClassPropertyParser.get_property_abbreviations('background-color')
        ['bgc-', 'bg-c-', 'bg-color-']
        >>> ClassPropertyParser.get_property_abbreviations('invalid_property_name')
        KeyError
        
        """
        property_abbreviations = list()
        for alias in property_alias_dict[property_name]:
            if self.alias_is_abbreviation(possible_alias=alias):
                property_abbreviations.append(alias)
        return property_abbreviations

    def strip_property_abbreviation(self, property_name='', encoded_property_value=''):
        """
        Strip property abbreviation from encoded_property_value if applicable and return encoded_property_value.

        Both property_name and encoded_property_value must not be empty or only contain whitespace values.

        :type property_name: str
        :type encoded_property_value: str

        :param property_name: Presumed to match a key or value in the ``property_alias_dict``
        :param encoded_property_value: Initially this value may or may not contain the property_name.
        :return: (str) --
        
        """
        deny_empty_or_whitespace(string=encoded_property_value, variable_name='encoded_property_value')
        deny_empty_or_whitespace(string=property_name, variable_name='property_name')

        property_abbreviations = self.get_property_abbreviations(property_name=property_name)

        for property_abbreviation in property_abbreviations:
            if encoded_property_value.startswith(property_abbreviation):
                return encoded_property_value[len(property_abbreviation):]
        return encoded_property_value

    # Property Value
    #
    def get_encoded_property_value(self, property_name='', css_class=''):
        """
        Strip property name or alias abbreviation prefix from front, and property priority designator from end.

        Examples
            'fw-bold-i' --> 'bold'                [abbreviated font-weight property_name]
            'padding-1-10-10-5-i' --> '1-10-10-5' [standard property_name]
            'height-7_25rem-i' --> '7_25rem'      [contains underscores]

        The term encoded_property_value means a property value that may or may not contain dashes and underscores.

        :type property_name: str
        :type css_class: str

        :param property_name: Name of CSS property that matches a key in ``property_alias_dict``.
        :param css_class: An encoded class that may contain property name, value, and priority designator.
        :return: (str) --
        
        """
        encoded_property_value = css_class
        encoded_property_value = self.strip_property_name(property_name, encoded_property_value)
        encoded_property_value = self.strip_property_abbreviation(property_name, encoded_property_value)
        encoded_property_value = self.strip_priority_designator(encoded_property_value)
        return encoded_property_value

    def get_property_value(self, property_name='', encoded_property_value=''):
        """
        Accepts an encoded_property_value that's been stripped of it's property named and priority
        Uses CSSPropertyValueParser, and returns a valid css property value or ''.

        encoded_property_value examples
            'bold'      [special case where alias == property value]
            '1-10-10-5' [contains dashes]
            '7_25rem'   [contains underscores]

        :type property_name: str
        :type encoded_property_value: str

        :param property_name: Name of CSS property that matches a key in ``property_alias_dict``.
        :param encoded_property_value: A property value that may or may not contain dashes and underscores.
        :return: str
        
        """
        value_parser = CSSPropertyValueParser(property_name=property_name, px_to_em=self.px_to_em)
        value = value_parser.decode_property_value(value=encoded_property_value)
        return value

    # Property Priority
    #
    def is_important(self, css_class=''):
        """
        Tests whether the css_class ends with the importance_designator.

        Returns True if the css_class ends with the importance_designator. Otherwise, it returns False.

        :type css_class: str

        :param css_class: An encoded class that may contain property name, value, and priority designator.
        :return: (bool) --
        
        """
        return css_class.endswith(self.importance_designator)

    def strip_priority_designator(self, encoded_property_value=''):
        """
        Strip priority designator from the end of encoded_property_value and returns the string.  If the
        importance_designator is not found it returns the unchanged encoded_proprety_value.

        :type encoded_property_value: str

        :param encoded_property_value: A property value that may or may not contain a priority designator.
        :return: (str) --
        
        """
        if self.is_important(css_class=encoded_property_value):
            return encoded_property_value[:-len(self.importance_designator)]
        else:
            return encoded_property_value

    def get_property_priority(self, css_class=''):
        """
        Returns the keyword 'IMPORTANT' if the property priority is set to important. Otherwise, it returns ''.

        :type css_class: str

        :param css_class: An encoded class that may contain property name, value, and priority designator.
        :return: (str) --
        
        """
        return 'IMPORTANT' if self.is_important(css_class=css_class) else ''
