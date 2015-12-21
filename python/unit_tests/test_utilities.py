from unittest import TestCase, main
from os import getcwd, path
# custom
from utilities import contains_a_digit, deny_empty_or_whitespace, get_file_path
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

if __name__ == '__main__':
    main()
