# python 2
from __future__ import absolute_import, division
from builtins import round

# builtins
from unittest import TestCase, main
from os import getcwd, path, removedirs
import sys
from io import StringIO, open

# custom
import blowdrycss.unit_tests.unittest_settings as unittest_settings
from blowdrycss.utilities import contains_a_digit, deny_empty_or_whitespace, get_file_path, unittest_file_path, \
    change_settings_for_testing, print_css_stats, print_blow_dryer, make_directory, delete_file_paths
import blowdrycss_settings as settings

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
            actual = unittest_settings.px_to_em(pixels=str(pixels))  # typecast to string str()
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_int_input(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_float_input(self):
        base = 16
        # Thank you: http://stackoverflow.com/questions/477486/python-decimal-range-step-value#answer-477506
        for pixels in range(-11, 11, 1):
            pixels /= 10.0
            expected = round(float(pixels) / float(base), 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=str(pixels) + ': ' + str(actual) + ' vs ' + str(expected))

    def test_px_to_em_invalid_input(self):
        # Expect the value to pass through unchanged.
        invalid_inputs = ['1 2', '5 6 5 6', 'cat', '11px', ' 234.8', 'n2_4p', '25deg', '16kHz', ]
        for invalid in invalid_inputs:
            expected = invalid
            actual = unittest_settings.px_to_em(pixels=invalid)
            self.assertEqual(actual, expected, msg=invalid)

    def test_px_to_em_change_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=str(actual) + ' vs ' + str(expected))

    def test_px_to_em_string_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_Wrong_base(self):
        unittest_settings.base = 'aoenth'
        self.assertRaises(ValueError, unittest_settings.px_to_em, pixels='32')
        unittest_settings.base = 16

    def test_unittest_file_path(self):
        folders = ['test_aspx', 'test_jinja', ]
        filenames = ['test.aspx', 'test.jinja2', ]

        for i, folder in enumerate(folders):
            the_path = unittest_file_path(folder, filenames[i])
            self.assertTrue(path.isfile(the_path))

    def test_unittest_file_path_exact_path(self):
        folder = 'test_html'
        filename = 'index.html'
        cwd = getcwd()
        expected_if_path = path.join(cwd, folder, filename)
        expecetd_else_path = path.join(cwd, 'blowdrycss', 'unit_tests', folder, filename)

        test_path = unittest_file_path(folder=folder, filename=filename)

        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            self.assertTrue(test_path, expected_if_path)
        else:                                                       # Run unittest cmd from the root directory.
            self.assertTrue(test_path, expecetd_else_path)

    def test_change_settings_for_testing(self):
        cwd = getcwd()

        if_cases = (
            settings.markdown_directory == path.join(cwd, 'test_markdown'),
            settings.project_directory == path.join(cwd, 'test_examplesite'),
            settings.css_directory == path.join(settings.project_directory, 'test_css'),
            settings.docs_directory == path.join(cwd, 'test_docs'),
        )
        else_cases = (
            settings.markdown_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_markdown'),
            settings.project_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite'),
            settings.css_directory == path.join(settings.project_directory, 'test_css'),
            settings.docs_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_docs'),
        )

        change_settings_for_testing()

        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            for if_case in if_cases:
                self.assertTrue(if_case)
        else:                                                       # Run unittest cmd from the root directory.
            for else_case in else_cases:
                self.assertTrue(else_case)

    def test_print_css_stats(self):
        substrings = [
            'blowdry.css:\t 0.3kB',
            'blowdry.min.css: 0.2kB',
            'CSS file size reduced by 67.5%.'
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            print_css_stats(file_name='blowdry')

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

    def test_print_blow_dryer(self):
        # Warning: Do not change the indentation.
        expected_ascii = """
                     .-'-.
                  ;@@@@@@@@@'
    ~~~~ ;@@@@@@@@@@@@@@@@@@@+`
    ~~~~ ;@@@@@@@@@@@@@``@@@@@@
                +@@@@@`  `@@@@@'
                   @@@@``@@@@@
                     .-@@@@@@@+
                          @@@@@
                           .@@@.
                            `@@@.
    """
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            print_blow_dryer()

            output = out.getvalue()
            self.assertTrue(expected_ascii in output, msg=expected_ascii + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout

    def test_make_directory_non_existing(self):
        directory_name = 'test_make_directory'
        directory = unittest_file_path(folder=directory_name)

        if path.isdir(directory):       # Remove test directory
            removedirs(directory)

        self.assertFalse(path.isdir(directory))
        make_directory(directory=directory)
        self.assertTrue(path.isdir(directory))

        if path.isdir(directory):       # Remove test directory
            removedirs(directory)

    def test_make_directory_pre_existing(self):
        directory_name = 'test_html'                    # pre-existing case
        directory = unittest_file_path(folder=directory_name)

        self.assertTrue(path.isdir(directory))
        make_directory(directory=directory)             # should do nothing
        self.assertTrue(path.isdir(directory))

    def test_delete_file_paths(self):
        file_paths = (
            unittest_file_path('test_examplesite', 'file1.html'),
            unittest_file_path('test_examplesite', 'file2.html'),
            unittest_file_path('test_examplesite', 'file3.html'),
        )

        # create files to delete
        text = 'test123'
        self.assertTrue(path.isdir(unittest_file_path('test_examplesite', '')))

        for file_path in file_paths:
            with open(file_path, 'wb') as generic_file:
                generic_file.write(bytearray(text, 'utf-8'))

        # assert they exist
        for file_path in file_paths:
            self.assertTrue(path.isfile(file_path))

        # delete them
        delete_file_paths(file_paths=file_paths)

        # assert they don't exist
        for file_path in file_paths:
            self.assertFalse(path.isfile(file_path))

if __name__ == '__main__':
    main()
