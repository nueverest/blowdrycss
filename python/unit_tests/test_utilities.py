from unittest import TestCase, main
# custom
from utilities import contains_a_digit
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class Test_contains_a_digit(TestCase):
    def test_contains_a_digit_true(self):
        digits = ['n12px', '1p 7p 1p 7p', '-1_25em', '-1.35%', 'rgba 255 0 0 0.5', 'h0ff48f']
        for value in digits:
            self.assertTrue(contains_a_digit(value=value), msg=value)

    def test_contains_a_digit_false(self):
        no_digits = ['bold', 'none', 'left']
        for value in no_digits:
            self.assertFalse(contains_a_digit(value=value), msg=value)


if __name__ == '__main__':
    main()
