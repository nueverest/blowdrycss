from unittest import TestCase, main
# custom
from colorparser import ColorParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestColorParser(TestCase):
    def test_property_name_allows_color(self):
        property_names_true = {
            'color', 'background-color', 'border-color', 'border-top-color', 'border-right-color', 'border-bottom-color',
            'border-left-color', 'outline_color',
            'background', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border', 'outline',
        }
        property_names_false = {'font-weight', 'padding', 'height', 'width', 'float'}
        color_parser = ColorParser()
        for property_name in property_names_true:
            self.assertTrue(color_parser.property_name_allows_color(property_name=property_name))
        for property_name in property_names_false:
            self.assertFalse(color_parser.property_name_allows_color(property_name=property_name))

    def test_is_valid_hex(self):
        values_true = ['h0ff48f', 'hfff', ' habc123 ', 'hfdec78', 'h000', ' hbcd ', 'border 5px solid hd0d',
                       'border-5px-solid-hd0d']
        values_false = ['height', 'h1', 'h52', 'hbbb4', 'h00005', 'h0ghyz6', 'h0uk']
        color_parser = ColorParser()
        for value in values_true:
            self.assertTrue(color_parser.is_valid_hex(value), msg=value)
        for value in values_false:
            self.assertFalse(color_parser.is_valid_hex(value), msg=value)

    def test_replace_h_with_hash_valid_property_name(self):
        valid_property_name = 'color'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        expected_values = ['#0ff48f', '#fff', '#abc123', '#fdec78', '#000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        color_parser = ColorParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.replace_h_with_hash(property_name=valid_property_name, value=value),
                expected_values[i],
                msg=value
            )

    def test_replace_h_with_hash_invalid_property_name(self):
        invalid_property_name = 'width'
        input_values = ['h0ff48f', 'hfff', 'habc123', 'hfdec78', 'h000', 'height', 'h1', 'h52', 'h0ghyz6', 'h0uk']
        expected_values = input_values
        color_parser = ColorParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.replace_h_with_hash(property_name=invalid_property_name, value=value),
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
        color_parser = ColorParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.add_color_parenthetical(property_name=valid_property_name, value=value),
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
        color_parser = ColorParser()
        for i, value in enumerate(input_values):
            self.assertEqual(
                color_parser.add_color_parenthetical(property_name=valid_property_name, value=value),
                expected_values[i],
                msg=value
            )


if __name__ == '__main__':
    main()
