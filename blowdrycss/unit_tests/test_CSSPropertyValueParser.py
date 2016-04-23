# python 2
from __future__ import absolute_import

# builtin
from unittest import TestCase, main

# custom
from blowdrycss.cssvalueparser import CSSPropertyValueParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestCSSPropertyValueParser(TestCase):
    def test_is_built_in_valid(self):
        property_names = ['font-weight', 'color', 'background-repeat']
        input_values = ['bold', 'white', 'no-repeat']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            property_parser.property_name = property_names[i]
            self.assertTrue(property_parser.is_built_in(value=value))

    def test_is_built_in_invalid(self):
        property_names = ['font-weight', 'color', 'padding', 'color', 'inValid2']
        input_values = ['-bold', 'white-', '1-5-1-5', 'h0ff48f', '24px']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            property_parser.property_name = property_names[i]
            self.assertFalse(property_parser.is_built_in(value=value))

    def test_replace_dashes(self):
        # Delete leading    example: '-bold' --> 'bold'
        # Delete trailing   example: 'white-' --> 'white'
        # Replace internal  example: '1-5-1-5' --> '1 5 1 5'
        input_values = ['-bold', 'white-', '1-5-1-5', 'h0ff48f']
        expected_values = ['bold', 'white', '1 5 1 5', 'h0ff48f']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEqual(property_parser.replace_dashes(value=value), expected_values[i])

    def test_replace_underscore_with_decimal(self):
        # '_' becomes '.'   example: '1_32rem' --> '1.32rem'
        test_values = ['1_32rem', '0_0435p', 'none']
        expected = ['1.32rem', '0.0435p', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEqual(property_parser.replace_underscore_with_decimal(value=value), expected[i])

    def test_replace_p_with_percent(self):
        test_values = ['1_32p', '0.0435p', '1p 2p 1p 2p', 'none']
        expected = ['1_32%', '0.0435%', '1% 2% 1% 2%', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEqual(property_parser.replace_p_with_percent(value=value), expected[i])

    def test_replace_n_with_minus(self):
        test_values = ['n5cm n6cm', 'n12rem', 'n0.0435%', 'n1p n2p n1p n2p', 'n9in', 'none']
        expected = ['-5cm -6cm', '-12rem', '-0.0435%', '-1p -2p -1p -2p', '-9in', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEqual(property_parser.replace_n_with_minus(value=value), expected[i])

    def test_decode_property_value(self):
        valid_property_name = 'color'
        encoded_property_values = [
            'bold', '55', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px', 'n5_25in-n6_1in', 'n0_0435p',
            'h0ff48f', 'hfff', 'rgba-255-0-0-0_5', 'hsla-120-60p-70p-0_3',
        ]
        expected_property_values = [
            'bold', '55', '1 5 1 5', '1.32rem', '1% 10% 3% 1%', '-12px', '-5.25in -6.1in', '-0.0435%',
            '#0ff48f', '#fff', 'rgba(255, 0, 0, 0.5)', 'hsla(120, 60%, 70%, 0.3)',
        ]
        property_parser = CSSPropertyValueParser(property_name=valid_property_name)
        for i, value in enumerate(encoded_property_values):
            self.assertEqual(
                property_parser.decode_property_value(value=value),
                expected_property_values[i],
                msg=value
            )

    def test_decode_property_value_px_to_em(self):
        valid_property_name = 'padding'
        encoded_property_values = [
            '55', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px', 'n5_25in-n6_1in', 'n0_0435p',
        ]
        expected_property_values = [
            '3.4375em', '0.0625em 0.3125em 0.0625em 0.3125em', '1.32rem', '1% 10% 3% 1%', '-0.75em',
            '-5.25in -6.1in', '-0.0435%',
        ]
        property_parser = CSSPropertyValueParser(property_name=valid_property_name)
        for i, value in enumerate(encoded_property_values):
            self.assertEqual(
                property_parser.decode_property_value(value=value),
                expected_property_values[i],
                msg=value
            )

    def test_decode_property_value_font_family(self):
        valid_property_name = 'font-family'
        encoded_property_values = [
            'serif', 'sans-serif', 'monospace', 'fantasy',
            'cambria', 'didot', 'garamond',
            'arial', 'helvetica', 'gadget',
            'courier', 'monaco', 'consolas',
            'copperplate', 'papyrus',
            'invalid', 'wrong',     # These just pass through.
        ]
        expected_property_values = [
            'serif', 'sans-serif', 'monospace', 'fantasy',
            'cambria, serif', 'didot, serif', 'garamond, serif',
            'arial, sans-serif', 'helvetica, sans-serif', 'gadget, sans-serif',
            'courier, monospace', 'monaco, monospace', 'consolas, monospace',
            'copperplate, fantasy', 'papyrus, fantasy',
            'invalid', 'wrong',     # These just pass through.
        ]
        property_parser = CSSPropertyValueParser(property_name=valid_property_name)
        for i, value in enumerate(encoded_property_values):
            self.assertEqual(
                property_parser.decode_property_value(value=value),
                expected_property_values[i],
                msg=value
            )

    # These patterns represent invalid CSS that still gets blindly processed. This is expected behavior as this
    # functions is not responsible for validation.  Validation occurs after the property value is decoded.
    def test_decode_property_value_pass_through_invalid_patterns(self):
        valid_property_name = 'color'
        encoded_property_values = ['bold-50', '5u5', 'b1-a5-c1p-e5', '5pxrem', '1ap-10xp-3qp-1mp3', 'p12px']
        expected_property_values = ['bold 50', '5u5', 'b1 a5 c1% e5', '5pxrem', '1a% 10x% 3q% 1mp3', 'p12px']
        property_parser = CSSPropertyValueParser(property_name=valid_property_name)
        for i, value in enumerate(encoded_property_values):
            self.assertEqual(
                property_parser.decode_property_value(value=value),
                expected_property_values[i],
                msg=value
            )

    def test_property_is_valid_true(self):
        property_name = 'color'
        valid_values = ['blue', 'white', '#fff', '#0ff48f', 'rgba(255, 0, 0, 0.5)', 'hsla(120, 60%, 70%, 0.3)']
        property_parser = CSSPropertyValueParser()
        for value in valid_values:
            self.assertTrue(property_parser.property_is_valid(name=property_name, value=value, priority=''))

    def test_property_is_valid_false(self):
        property_name = 'color'
        invalid_values = ['a pm', 'bold-50', 'whatever', '1% 5% 1% 5%', '-12.7rem', '5u5', '5pxrem', 'p12px',
                          'b1 a5 c1% e5', '1a% 10x% 3q% 1mp3', ]    # The last two raise SyntaxErr
        property_parser = CSSPropertyValueParser()
        for value in invalid_values:
            self.assertFalse(property_parser.property_is_valid(name=property_name, value=value, priority=''))


if __name__ == '__main__':
    main()
