from unittest import TestCase, main
# custom 
from unitparser import UnitParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestUnitParser(TestCase):
    def test_add_units_multi_value(self):
        # Handles cases input like: '12', '35 15', '1 2 1 2'
        # Outputs: '12px', '35px 15px', '1px 2px 1px 2px'
        property_name = 'padding'
        property_values = ['12', '35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em']
        expected_values = ['12px', '35px 15px', '1px 2px 1px 2px', '20% 20%', '5em 6em 5em 6em']
        unit_parser = UnitParser()

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_name=property_name, property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_margin_top(self):
        property_name = 'margin-top'
        property_values = ['1', '20', '15px', '60rem']
        expected_values = ['1px', '20px', '15px', '60rem']
        unit_parser = UnitParser()

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_name=property_name, property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)
    
    def test_px_to_em(self):
        unit_parser = UnitParser(base=16)
        for pixels in range(-1000, 1001):
            expected = pixels / unit_parser.base
            actual = unit_parser.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=pixels)

    def test_px_to_em_typecast_to_string(self):
        unit_parser = UnitParser(base=16)
        for pixels in range(-1000, 1001):
            expected = pixels / unit_parser.base
            actual = unit_parser.px_to_em(pixels=str(pixels))       # typecast
            self.assertEqual(actual, expected, msg=pixels)

    def test_px_to_em_change_base(self):
        unit_parser = UnitParser(base=48)
        for pixels in range(-1000, 1001):
            expected = pixels / unit_parser.base
            actual = unit_parser.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=pixels)

    def test_px_to_em_string_base(self):
        unit_parser = UnitParser(base='480')
        for pixels in range(-1000, 1001):
            expected = pixels / unit_parser.base
            actual = unit_parser.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=pixels)

    def test_px_to_em_Wrong_base(self):
        self.assertRaises(ValueError, UnitParser, base='wrong')


if __name__ == '__main__':
    main()


