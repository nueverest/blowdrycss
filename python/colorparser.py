from re import findall
# custom
from utilities import contains_a_digit
from datalibrary import property_regex_dict
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ColorParser(object):
    def __init__(self, property_name='', value=''):
        self.color_regexes = property_regex_dict['color']
        self.property_name = property_name
        self.value = value

    @staticmethod
    def property_name_allows_color(property_name=''):
        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        color_property_names = {
            'color', 'background-color', 'border', 'border-color', 'border-top-color', 'border-right-color',
            'border-bottom-color', 'border-left-color', 'outline', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border', 'outline',
        }
        for color_property_name in color_property_names:
            if property_name == color_property_name:
                return True
        return False

    # Expects a value of the form: h0ff48f or hfaf i.e. 'h' + a 3 or 6 digit hexidecimal value 0-f.
    # Returns #0ff48f or #faf
    # Some shorthand properties are supported: border 1px solid hddd --> border 1px solid #ddd
    def is_valid_hex(self, value=''):
        for regex in self.color_regexes:
            if len(findall(regex, value)) == 1:
                return True
        return False

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
