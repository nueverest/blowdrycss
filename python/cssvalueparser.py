from re import findall
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# Accepts a clean encoded_property_value e.g. 'bold', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px', 'n5_25cm-n6_1cm',
# Decodes a css property_value from a clean encoded_property_value.
class CSSPropertyValueParser(object):
    def __init__(self, encoded_property_value=''):
        self.property_value = encoded_property_value
        self.decode_property_value()

    # Important: these methods are intended to be called in the order they are declared.

    # Delete leading '-' example: '-bold' --> 'bold'
    # '-' becomes spaces example: '1-5-1-5' --> '1 5 1 5'
    def replace_dashes(self):
        if self.property_value.startswith('-'):
            self.property_value = self.property_value[1:]
        self.property_value = self.property_value.replace('-', ' ')

    @staticmethod
    def contains_a_digit(value=''):
        return True if len(findall(r"\D([0-9])\D", ' ' + value + ' ')) >= 1 else False

    # '_' becomes '.'   example: '1_32rem' --> '1.32rem'
    def replace_underscore_with_decimal(self):
        if self.contains_a_digit(value=self.property_value):
            self.property_value = self.property_value.replace('_', '.')

    # mind the space
    # 'p ' becomes '% ' example: '1p 10p 3p 1p' --> '1% 10% 3% 1%' AND ' 1p' --> ' 1%'
    def replace_p_with_percent(self):
        if self.contains_a_digit(value=self.property_value):
            self.property_value = self.property_value.replace('p ', '% ')
            if self.property_value.endswith('p'):
                self.property_value = self.property_value[:-1] + '%'    # chop last character and add percentage sign
    
    # mind the space
    # ' n' becomes ' -' example: 'n5cm n6cm' --> '-5cm -6cm'
    def replace_n_with_minus(self):
        if self.contains_a_digit(value=self.property_value):
            self.property_value = self.property_value.replace(' n', ' -')
            if self.property_value.startswith('n'):
                self.property_value = '-' + self.property_value[1:]     # add minus sign and chop first character

    # Expects a value of the form: h0ff48f or hfaf i.e. 'h' + a 3 or 6 digit hexidecimal value 0-f.
    @staticmethod
    def is_valid_hex(pv=''):
        _len = len(pv)              # _len includes 'h'
        if pv.startswith('h'):
            if _len == 4:           # 'h' + 3 hex digits
                return True if len(findall(r"\D([0-9a-f]{3})\D", ' ' + pv + ' ')) == 1 else False
            if _len == 7:           # 'h' + 6 hex digits
                return True if len(findall(r"\D([0-9a-f]{6})\D", ' ' + pv + ' ')) == 1 else False

        return False

    # Declaring hex (prepend 'h'):
    # h0ff24f --> #0ff24f   (6 digit)
    # hf4f --> #fff         (3 digit)
    def replace_h_with_hash(self):
        if self.is_valid_hex(pv=self.property_value):
            self.property_value = self.property_value.replace('h', '#')

    # Convert parenthetical color values:
    #  rgb: rgb 0 255 0
    # rgba: rgba 255 0 0 0_5
    #  hsl: hsl 120 60% 70%
    # hsla: hsla 120 60% 70% 0_3
    def add_color_parenthetical(self):
        if self.contains_a_digit(value=self.property_value):
            keywords = {'rgb ', 'rbga ', 'hsl ', 'hsla '}
            pv = self.property_value

            for key in keywords:
                if pv.startswith(key):
                    pv = pv.replace(key, key.strip() + '(')     # Remove key whitespace and add opening '('
                    pv += ')'                                   # Add closing ')'
                    pv = pv.replace(' ', ', ')                  # Add commas
                    self.property_value = pv
                    break

    def decode_property_value(self):
        # Apply to all.
        self.replace_dashes()

        # These only apply if self.property_value contains a digit.
        self.replace_underscore_with_decimal()
        self.replace_p_with_percent()
        self.replace_n_with_minus()

        # The following two only apply when particular property names are used, but property_names are not passed in.
        self.replace_h_with_hash()
        self.add_color_parenthetical()


    # nice to have 16px = 1em
    # convert px to rem
    # def px_to_em(self, px):
    #     # TODO: write this.
    #     pass