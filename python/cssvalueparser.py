__author__ = 'chad nelson'
__project__ = 'blow dry css'


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