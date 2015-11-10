from unittest import TestCase
from classpropertyparser import ClassPropertyParser


class TestClassPropertyParser(TestCase):
    def test_class_set_to_lowercase(self):
        original_class_set = {'ThE', 'the', 'THE', 't2HE'}
        expected_class_set = {'the', 'the', 'the', 't2he'}
        class_parser = ClassPropertyParser(class_set=original_class_set)
        class_parser.class_set_to_lowercase()
        self.assertEquals(class_parser.class_set, expected_class_set)

    def test_underscores_valid_is_true(self):
        valid_classes = {'6_3', 'padding-5_2rem', 'height-24_48p'}
        class_parser = ClassPropertyParser(class_set=valid_classes)
        for css_class in class_parser.class_set:
            self.assertTrue(class_parser.underscores_valid(css_class=css_class), msg=css_class)

    def test_underscores_valid_is_false(self):
        # Invalid: '-_2", '2_rem', 'm_px', and '__'
        invalid_classes = {'_bold', 'lighter-1_', 'width-_2', 'margin-2_rem', 'height-m_px', 'bg-color__blue'}
        class_parser = ClassPropertyParser(class_set=invalid_classes)
        for css_class in class_parser.class_set:
            self.assertFalse(class_parser.underscores_valid(css_class=css_class), msg=css_class)

    def test_clean_class_set(self):
        valid_classes = {'width-6_3', 'padding-5_2rem', 'height-24_48p', 'padding-7_3-8_5-9_7-10_2'}
        invalid_classes = {'_b', 'lighter-1_', 'width-_2', 'margin-2_rem', 'height-m_px', 'bg-color__blue'}
        class_parser = ClassPropertyParser(class_set=valid_classes.union(invalid_classes))
        class_parser.clean_class_set()                              # Called explicitly even though called by init().
        self.assertEquals(class_parser.class_set, valid_classes)    # Only valid classes should remain.
        self.assertEquals(class_parser.removed_class_set, invalid_classes)

    def test_get_property_name_by_identical_name_valid(self):
        valid_identical_set = {'font-weight-bold', 'font-weight-700'}
        expected_property_name = 'font-weight'
        class_parser = ClassPropertyParser(class_set=valid_identical_set)

        class_list = list(class_parser.class_set)
        for i, css_class in enumerate(class_list):
            property_name = class_parser.get_property_name(css_class=css_class)
            self.assertEquals(property_name, expected_property_name)

    def test_get_property_name_by_identical_name_invalid(self):
        invalid_identical_set = {'font-weight', 'font-weight-', '-font-weight', 'font%weight'}
        expected_property_name = ''
        expected_empty_set = set()
        class_parser = ClassPropertyParser(class_set=invalid_identical_set)

        class_list = list(class_parser.class_set)
        for i, css_class in enumerate(class_list):
            property_name = class_parser.get_property_name(css_class=css_class)
            self.assertEquals(property_name, expected_property_name)
        self.assertEquals(class_parser.class_set, expected_empty_set)

    def test_get_property_name_by_alias(self):
        class_alias_set = {'normal', 'bold', 'bolder', 'lighter', 'initial', 'fw-'}
        expected_property_name = 'font-weight'
        class_parser = ClassPropertyParser(class_set=set())

        class_list = list(class_alias_set)
        for css_class in class_list:
            property_name = class_parser.get_property_name(css_class=css_class)
            self.assertEquals(property_name, expected_property_name, msg=css_class)

    def test_get_property_name_non_matching(self):
        non_matching = {'font-weight', 'font-weight-', '-font-weight'}
        expected_property_name = ''
        expected_empty_set = set()
        class_parser = ClassPropertyParser(class_set=non_matching)

        class_list = list(class_parser.class_set)
        for i, css_class in enumerate(class_list):
            property_name = class_parser.get_property_name(css_class=css_class)
            self.assertEquals(property_name, expected_property_name)
        self.assertEquals(class_parser.class_set, expected_empty_set)

    def test_strip_property_name_matching(self):
        property_name = 'font-weight'
        encoded_property_value = 'font-weight-400'
        expected_encoded_property_value = '400'
        class_parser = ClassPropertyParser(class_set=set())
        encoded_property_value = class_parser.strip_property_name(
            property_name=property_name,
            encoded_property_value=encoded_property_value
        )
        self.assertEquals(encoded_property_value, expected_encoded_property_value)

    def test_strip_property_name_not_matching(self):
        property_name = 'font-weight'
        encoded_property_value = 'bold'
        expected_encoded_property_value = 'bold'
        class_parser = ClassPropertyParser(class_set=set())
        encoded_property_value = class_parser.strip_property_name(
            property_name=property_name,
            encoded_property_value=encoded_property_value
        )
        self.assertEquals(encoded_property_value, expected_encoded_property_value)

    def test_strip_property_name_empty(self):
        empty_property_name = ''
        encoded_property_value = 'bold'
        class_parser = ClassPropertyParser(class_set=set())
        self.assertRaises(ValueError, class_parser.strip_property_name, empty_property_name, encoded_property_value)

    def test_alias_is_abbreviation(self):
        expected_true = ['fw-', 'p-', 'h-', 'w-']
        expected_false = ['fw', 'p', 'height', 'width']
        class_parser = ClassPropertyParser(class_set=set())

        for _true in expected_true:
            self.assertTrue(class_parser.alias_is_abbreviation(_true), msg=_true)

        for _false in expected_false:
            self.assertFalse(class_parser.alias_is_abbreviation(_false), msg=_false)

    def test_get_property_abbreviations(self):
        expected_abbreviations = ['fw-']
        property_name = 'font-weight'
        class_parser = ClassPropertyParser(class_set=set())
        abbreviations = class_parser.get_property_abbreviations(property_name=property_name)
        self.assertEquals(abbreviations, expected_abbreviations)

    def test_strip_property_abbreviation_matching(self):
        property_name = 'font-weight'
        encoded_property_value = 'fw-400'
        expected_encoded_property_value = '400'
        class_parser = ClassPropertyParser(class_set=set())
        encoded_property_value = class_parser.strip_property_abbreviation(
            property_name=property_name,
            encoded_property_value=encoded_property_value
        )
        self.assertEquals(encoded_property_value, expected_encoded_property_value)

    def test_strip_property_abbreviation_not_matching(self):
        property_name = 'font-weight'
        encoded_property_value = 'bold'
        expected_encoded_property_value = 'bold'
        class_parser = ClassPropertyParser(class_set=set())
        encoded_property_value = class_parser.strip_property_abbreviation(
            property_name=property_name,
            encoded_property_value=encoded_property_value
        )
        self.assertEquals(encoded_property_value, expected_encoded_property_value)

    def test_get_encoded_property_value(self):
        # 'fw-bold-i' --> 'bold'                [abbreviated font-weight property_name]
        # 'padding-1-10-10-5-i' --> '1-10-10-5' [standard property_name]
        # 'height-7_25rem-i' --> '7_25rem'      [contains underscores]
        property_names = ['font-weight', 'padding', 'height']
        css_classes = ['fw-bold-i', 'padding-1-10-10-5-i', 'height-7_25rem-i']
        expected_encoded_property_values = ['bold', '1-10-10-5', '7_25rem']
        class_parser = ClassPropertyParser(class_set=set())

        for i, css_class in enumerate(css_classes):
            encoded_property_value = class_parser.get_encoded_property_value(
                property_name=property_names[i],
                css_class=css_class
            )
            self.assertEquals(encoded_property_value, expected_encoded_property_values[i], msg=property_names)

    def test_get_property_value_valid_patterns(self):
        property_name = 'color'
        encoded_property_values = [
            'bold', '55', '1-5-1-5', '1_32rem', '1p-10p-3p-1p', 'n12px', 'n5_25in-n6_1in', 'n0_0435p',
            'h0ff48f', 'hfff', 'rgba-255-0-0-0_5', 'hsla-120-60p-70p-0_3',
        ]
        expected_property_values = [
            'bold', '55', '1 5 1 5', '1.32rem', '1% 10% 3% 1%', '-12px', '-5.25in -6.1in', '-0.0435%',
            '#0ff48f', '#fff', 'rgba(255, 0, 0, 0.5)', 'hsla(120, 60%, 70%, 0.3)',
        ]
        class_parser = ClassPropertyParser(class_set=set())
        for i, value in enumerate(encoded_property_values):
            self.assertEquals(
                class_parser.get_property_value(property_name=property_name, encoded_property_value=value),
                expected_property_values[i]
            )

    # Invalid CSS patterns that yield an invalid output.
    def test_get_property_value_invalid_patterns(self):
        property_name = 'color'
        encoded_property_values = ['bold-50', '5u5', 'b1-a5-c1p-e5', '5pxrem', '1ap-10xp-3qp-1mp3', 'p12px']
        expected_property_values = ['bold 50', '5u5', 'b1 a5 c1% e5', '5pxrem', '1a% 10x% 3q% 1mp3', 'p12px']
        class_parser = ClassPropertyParser(class_set=set())
        for i, value in enumerate(encoded_property_values):
            self.assertEquals(
                class_parser.get_property_value(property_name=property_name, encoded_property_value=value),
                expected_property_values[i]
            )

    def test_is_important(self):
        expected_true = 'p-10-i'
        expected_false = 'height-50'
        class_parser = ClassPropertyParser(class_set=set())
        self.assertTrue(class_parser.is_important(css_class=expected_true))
        self.assertFalse(class_parser.is_important(css_class=expected_false))

    def test_strip_priority_designator(self):
        important = 'p-10-i'
        not_important = 'p-10'
        expected_value = 'p-10'
        class_parser = ClassPropertyParser(class_set=set())
        value = class_parser.strip_priority_designator(encoded_property_value=important)    # important
        self.assertEquals(value, expected_value)
        value = class_parser.strip_priority_designator(encoded_property_value=not_important)    # not important
        self.assertEquals(value, expected_value)

    def test_get_property_priority_important(self):
        expected_property_priority = 'IMPORTANT'
        class_set = {'font-weight-bold-i', 'font-weight-700-i', 'bold-i', 'normal-i'}
        class_parser = ClassPropertyParser(class_set=class_set)
        for css_class in class_parser.class_set:
            property_priority = class_parser.get_property_priority(css_class=css_class)
            self.assertEquals(property_priority, expected_property_priority)

    def test_get_property_priority_not_important(self):
        expected_property_priority = ''
        class_set = {'font-weight-bold', 'font-weight-700', 'bold', 'normal'}
        class_parser = ClassPropertyParser(class_set=class_set)
        for css_class in class_parser.class_set:
            property_priority = class_parser.get_property_priority(css_class=css_class)
            self.assertEquals(property_priority, expected_property_priority)
