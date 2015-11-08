from cssutils import parseString
from string import ascii_lowercase, digits
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ClassPropertyParser(object):
    # Class Format Legend
    # Dashes separate word in multi-word property names/aliases.
    # property-name
    # font-weight
    #
    # Dashes separate CSS property_name/alias from property_value
    # alias-value
    # font-weight-700
    #
    # Dashes separate multiple values for properties that take multiple values.
    # alias-value-value-value-value
    # padding-10-20-10-10
    #
    # Dashes separate !important priority indicator '-i' (append to the end of the string)
    # alias-value-i
    # font-weight-bold-i
    #
    # Shorthand can be used in cases where the alias is the unambiguously the value.
    # alias = value
    # font-weight-bold OR bold OR b
    # font-weight-bold-i OR bold-i OR b-i
    def __init__(self, class_set=set()):
        css = u'''/* Generated with BlowDryCSS. */'''
        self.sheet = parseString(css)
        self.rules = []
        self.class_set = class_set
        self.clean_class_set()

        # TODO: move this to a CSV file and autogenerate this dictionary from CSV.
        # Dictionary contains:
        #   css property name as keys
        #   aliases as values - An alias can be thought of as a shorthand means of
        self.property_dict = {
            'font-weight': ['normal', 'b', 'bold', 'bolder', 'lighter', 'initial', 'inherit', 'fw', 'font-weight']
        }

    # Take list, tuple, or set of strings an convert to lowercase.
    def class_set_to_lowercase(self):
        self.class_set = {css_class.lower() for css_class in self.class_set}

    # Underscores are only allowed to designate a decimal point between numbers.
    #   Valid: '6_3'
    # Invalid: '-_2", '2_rem', 'm_px', and '__'
    @staticmethod
    def underscores_valid(css_class=''):
        # underscore is not allowed to be the first or last character of css_class
        if css_class[0] != '_' != css_class[-1]:
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

    # Detect and Remove invalid css classes from class_set
    # Class names must abide by: http://www.w3.org/TR/CSS2/syndata.html#characters
    # For purposes of this library only a SUBSET of the standard is permissible as follows:
    # Classes are only allowed to begin with [a-z]
    # Classes are only allowed to end with [a-z0-9]
    # Classes are allowed to contain [_a-z0-9-]
    # Underscores are only allowed between digits [0-9]
    # Reference: stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
    def clean_class_set(self):
        # Set all strings to lowercase first.
        self.class_set_to_lowercase()

        # Validate against character sets.
        allowed_first = set(ascii_lowercase)
        allowed_middle = set(ascii_lowercase + digits + '_-')
        allowed_last = set(ascii_lowercase + digits)

        # Gather invalid_css_classes
        invalid_css_classes = set()
        for css_class in self.class_set:
            if not set(css_class[0]) <= allowed_first:              # First character
                invalid_css_classes.add(css_class)
            if not set(css_class) <= allowed_middle:                # All characters
                invalid_css_classes.add(css_class)
            if not set(css_class[-1]) <= allowed_last:              # Last character
                invalid_css_classes.add(css_class)
            if not self.underscores_valid(css_class=css_class):     # Underscore
                invalid_css_classes.add(css_class)

        # Remove invalid_css_classes from self.class_set
        for invalid_css_class in invalid_css_classes:
            self.class_set.remove(invalid_css_class)

    def get_property_name(self, css_class=''):
        for property_name, aliases in self.property_dict.items():
            # Try exact match first. An exact match must also end with a '-' dash to be valid.
            if css_class.startswith(property_name + '-'):
                return property_name
            # Try matching with alias
            for alias in aliases:
                if css_class.startswith(alias):
                        return property_name
            # No match found
            return ''

    # Strip property name and priority from a given css_class and return encoded_property_value
    # '-i' is used to designate that the priority level is '!important'
    @staticmethod
    def get_encoded_property_value(self, property_name='', css_class=''):
        encoded_property_value = css_class
        important = '-i'

        # Deny empty string. If it doesn't have a property name ignore it.
        # Wrap in try/catch to allow user to define custom css classes.
        if property_name == '':
            raise ValueError('CSS property_name cannot be empty.')
        # Append '-' to property to match the class format.
        else:
            property_name += '-'

        # Strip property name
        if encoded_property_value.startswith(property_name):
            encoded_property_value = encoded_property_value[len(property_name):]

            # Strip priority designator
            if encoded_property_value.endswith(important):
                encoded_property_value = encoded_property_value[:-len(important)]

        return encoded_property_value

    # Accepts an encoded_property_value that's been stripped of it's property named and priority
    # Returns the property value.
    def get_property_value(self, encoded_property_value=''):
        # TODO: Call CSSPropertyValueParser
        return ''

    @staticmethod
    def get_property_priority(self, css_class=''):
        if css_class.endswith('-i'):
            return 'IMPORTANT'
        else:
            return ''


# Accepts a clean encoded_property_value.
# Generates a valid css property_value
class CSSPropertyValueParser(object):
    def __init__(self, encoded_property_value=''):
        if not '-' in encoded_property_value:
            self.property_value = encoded_property_value
        else:
            # TODO: Handle values and units 12px or 1o32rem or 25p
            pass

    # '-' becomes spaces    example: 1-5-1-5 --> 1 5 1 5
    def replace_dashes(self):
        self.property_value.replace('-', ' ')

    # '_' becomes '.'   example: 1_32rem --> 1.32rem
    def replace_underscore(self):
        self.property_value.replace('_', '.')

    # TODO: handle percentage case i.e. padding-1p-10p-3p-1p --> 1% 10% 3% 1%

    # convert px to rem
    def px_to_em(self, px):
        # TODO: write this.
        pass