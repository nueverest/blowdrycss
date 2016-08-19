"""
**Features:**

- Validates whether the property_name allows a color property to be set.

- Decodes the following color formats: hexidecimal, rgb, rgba, hsl, hsla.

  Exception: English color names are handled separately
    | **Either** in the property_alias_dict under the key ``color``,
    | **Or** they are passed through to cssutils because they are valid CSS and do not require further processing.

**Note:** The shorthand properties ``background``, ``border``,  and ``outline`` are supported (as of November 2015).

**Assumption:** It is assumed that all dashes are removed from the input ``value`` prior to using this parser.

**Example:**

>>> color_parser = ColorParser('border-color', 'h0df48a')
>>> color_parser.property_name_allows_color()
True

"""

# python 2
from __future__ import absolute_import
# builtins
from re import findall
# custom
from blowdrycss.utilities import contains_a_digit
from blowdrycss.datalibrary import property_regex_dict

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class ColorParser(object):
    """ Extracts plain text, hexidecimal, rgb, rgba, hsl, and hsla color codes from encoded class selectors.

    """
    def __init__(self, property_name='', value=''):
        self.color_regexes = property_regex_dict['color']
        self.property_name = property_name
        self.value = value

    def property_name_allows_color(self):
        """ Detects if the ``property_name`` allows a color property value.

        **Reference:** http://www.w3.org/TR/CSS21/propidx.html

        :return: (bool) -- Returns True if the ``property_name`` is allow to contain colors. Otherwise, it returns
            False.

        **Examples:**

        >>> color_parser = ColorParser('border-color', 'h0df48a')
        >>> color_parser.property_name_allows_color()
        True
        >>> color_parser.property_name = 'invalid'
        >>> color_parser.property_name_allows_color()
        False

        """
        color_property_names = {
            'color', 'background-color', 'border', 'border-color', 'border-top-color', 'border-right-color',
            'border-bottom-color', 'border-left-color', 'outline', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left',
            'text-shadow',
        }
        for color_property_name in color_property_names:
            if self.property_name == color_property_name:
                return True
        return False

    def find_h_index(self, value=''):
        """ Detects if the ``value`` is a valid hexidecimal encoding.

        **Note:** Supports shorthand properties.

        :type value: str

        :param value: Expects a ``value`` of the form: h0ff48f or hfaf i.e. 'h' + a 3 or 6 digit hexidecimal value 0-f.
        :return: (int or NoneType) -- Returns the index of the ``h`` to be replaced in the ``value`` if it matches
            the hex regex. Otherwise it returns None.

        **Examples:**

        >>> color_parser = ColorParser()
        >>> color_parser.find_h_index(value='h0df48a')
        0
        >>> color_parser.find_h_index(value='h1invalid')
        None

        """
        for regex in self.color_regexes:
            matches = findall(regex, value)
            if len(matches) == 1:
                h_index = value.index(matches[0])
                return h_index
        return None

    def replace_h_with_hash(self, value=''):
        """ Replaces the prepended ``h`` prefix with a hash sign ``#`` or octothorpe if you prefer long words.

        | Includes an internal check to ensure that the value is a valid hexidecimal encoding.
        | Only replaces the ``h`` that matches the regex as other ``h`` characters may be present.

        | **Shorthand properties are supported:**
        | **border case:** ``1px solid hddd`` becomes ``1px solid #ddd``

        :param value: Encoded hexidecimal value of the form ``hf1f`` or ``hc2c2c2``.
        :return: (str) -- Returns actually #0ff48f and #faf in the valid case. Returns the input ``value`` unchanged
            for the invalid case.

        >>> color_parser = ColorParser()
        >>> # Valid Cases
        >>> color_parser.replace_h_with_hash('h0ff24f')
        #0ff24f
        >>> color_parser.replace_h_with_hash('hf4f')
        #f4f
        >>> # Valid multiple 'h' case.
        >>> color_parser.replace_h_with_hash('13px dashed hd0d')
        13px dashed #d0d
        >>> # Invalid Cases
        >>> color_parser.replace_h_with_hash('bold')
        bold
        >>> color_parser.replace_h_with_hash('he2z')
        he2z

        """
        if self.property_name_allows_color():
            h_index = self.find_h_index(value=value)        # Only this 'h' will be replaced.
            if h_index is not None:
                value = value[0:h_index] + '#' + value[h_index + 1:]
        return value

    def add_color_parenthetical(self, value=''):
        """ Convert parenthetical color values: rbg, rbga, hsl, hsla to valid css format

        Assumes that color conversion happens after dashes, decimal point, negative signs, and percentage signs
        are converted.

        **Note:** Currently not compatible with shorthand properties.

        :type value: str

        :param value: Space delimited rbg, rbga, hsl, hsla values.
        :return: (str) -- Returns the valid css color parenthetical. Returns the input ``value`` unchanged
            for the non-matching case.

        **Examples:**

        >>> color_parser = ColorParser('color', '')
        >>> color_parser.add_color_parenthetical('rgb 0 255 0')
        rgb(0, 255, 0)
        >>> color_parser.add_color_parenthetical('rgba 255 0 0 0.5')
        rgba(255, 0, 0, 0.5)
        >>> color_parser.add_color_parenthetical('hsl 120 60% 70%')
        hsl(120, 60%, 70%)
        >>> color_parser.add_color_parenthetical('hsla 120 60% 70% 0.3')
        hsla(120, 60%, 70%, 0.3)
        >>> # Pass-through case as no conversion is possible.
        >>> color_parser.add_color_parenthetical('hsla')
        hsla

        """
        if self.property_name_allows_color():
            if contains_a_digit(string=value):
                keywords = {'rgb ', 'rgba ', 'hsl ', 'hsla '}
                for key in keywords:
                    if value.startswith(key):
                        value = value.replace(key, key.strip() + '(')   # Remove key whitespace and add opening '('
                        value += ')'                                    # Add closing ')'
                        value = value.replace(' ', ', ')                # Add commas ', '
                        break
        return value
