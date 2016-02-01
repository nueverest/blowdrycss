# python 2
from __future__ import division
from builtins import round
# general
from unittest import TestCase, main
from os import getcwd, path
# custom
from settings import blowdrycss_settings as settings
from change_settings import change_settings_for_testing
from utilities import contains_a_digit, deny_empty_or_whitespace, get_file_path

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


# Change settings directories for testing
change_settings_for_testing()


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
        self.assertEqual(deny_empty_or_whitespace(string='valid_string', variable_name='valid_variable'), None)

    def test_deny_empty_or_whitespace_invalid_string(self):
        invalid = ['', None, '          ']
        for string in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, string, 'valid_variable')

    def test_deny_empty_or_whitespace_invalid_variable_name(self):
        invalid = ['', None, '          ']
        for variable_name in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, 'valid_string', variable_name)

    def test_get_file_path(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extensions = ['.css', '.min.css', '.txt', '.mp3', '.anything', '.md', '.html', '.rst']

        for extension in extensions:
            expected_file_path = path.join(getcwd(), file_name + extension)
            file_path = get_file_path(file_directory=file_directory, file_name=file_name, extension=extension)
            self.assertEqual(file_path, expected_file_path)

    def test_get_file_path_empty_input_valueerrror(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extension = '.css'

        self.assertRaises(ValueError, get_file_path, '', file_name, extension)
        self.assertRaises(ValueError, get_file_path, file_directory, '', extension)
        self.assertRaises(ValueError, get_file_path, file_directory, file_name, '')

    def test_get_file_path_invalid_extension(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extensions = ['.c$@$0f00ss', '.min.!@#css', '.tx^*()&)/\t', '.a@\nything', 'txt', 'md.', '.min.']

        for extension in extensions:
            self.assertRaises(ValueError, get_file_path, file_directory, file_name, extension)

    def test_px_to_em_typecast_string_input(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = settings.px_to_em(pixels=str(pixels))  # typecast to string str()
            self.assertEqual(actual, str(expected), msg=pixels)


    def test_px_to_em_int_input(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_float_input(self):
        base = 16
        # Thank you: http://stackoverflow.com/questions/477486/python-decimal-range-step-value#answer-477506
        for pixels in range(-11, 11, 1):
            pixels /= 10.0
            expected = round(float(pixels) / float(base), 4)
            expected = str(expected) + 'em'
            actual = settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=str(pixels) + ': ' + str(actual) + ' vs ' + str(expected))

    def test_px_to_em_invalid_input(self):
        # Expect the value to pass through unchanged.
        invalid_inputs = ['1 2', '5 6 5 6', 'cat', '11px', ' 234.8', 'n2_4p', '25deg', '16kHz', ]
        for invalid in invalid_inputs:
            expected = invalid
            actual = settings.px_to_em(pixels=invalid)
            self.assertEqual(actual, expected, msg=invalid)

    def test_px_to_em_change_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=str(actual) + ' vs ' + str(expected))

    def test_px_to_em_string_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_Wrong_base(self):
        settings.base = 'aoenth'
        self.assertRaises(ValueError, settings.px_to_em, pixels='32')
        settings.base = 16

if __name__ == '__main__':
    main()
