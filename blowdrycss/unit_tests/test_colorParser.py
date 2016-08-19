# python 2
from __future__ import absolute_import
# builtins
from unittest import TestCase, main

# custom
from blowdrycss.colorparser import ColorParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestColorParser(TestCase):
    def test_property_name_allows_color(self):
        property_names_true = {
            'color', 'background-color', 'border-color', 'border-top-color', 'border-right-color',
            'border-bottom-color',
            'border-left-color', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border', 'outline',
        }
        property_names_false = {'font-weight', 'padding', 'height', 'width', 'float'}
        color_parser = ColorParser()
        for property_name in property_names_true:
            color_parser.property_name = property_name
            self.assertTrue(color_parser.property_name_allows_color())
        for property_name in property_names_false:
            color_parser.property_name = property_name
            self.assertFalse(color_parser.property_name_allows_color())

    def test_is_valid_hex_Integer_case(self):
        values_true = [
            'h0ff48f', 'hfff', ' hABC123 ', 'hfdec78', 'h000', ' hbcd ', '5px solid hd0d', '5px-hidden-hd0d987',
            '13px dashed hd0d',
            'h000-i', 'h484848-i',
            'hd9d-hover', 'hd9d9d8-hover', 'hf2f-hover-i', 'hF3F-i-hover',
            'hf2f2f2-hover-i', 'hf3f3f3-i-hover',
        ]
        expected = [
            0, 0, 1, 0, 0, 1, 10, 11,
            12,
            0, 0,
            0, 0, 0, 0,
            0, 0,
        ]
        color_parser = ColorParser()
        for i, value in enumerate(values_true):
            self.assertEqual(color_parser.find_h_index(value), expected[i], msg=value)

    def test_is_valid_hex_None_case(self):
        values_false = ['height', 'h1', 'h52', 'hbbb4', 'h00005', 'h0ghyz6', 'h0uk']
        color_parser = ColorParser()
        for value in values_false:
            self.assertEqual(color_parser.find_h_index(value), None, msg=value)

    def test_replace_h_with_hash_valid_property_name(self):
        valid_property_name = 'color'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk', ]
        expected_values = ['#0ff48f', '#fff', '#abc123', '#fdec78', '#000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk', ]
        color_parser = ColorParser(property_name=valid_property_name)
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.replace_h_with_hash(value=value),
                expected_values[i],
                msg=value
            )

    def test_replace_h_with_hash_valid_shorthand_property_name(self):
        valid_property_name = 'border'
        input_values = ['5px solid hd0da1a', '13px dashed hd0d', '9px hidden hc0d', ]
        expected_values = ['5px solid #d0da1a', '13px dashed #d0d', '9px hidden #c0d', ]
        color_parser = ColorParser(property_name=valid_property_name)
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.replace_h_with_hash(value=value),
                expected_values[i],
                msg=value
            )

    def test_replace_h_with_hash_invalid_property_name(self):
        invalid_property_name = 'width'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        expected_values = input_values
        color_parser = ColorParser(property_name=invalid_property_name)
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.replace_h_with_hash(value=value),
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
        color_parser = ColorParser(property_name=valid_property_name)
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.add_color_parenthetical(value=value),
                expected_values[i],
                msg=value
            )

    def test_add_color_parenthetical_invalid_property_name(self):
        #  rgb: rgb 0 255 0             -->  rgb(0, 255, 0)
        # rgba: rgba 255 0 0 0.5        --> rgba(255, 0, 0, 0.5)
        #  hsl: hsl 120 60% 70%         -->  hsl(120, 60%, 70%)
        # hsla: hsla 120 60% 70% 0.3    --> hsla(120, 60%, 70%, 0.3)
        input_values = ['rgb 0 255 0', 'rgba 255 0 0 0.5', 'hsl 120 60% 70%', 'hsla 120 60% 70% 0.3', 'blue', '#000']
        expected_values = input_values
        color_parser = ColorParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.add_color_parenthetical(value=value),
                expected_values[i],
                msg=value
            )


if __name__ == '__main__':
    main()
