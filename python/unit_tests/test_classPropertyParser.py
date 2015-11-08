from unittest import TestCase
from cssparser import ClassPropertyParser


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


    # def test_clean_class_set(self):
    #     self.fail()
    #
    # def test_get_property_name(self):
    #     self.fail()
    #
    # def test_get_encoded_property_value(self):
    #     self.fail()
    #
    # def test_get_property_value(self):
    #     self.fail()
    #
    # def test_get_property_priority(self):
    #     self.fail()
