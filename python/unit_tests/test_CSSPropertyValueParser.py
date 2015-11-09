from unittest import TestCase
from cssvalueparser import CSSPropertyValueParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestCSSPropertyValueParser(TestCase):
    def test_replace_dashes(self):
        # Delete leading '-' example: '-bold' --> 'bold'
        # '-' becomes spaces example: '1-5-1-5' --> '1 5 1 5'
        leading = '-bold'
        leading_expected = 'bold'
        internal = '1-5-1-5'
        internal_expected = '1 5 1 5'
        css_property_parser = CSSPropertyValueParser(encoded_property_value=leading)
        self.assertEquals(css_property_parser.property_value, leading_expected)
        css_property_parser = CSSPropertyValueParser(encoded_property_value=internal)
        self.assertEquals(css_property_parser.property_value, internal_expected)

    # def test_contains_a_digit(self):
    #     self.fail()
    #
    # def test_replace_underscore_with_decimal(self):
    #     self.fail()
    #
    # def test_replace_p_with_percent(self):
    #     self.fail()
    #
    # def test_replace_n_with_minus(self):
    #     self.fail()
    #
    # def test_is_valid_hex(self):
    #     self.fail()
    #
    # def test_replace_h_with_hash(self):
    #     self.fail()
    #
    # def test_add_color_parenthetical(self):
    #     self.fail()
    #
    # def test_decode_property_value(self):
    #     self.fail()
