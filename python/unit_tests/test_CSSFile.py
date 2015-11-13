from unittest import TestCase
from os import path, getcwd

# Custom
from filehandler import CSSFile
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestCSSFile(TestCase):
    def test_not_a_directory(self):
        not_a_directory = 'not/a/valid/directory/file.txt'
        file_name = 'some_file'
        self.assertRaises(NotADirectoryError, CSSFile, not_a_directory, file_name)

    def test_file_path(self):
        extensions = ['.css', '.min.css', '.txt', '.mp3', '.anything']
        css_file = CSSFile()

        for extension in extensions:
            expected_file_path = path.join(getcwd(), 'blowdry' + extension)
            file_path = css_file.file_path(extension=extension)
            self.assertEqual(file_path, expected_file_path)

    def test_file_path_invalid(self):
        extensions = ['.c$@$0f00ss', '.min.!@#css', '.tx^*()&)/\t', '.a@\nything']
        css_file = CSSFile()

        for extension in extensions:
            self.assertRaises(ValueError, css_file.file_path, extension)


    # def test_write(self):
    #
    # def test_minify(self):

