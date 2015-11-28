from re import findall
# custom
from utilities import contains_a_digit
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ColorParser(object):
    def __init__(self, property_name='', value=''):
        self.property_name = property_name
        self.value = value

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
    # Note: This does not work with shorthand properties border-1px-solid-hddd will not replace the 'h'
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
            if contains_a_digit(value=value):
                keywords = {'rgb ', 'rgba ', 'hsl ', 'hsla '}
                for key in keywords:
                    if value.startswith(key):
                        value = value.replace(key, key.strip() + '(')   # Remove key whitespace and add opening '('
                        value += ')'                                    # Add closing ')'
                        value = value.replace(' ', ', ')                # Add commas
                        break
        return value
