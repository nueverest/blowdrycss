__author__ = 'chad nelson'
__project__ = 'blow dry css'


# Assumes that the property_name is 'font-family'
# TODO: Consider what it would take to handle shorthand property 'font'.
class FontParser(object):
    # Font-Family References:
    # http://www.cssfontstack.com/
    # https://mathiasbynens.be/notes/unquoted-font-family
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
            'monospace': { 'courier', 'monaco', 'consolas', },
            'fantasy': {'copperplate', 'papyrus', },
        }

    # Generates web safe fallback fonts
    # Reference: http://www.w3schools.com/cssref/css_websafe_fonts.asp
    # font_value 'arial' returns 'arial, sans-serif'
    # font_value 'monospace' returns 'monospace'
    # font_value 'invalid' returns 'serif'  i.e. fail gracefully.
    def generate_fallback_fonts(self):
        fallback = 'serif'                                          # set default font
        if self.font_value in self.font_families_dict:
            fallback = self.font_value                              # font_value 'monospace' returns 'monospace'
        else:
            for family, fonts in self.font_families_dict.items():
                if self.font_value in fonts:
                    fallback = self.font_value + ", " + family      # font_value 'arial' returns 'arial, sans-serif'
        return fallback

    # TODO: Consider the handling of multi-word double quoted fonts i.e. "Palatino Linotype", "Book Antiqua", etc.
    # could use 'qq', 'q--q' or 'dq' to indicate double-quotes e.g. 'qqPalatino-Linotypeqq'
    # 'q-Palatino-Linotype-q'
