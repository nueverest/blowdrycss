from unittest import TestCase
from cssvalueparser import CSSPropertyValueParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestCSSPropertyValueParser(TestCase):
    def test_replace_dashes(self):
        # Delete leading    example: '-bold' --> 'bold'
        # Delete trailing   example: 'white-' --> 'white'
        # Replace internal  example: '1-5-1-5' --> '1 5 1 5'
        input_values = ['-bold', 'white-', '1-5-1-5', 'h0ff48f']
        expected_values = ['bold', 'white', '1 5 1 5', 'h0ff48f']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEquals(property_parser.replace_dashes(value=value), expected_values[i])

    def test_contains_a_digit_true(self):
        digits = ['n12px', '1p 7p 1p 7p', '-1_25em', '-1.35%', 'rgba 255 0 0 0.5', 'h0ff48f']
        property_parser = CSSPropertyValueParser()
        for value in digits:
            self.assertTrue(property_parser.contains_a_digit(value=value), msg=value)

    def test_contains_a_digit_false(self):
        no_digits = ['bold', 'none', 'left']
        property_parser = CSSPropertyValueParser()
        for value in no_digits:
            self.assertFalse(property_parser.contains_a_digit(value=value), msg=value)

    def test_replace_underscore_with_decimal(self):
        # '_' becomes '.'   example: '1_32rem' --> '1.32rem'
        test_values = ['1_32rem', '0_0435p', 'none']
        expected = ['1.32rem', '0.0435p', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEquals(property_parser.replace_underscore_with_decimal(value=value), expected[i])

    def test_replace_p_with_percent(self):
        test_values = ['1_32p', '0.0435p', '1p 2p 1p 2p', 'none']
        expected = ['1_32%', '0.0435%', '1% 2% 1% 2%', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEquals(property_parser.replace_p_with_percent(value=value), expected[i])

    def test_replace_n_with_minus(self):
        test_values = ['n5cm n6cm', 'n12rem', 'n0.0435%', 'n1p n2p n1p n2p', 'n9in', 'none']
        expected = ['-5cm -6cm', '-12rem', '-0.0435%', '-1p -2p -1p -2p', '-9in', 'none']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(test_values):
            self.assertEquals(property_parser.replace_n_with_minus(value=value), expected[i])    

    def test_property_name_allows_color(self):
        property_names_true = {
            'color', 'background-color', 'border-color', 'border-top-color', 'border-right-color', 'border-bottom-color',
            'border-left-color', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border', 'outline',
        }
        property_names_false = {'font-weight', 'padding', 'height', 'width', 'float'}
        property_parser = CSSPropertyValueParser()
        for property_name in property_names_true:
            self.assertTrue(property_parser.property_name_allows_color(property_name=property_name))
        for property_name in property_names_false:
            self.assertFalse(property_parser.property_name_allows_color(property_name=property_name))

    def test_is_valid_hex(self):
        values_true = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000']
        values_false = ['height', 'h1', 'h52', 'hbbb4', 'h00005', 'h0ghyz6', 'h0uk']
        property_parser = CSSPropertyValueParser()
        for value in values_true:
            self.assertTrue(property_parser.is_valid_hex(value))
        for value in values_false:
            self.assertFalse(property_parser.is_valid_hex(value))

    def test_replace_h_with_hash_valid_property_name(self):
        valid_property_name = 'color'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        expected_values = ['#0ff48f', '#fff', '#abc123', '#fdec78', '#000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                property_parser.replace_h_with_hash(property_name=valid_property_name, value=value),
                expected_values[i],
                msg=value
            )

    def test_replace_h_with_hash_invalid_property_name(self):
        invalid_property_name = 'width'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        expected_values = input_values
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                property_parser.replace_h_with_hash(property_name=invalid_property_name, value=value),
                expected_values[i],
                msg=value
            )

    def test_add_color_parenthetical_valid_property_name(self):
        #  rgb: rgb 0 255 0             -->  rgb(0, 255, 0)
        # rgba: rgba 255 0 0 0.5        --> rgba(255, 0, 0, 0.5)
        #  hsl: hsl 120 60% 70%         -->  hsl(120, 60%, 70%)
        # hsla: hsla 120 60% 70% 0.3    --> hsla(120, 60%, 70%, 0.3)
        valid_property_name = 'color'
        input_values = ['rgb 0 255 0', 'rgba 255 0 0 0.5', 'hsl 120 60% 70%', 'hsla 120 60% 70% 0.3', 'blue', '#000']
        expected_values = ['rgb(0, 255, 0)', 'rgba(255, 0, 0, 0.5)', 'hsl(120, 60%, 70%)', 'hsla(120, 60%, 70%, 0.3)',
                           'blue', '#000']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                property_parser.add_color_parenthetical(property_name=valid_property_name, value=value),
                expected_values[i],
                msg=value
            )

    def test_add_color_parenthetical_invalid_property_name(self):
        #  rgb: rgb 0 255 0             -->  rgb(0, 255, 0)
        # rgba: rgba 255 0 0 0.5        --> rgba(255, 0, 0, 0.5)
        #  hsl: hsl 120 60% 70%         -->  hsl(120, 60%, 70%)
        # hsla: hsla 120 60% 70% 0.3    --> hsla(120, 60%, 70%, 0.3)
        valid_property_name = 'height'
        input_values = ['rgb 0 255 0', 'rgba 255 0 0 0.5', 'hsl 120 60% 70%', 'hsla 120 60% 70% 0.3', 'blue', '#000']
        expected_values = input_values
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                property_parser.add_color_parenthetical(property_name=valid_property_name, value=value),
                expected_values[i],
                msg=value
            )

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
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(encoded_property_values):
            self.assertEquals(
                property_parser.decode_property_value(property_name=valid_property_name, value=value),
                expected_property_values[i],
                msg=value
            )

    # These patterns represent invalid CSS that still gets blindly processed. This is expected behavior as this
    # functions is not responsible for validation.  Validation occurs after the property value is decoded.
    def test_decode_property_value_pass_through_invalid_patterns(self):
        valid_property_name = 'color'
        encoded_property_values = ['bold-50', '5u5', 'b1-a5-c1p-e5', '5pxrem', '1ap-10xp-3qp-1mp3', 'p12px']
        expected_property_values = ['bold 50', '5u5', 'b1 a5 c1% e5', '5pxrem', '1a% 10x% 3q% 1mp3', 'p12px']
        property_parser = CSSPropertyValueParser()
        for i, value in enumerate(encoded_property_values):
            self.assertEquals(
                property_parser.decode_property_value(property_name=valid_property_name, value=value),
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