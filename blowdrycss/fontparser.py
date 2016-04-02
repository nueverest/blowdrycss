# python 2
from __future__ import absolute_import

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


# TODO: Consider what it would take to handle shorthand property 'font'.
class FontParser(object):
    """ **Features:**

    - Parses unquoted font families.

      Unquoted Font-Family References:
        | http://www.cssfontstack.com/
        | https://mathiasbynens.be/notes/unquoted-font-family

    - Holds a basic ``font_families_dict`` (could be extended as desired):
        | Keys: ``font-family`` category names
        | Values: ``font-family`` member names

    - Can generate web safe fallback fonts.

    Assumes that the property_name is ``font-family``. It does not handle the shorthand property_name ``font``

    **Examples:**

    >>> font_parser = FontParser('papyrus')
    >>> font_parser.generate_fallback_fonts()
    'papyrus, fantasy'

    """
    def __init__(self, font_value=''):
        self.font_value = font_value
        self.font_families_dict = {
            'serif': {
                'georgia', 'palatino', 'times', 'cambria', 'didot', 'garamond', 'perpetua', 'rockwell', 'baskerville',
            },
            'sans-serif': {
                'arial', 'helvetica', 'gadget', 'cursive', 'impact', 'charcoal', 'tahoma', 'geneva', 'verdana',
                'calibri', 'candara', 'futura', 'optima',
            },
            'monospace': {'courier', 'monaco', 'consolas', },
            'fantasy': {'copperplate', 'papyrus', },
        }

    def generate_fallback_fonts(self):
        """ Generates web safe fallback fonts

        Reference: http://www.w3schools.com/cssref/css_websafe_fonts.asp

        :return: (str) -- Returns a web safe fallback font string.

        **Examples:**

        >>> font_parser = FontParser('arial')
        >>> font_parser.generate_fallback_fonts()
        'arial, sans-serif'
        >>> font_parser.font_value = 'monospace'
        'monospace'
        >>> font_parser.font_value = 'invalid'
        ''

        """
        fallback = ''                                               # set default font to empty string
        if self.font_value in self.font_families_dict:
            fallback = self.font_value                              # font_value 'monospace' returns 'monospace'
        else:
            for family, fonts in self.font_families_dict.items():
                if self.font_value in fonts:
                    fallback = self.font_value + ", " + family      # font_value 'arial' returns 'arial, sans-serif'
        return fallback

    # TODO: Consider the handling of multi-word double quoted fonts i.e. "Palatino Linotype", "Book Antiqua", etc.
    # Seems complicated.
    # could use 'qq', 'q--q' or 'dq' to indicate double-quotes e.g.
    # 'qqPalatino-Linotypeqq' - confusing 'Linotype' looks like 'Linotypeg'. The letter 'q' looks like a 'g' at the end.
    # 'q-Palatino-Linotype-q' - might work
    # 'dqPalatino-Linotypedq' - confusing 'Linotype' becomes 'Linotyped'. The letter 'd' commonly ends words.
