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
        css_property_parser = CSSPropertyValueParser()
        self.assertEquals(css_property_parser.property_value, leading_expected)
        css_property_parser = CSSPropertyValueParser()
        self.assertEquals(css_property_parser.property_value, internal_expected)

    def test_contains_a_digit_true(self):
        digits = ['n12px', '1p 7p 1p 7p', '-1_25em', '-1.35%']
        css_property_parser = CSSPropertyValueParser()
        for value in digits:
            self.assertTrue(css_property_parser.contains_a_digit(value=value), msg=value)

    def test_contains_a_digit_false(self):
        no_digits = ['bold', 'none', 'left']
        css_property_parser = CSSPropertyValueParser()
        for value in no_digits:
            self.assertFalse(css_property_parser.contains_a_digit(value=value), msg=value)

    # def test_replace_underscore_with_decimal(self):
    #     # '_' becomes '.'   example: '1_32rem' --> '1.32rem'
    #     test_values = ['1_32rem', '0_0435p']
    #     expected = ['1.32rem', '0.0435p']
    #     css_property_parser = CSSPropertyValueParser(encoded_property_value='')
    #     for value in test_values:
    #         css_property_parser.


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
