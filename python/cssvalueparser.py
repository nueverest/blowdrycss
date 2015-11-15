from re import search, findall
from cssutils.css import Property
from xml.dom import SyntaxErr
from string import digits
# Custom
from datalibrary import DataLibrary
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# Accepts a clean encoded_property_value e.g. 'bold', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px', 'n5_25cm-n6_1cm'
# Decodes a css property_value from a clean encoded_property_value.
class CSSPropertyValueParser(object):
    def __init__(self):
        pass
    
    # Important: these methods are intended to be called in the order they are declared.

    # Delete leading    example: '-bold' --> 'bold'
    # Delete trailing   example: 'white-' --> 'white'
    # Replace internal  example: '1-5-1-5' --> '1 5 1 5'
    @staticmethod
    def replace_dashes(value=''):
        value = value[1:] if value.startswith('-') else value
        value = value[:-1] if value.endswith('-') else value
        return value.replace('-', ' ')

    @staticmethod
    def contains_a_digit(value=''):
        return True if search(r"[0-9]", value) else False

    # Use underscores to indicate Decimal point '_' --> '.'
    # '_' becomes '.'   example: '1_32rem' --> '1.32rem'
    def replace_underscore_with_decimal(self, value=''):
        if self.contains_a_digit(value=value):
            value = value.replace('_', '.')
        return value

    # Using Percentages 'p' --> '%'
    # mind the space
    # 'p ' becomes '% ' example: '1p 10p 3p 1p' --> '1% 10% 3% 1%' AND ' 1p' --> ' 1%'
    def replace_p_with_percent(self, value=''):
        if self.contains_a_digit(value=value):
            value = value.replace('p ', '% ')
            if value.endswith('p'):
                value = value[:-1] + '%'    # chop last character and add percentage sign
        return value

    # Declaring negative values
    # mind the space
    # ' n' becomes ' -'
    # examples:
    # 'n5cm n6cm' --> '-5cm -6cm'
    # 'n9in' --> '-9in' (note that the 'n' at the end is not touched)
    def replace_n_with_minus(self, value=''):
        if self.contains_a_digit(value=value):
            value = value.replace(' n', ' -')
            if value.startswith('n'):
                value = '-' + value[1:]     # add minus sign and chop first character
        return value

    # TODO: implement
    @staticmethod
    def property_name_allows_color(property_name=''):
        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        color_property_names = {
            'color', 'background-color', 'border-color', 'border-top-color', 'border-right-color', 'border-bottom-color',
            'border-left-color', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border', 'outline',
        }
        for color_property_name in color_property_names:
            if property_name == color_property_name:
                return True
        return False

    # Expects a value of the form: h0ff48f or hfaf i.e. 'h' + a 3 or 6 digit hexidecimal value 0-f.
    # Returns #0ff48f or #faf
    @staticmethod
    def is_valid_hex(value=''):
        is_valid = False
        _len = len(value)              # _len includes 'h'
        if value.startswith('h'):
            if _len == 4:           # 'h' + 3 hex digits
                is_valid = True if len(findall(r"([0-9a-f]{3})", value)) == 1 else False
            if _len == 7:           # 'h' + 6 hex digits
                is_valid = True if len(findall(r"([0-9a-f]{6})", value)) == 1 else False
        return is_valid

    # Declaring hex (prepend 'h'):
    # h0ff24f   --> #0ff24f (6 digit)
    # hf4f      --> #fff    (3 digit)
    def replace_h_with_hash(self, property_name='', value=''):
        if self.property_name_allows_color(property_name=property_name):
            if self.is_valid_hex(value=value):
                value = value.replace('h', '#')
        return value

    # Convert parenthetical color values:
    #  rgb: rgb 0 255 0             -->  rgb(0, 255, 0)
    # rgba: rgba 255 0 0 0.5        --> rgba(255, 0, 0, 0.5)
    #  hsl: hsl 120 60% 70%         -->  hsl(120, 60%, 70%)
    # hsla: hsla 120 60% 70% 0.3    --> hsla(120, 60%, 70%, 0.3)
    def add_color_parenthetical(self, property_name='', value=''):
        if self.property_name_allows_color(property_name=property_name):
            if self.contains_a_digit(value=value):
                keywords = {'rgb ', 'rgba ', 'hsl ', 'hsla '}
                for key in keywords:
                    if value.startswith(key):
                        value = value.replace(key, key.strip() + '(')   # Remove key whitespace and add opening '('
                        value += ')'                                    # Add closing ')'
                        value = value.replace(' ', ', ')                # Add commas
                        break
        return value

    def decode_property_value(self, property_name='', value=''):
        # Apply to all.
        value = self.replace_dashes(value=value)

        # These only apply if value contains a digit.
        value = self.replace_underscore_with_decimal(value=value)
        value = self.replace_p_with_percent(value=value)
        value = self.replace_n_with_minus(value=value)

        # The following two only apply when particular property names are used.
        value = self.replace_h_with_hash(property_name=property_name, value=value)
        value = self.add_color_parenthetical(property_name=property_name, value=value)  # Must contain digits.
        value = self.add_units(property_name=property_name, property_value=value)       # Add units if necessary.
        return value

    # Accepts a property name and value
    # Validation occurs after the property value is decoded.
    @staticmethod
    def property_is_valid(name='', value='', priority=''):
        try:
            css_property = Property(name=name, value=value, priority=priority)
            is_valid = css_property.valid
            return is_valid
        except SyntaxErr:
            return False

    # For property_name's that require units apply the default units defined in default_property_units_dict.
    # Handles cases input like: '12', '35 15', '1 2 1 2'
    # Outputs: '12px', '35% 15%', '1px 2px 1px 2px'
    @staticmethod
    def add_units(property_name='', property_value=''):
        new_value = []
        data_library = DataLibrary()
        try:
            default_units = data_library.default_property_units_dict[property_name]  # See if property name is a key.
            for val in property_value.split():                                      # Double and quadruple values.
                if val[-1] in digits:                                               # If value have units.
                    new_value.append(val + default_units)                           # Add default units.
                else:
                    new_value.append(val)                                           # Leave current value unchanged
            property_value = ' '.join(new_value)                                    # Put the new values back together
        except KeyError:
            pass                                                                    # Property does not need units.
        return property_value

    # nice to have 16px = 1em
    # convert px to rem
    # def px_to_em(self, px):
    # TODO: write this.
    #     pass

    # TODO: Implement media query handling using:
    # allow user to define a dict
    # 'xsmall': (0, 240),
    # 'small': (0, 480), etc...
    #
    # hide-for-, show-for-
    # -small-only, -small-down, -small-up, hide-for-480px-down, show-for-480px-up, hide-for-480-down, show-for-480-down

    # TODO: Are URIs ridiculous? or should we implement syntax
    # background-image-url-image.png --> background-image: url("image.png")
    # background-image-url-_home_images_sample_image.png --> background-image: url("/home/images/sample/image.png")
    # IN THE LAST CASE images with underscores would not work could use a double underscore to represent final directory
    # but this is getting ridiculous example double underscore signifies final directory
    # allowing underscore in file name:
    # background-image-url-_home_images_sample__image_1.png --> background-image: url("/home/images/sample/image_1.png")

    # TODO: Handle font-family names with dashes in them same thing for "voice-family"
    # TODO: Consider using '--' to represent '-' dash could be an escape character
    # e.g. font: 15px sans-serif OR font: sans-serif 15px OR font-family: sans-serif
    # ERROR font-15px-sans-serif --> font: 15px sans serif
    # Might require a font name dictionary.
    # What about commas?
    # Could just use font-family name explicity e.g. sans-serif, arial, source-sans-pro
