from cssutils import parseString
from string import ascii_lowercase, digits
from collections import OrderedDict
# Custom
from cssvalueparser import CSSPropertyValueParser
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
    #
    # Declaring colors:
    #  rgb: font-color-rgb-0-255-0
    # rgba: font-color-rgba-255-0-0-0_5
    #  hex: font-color-h0ff23f (prepend 'h')
    #  hsl: font-color-hsl-120-60p-70p
    # hsla: font-color-hsla-120-60p-70p-0_3
    #
    # CSS Unit Reference: http://www.w3schools.com/cssref/css_units.asp
    # CSS Value Reference: http://www.w3.org/TR/CSS21/propidx.html
    def __init__(self, class_set=set()):
        css = u'''/* Generated with BlowDryCSS. */'''
        self.sheet = parseString(css)
        self.rules = []
        self.css_units = {'px', 'em', 'rem', 'p', 'ex', 'cm', 'mm', 'in', 'pt', 'pc', 'ch', 'vh', 'vw', 'vmin', 'vmax'}
        self.importance_designator = '-i'       # '-i' is used to designate that the priority level is '!important'
        self.removed_class_set = set()
        self.class_set = class_set
        self.clean_class_set()
        print('clean ran')

        # TODO: create function that validates dictionary ensuring that no aliases clash.
        # TODO: move this to a CSV file and autogenerate this dictionary from CSV.
        # Dictionary contains:
        #   css property name as 'keys'
        #   list of aliases as 'values' - An alias can be shorthand for the property name.
        self.property_dict = {
            'background-color': ['bgc-', 'bg-c-', 'bg-color-', ],
            'color': ['c-', ],
            'font-size': ['fsize-', 'f-size-', 'fs-', ],
            'font-weight': ['normal', 'bold', 'bolder', 'lighter', 'initial', 'fweight-', 'f-weight-', 'fw-', ],
            'height': ['h-', ],
            'margin': ['m-', ],
            'margin-top': ['m-top-', 'mt-', ],
            'padding': ['p-', ],
            'padding-top': ['p-top-', 'pt-', ],
            'text-align': ['talign-', 't-align-', ],
            'vertical-align': ['valign-', 'v-align-', ],
            'width': ['w-', ],
        }

        # TODO: explore another way using regex for property (no cssutils already does regex validation)
        # allowed = self.allowed_unit_characters()
        # self.property_dict = {
        #     'font-weight': [['normal', 'bold', 'bolder', 'lighter', 'initial', 'fw-'], r"([0-9a-z-])"],
        #     'padding': [['p-'], r"([0-9" + allowed + "_-])"],
        #     'height': [['h-'], r"([0-9" + allowed + "_-])"],
        # }

    # Reduces css_units to a minimum set of allowed characters.
    # Used in property_dict regex.
    # Example: converts {'px', 'em', 'rem'} --> 'pxemr' thus eliminating duplicate 'e' and 'm'
    # def allowed_unit_characters(self):
    #     allowed = ''
    #     for css_unit in self.css_units:
    #         allowed += css_unit
    #     return allowed

    # Take list, tuple, or set of strings an convert to lowercase.
    def class_set_to_lowercase(self):
        self.class_set = {css_class.lower() for css_class in self.class_set}

    # Validate underscore usage in a single css_class.
    # Underscores are only allowed to designate a decimal point between numbers.
    #   Valid: '6_3'
    # Invalid: '_b', 'b_', 'padding-_2", '2_rem', 'm_px', and '__'
    @staticmethod
    def underscores_valid(css_class=''):
        # underscore is not allowed to be the first or last character of css_class
        if css_class[0] == '_' or css_class[-1] == '_':
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
        invalid_css_classes = []
        reasons = []

        # 'continue' is used to prevent the same css_class from being added to the invalid_css_classes multiple times.
        for css_class in self.class_set:
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

    # Property Name
    #
    # Class returns the property_name or removes/cleans the unrecognized class and returns ''.
    # Classes that use identical property names must set a property value
    # i.e. 'font-weight' is invalid because no value is included AND 'font-weight-700' is valid because 700 is a value.
    def get_property_name(self, css_class=''):
        # Sort property_dict with the longest items first as the most verbose match is preferred.
        # i.e. If css_class == 'margin-top' Then we want it to match the property_dict key 'margin-top' not 'margin'
        # TODO: Instead of doing this multiple times do it once in self.property_dict.
        ordered_property_dict = OrderedDict(sorted(self.property_dict.items(), key=lambda t: len(t[0]), reverse=True))

        for property_name, aliases in ordered_property_dict.items():
            # Try identical key match first. An exact css_class match must also end with a '-' dash to be valid.
            if css_class.startswith(property_name + '-'):
                return property_name

            # Sort the aliases by descending string length
            # This is necessary when the css_class == 'bolder' since 'bold' appears before 'bolder'
            # TODO: Instead of doing this multiple times do it once in self.property_dict.
            aliases = sorted(aliases, key=len, reverse=True)

            # Try matching with alias. An alias is not required to end with a dash, but could if it is an abbreviation.
            for alias in aliases:
                if css_class.startswith(alias):
                    return property_name

        # No match found. Remove from class_set.
        # self.class_set.remove(css_class)
        # self.removed_class_set.add(css_class + ' (Property name does not match patterns in self.property_dict.)')
        return ''

    # Strip property name from encoded_property_value if applicable and return encoded_property_value.
    @staticmethod
    def strip_property_name(property_name='', encoded_property_value=''):
        # Deny empty string. If it doesn't have a property name ignore it.
        if property_name == '':
            raise ValueError('CSS property_name cannot be empty.')
        # Append '-' to property to match the class format.
        else:
            property_name += '-'

        # Strip property name
        if encoded_property_value.startswith(property_name):
            return encoded_property_value[len(property_name):]
        else:
            return encoded_property_value

    # Some alias could be abbreviations e.g. 'fw-' stands for 'font-weight-'
    # In these cases a dash is added in the dictionary to indicate an abbreviation.
    @staticmethod
    def alias_is_abbreviation(alias=''):
        return alias.endswith('-')

    # Returns a list of all property abbreviations appearing in property_dict
    def get_property_abbreviations(self, property_name=''):
        property_abbreviations = list()
        for alias in self.property_dict[property_name]:
            if self.alias_is_abbreviation(alias=alias):
                property_abbreviations.append(alias)
        return property_abbreviations

    # Strip property abbreviation from encoded_property_value if applicable and return encoded_property_value.
    def strip_property_abbreviation(self, property_name='', encoded_property_value=''):
        property_abbreviations = self.get_property_abbreviations(property_name=property_name)

        for property_abbreviation in property_abbreviations:
            if encoded_property_value.startswith(property_abbreviation):
                return encoded_property_value[len(property_abbreviation):]
        return encoded_property_value

    # Property Value
    #
    # Valid encoded_property_values: '1p-2p-1p-1p', '5rem', '6ex', 'bold'
    # def encoded_property_value_is_valid(self, encoded_property_value):
    #     for value in self.text_only_values:
    #         if encoded_property_value == value:
    #             return True
    #         handle suffix

    # Strip property name or abbreviation prefix and property priority designator
    # Examples:
    # 'fw-bold-i' --> 'bold'                [abbreviated font-weight property_name]
    # 'padding-1-10-10-5-i' --> '1-10-10-5' [standard property_name]
    # 'height-7_25rem-i' --> '7_25rem'      [contains underscores]
    # The term encoded_property_value means a property value that may or may not contain dashes and underscores.
    def get_encoded_property_value(self, property_name='', css_class=''):
        encoded_property_value = css_class
        encoded_property_value = self.strip_property_name(property_name, encoded_property_value)
        encoded_property_value = self.strip_property_abbreviation(property_name, encoded_property_value)
        encoded_property_value = self.strip_priority_designator(encoded_property_value)
        return encoded_property_value

    # Accepts an encoded_property_value that's been stripped of it's property named and priority
    # Returns a valid css property value or ''.
    def get_property_value(self, css_class='', property_name='', encoded_property_value='', property_priority=''):
        property_parser = CSSPropertyValueParser()
        value = property_parser.decode_property_value(property_name=property_name, value=encoded_property_value)
        return value
        # if property_parser.property_is_valid(name=property_name, value=value, priority=property_priority):
        #     return value
        #
        # # property_value is invalid
        # self.class_set.remove(css_class)
        # self.removed_class_set.add(css_class + ' (cssutils declared property value invalid.)')
        # return ''

    # Property Priority
    #
    def is_important(self, css_class=''):
        return css_class.endswith(self.importance_designator)

    # Strip priority designator from the end of encoded_property_value.
    def strip_priority_designator(self, encoded_property_value=''):
        if self.is_important(css_class=encoded_property_value):
            return encoded_property_value[:-len(self.importance_designator)]
        else:
            return encoded_property_value

    def get_property_priority(self, css_class=''):
        return 'IMPORTANT' if self.is_important(css_class=css_class) else ''
