# python 2
from __future__ import absolute_import, division

# builtins
from unittest import TestCase, main

# custom
from blowdrycss.utilities import change_settings_for_testing
from blowdrycss.unitparser import UnitParser
import blowdrycss_settings as settings

change_settings_for_testing()


class TestUnitParser(TestCase):
    def test_default_units(self):
        property_names = [
            'font-size', 'padding', 'margin', 'pitch', 'text-indent', 'volume', 'width', 'font-weight', 'color',
            'invalid', '', 'none',
        ]
        expected_units = ['px', 'px', 'px', 'Hz', 'px', '%', 'px', '', '', '', '', '']

        for i, property_name in enumerate(property_names):
            unit_parser = UnitParser(property_name=property_name)
            self.assertEqual(unit_parser.default_units(), expected_units[i])

    def test_add_units_multi_value_conversion_True_invalid_pass_through(self):
        # Handles cases input like: '1a2', '-35mx 15mx', '1px 2 m11 2', '22.5px 10 22.5px 10'
        # Outputs: '1a2', '-35mx 15mx', '0.0625em 0.125em m11 0.125em', '22.5px 0.625em 22.5px 0.625em'
        property_name = 'padding'
        property_values = ['1a2', '-35mx 15mx', '1px 2 m11 2', '22.5px 10 22.5px 10']
        expected_values = ['1a2', '-35mx 15mx', '0.0625em 0.125em m11 0.125em', '1.4062em 0.625em 1.4062em 0.625em']
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=new_value + ' vs ' + expected_values[i])

    def test_add_units_multi_value_conversion_True(self):
        # Handles cases input like: '12.5', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em'
        # Outputs: '0.75em', '-35px 15px', '1px 2px 1px 2px', '20% 20%', '5em 6em 5em 6em'
        property_name = 'padding'
        property_values = ['12', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em']
        expected_values = [
            '0.75em', '-2.1875em 0.9375em', '0.0625em 0.125em 0.0625em 0.125em', '20% 20%', '5em 6em 5em 6em'
        ]
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=new_value)

    def test_add_units_margin_top_conversion_True(self):
        property_name = 'margin-top'
        property_values = ['1', '-20.0', '15px', '60rem']
        expected_values = ['0.0625em', '-1.25em', '0.9375em', '60rem']
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_no_conversion(self):
        # Handles cases input like: '12', '-35 15', '1 2 1 2'
        # Outputs: '12px', '-35px 15px', '1px 2px 1px 2px'
        property_name = 'padding'
        property_values = ['12', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em']
        expected_values = ['12px', '-35px 15px', '1px 2px 1px 2px', '20% 20%', '5em 6em 5em 6em']
        settings.use_em = False
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

        settings.use_em = True

    def test_add_units_multi_value_conversion_True_strange_input(self):
        # Note that the cm, rem, and em cases are not handled intuitively causing the units to be mixed.
        # This still produces valid CSS.
        property_name = 'padding'
        property_values = ['-35rem 15', '3 4px 3px 5', '5em 6 5em 6', '1em 100 4cm 9rem']
        expected_values = [
            '-35rem 0.9375em', '0.1875em 0.25em 0.1875em 0.3125em', '5em 0.375em 5em 0.375em', '1em 6.25em 4cm 9rem'
        ]
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_no_conversion_strange_input(self):
        # Note that the cm, rem and em cases are not handled intuitively causing the units to be mixed.
        # This still produces valid CSS.
        property_name = 'padding'
        property_values = ['-35rem 15', '3 4px 3px 5', '5em 6 5em 6', '1em 100 4cm 9rem']
        expected_values = ['-35rem 15px', '3px 4px 3px 5px', '5em 6px 5em 6px', '1em 100px 4cm 9rem']
        settings.use_em = False
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

        settings.use_em = True

    def test_add_units_margin_top_no_conversion(self):
        property_name = 'margin-top'
        property_values = ['1', '-20.0', '15px', '60rem']
        expected_values = ['1px', '-20.0px', '15px', '60rem']
        settings.use_em = False
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

        settings.use_em = True

    def test_add_units_margin_top_no_conversion_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'margin-top'
        property_values = ['1um', '-20.0no', '15txt', '60st']
        unit_parser = UnitParser(property_name=property_name)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_margin_top_conversion_True_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'margin-top'
        property_values = ['12aou', '-35oeu 15ou', '1ou 2oeu 1ou 2ou', '20i 20u*', '5e 6m 5e 6m']
        unit_parser = UnitParser(property_name=property_name)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_multi_value_no_conversion_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'padding'
        property_values = ['12aou', '-35oeu 15ou', '1ou 2oeu 1ou 2ou', '20i 20u*', '5e 6m 5e 6m']
        unit_parser = UnitParser(property_name=property_name)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_multi_value_conversion_True_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'padding'
        property_values = ['1um', '-20.0no', '15txt', '60st']
        unit_parser = UnitParser(property_name=property_name)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_UnitLess_Property_conversion_True(self):
        property_name = 'font-weight'
        property_values = ['bold', '200', '800', 'lighter']
        expected_values = ['bold', '200', '800', 'lighter']
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_UnitLess_Property_conversion_False(self):
        property_name = 'font-weight'
        property_values = ['bold', '200', '800', 'lighter']
        expected_values = ['bold', '200', '800', 'lighter']
        unit_parser = UnitParser(property_name=property_name)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)


if __name__ == '__main__':
    main()


