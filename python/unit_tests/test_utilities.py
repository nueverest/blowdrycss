from unittest import TestCase, main
# custom
from utilities import contains_a_digit, deny_empty_or_whitespace
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class Test_utilities(TestCase):
    def test_contains_a_digit_true(self):
        digits = ['n12px', '1p 7p 1p 7p', '-1_25em', '-1.35%', 'rgba 255 0 0 0.5', 'h0ff48f']
        for value in digits:
            self.assertTrue(contains_a_digit(string=value), msg=value)

    def test_contains_a_digit_false(self):
        no_digits = ['bold', 'none', 'left']
        for value in no_digits:
            self.assertFalse(contains_a_digit(string=value), msg=value)

    def test_deny_empty_or_whitespace_valid(self):
        self.assertIsNone(deny_empty_or_whitespace(string='valid_string', variable_name='valid_variable'))

    def test_deny_empty_or_whitespace_invalid_string(self):
        invalid = ['', None, '          ']
        for string in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, string, 'valid_variable')

    def test_deny_empty_or_whitespace_invalid_variable_name(self):
        invalid = ['', None, '          ']
        for variable_name in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, 'valid_string', variable_name)


if __name__ == '__main__':
    main()
