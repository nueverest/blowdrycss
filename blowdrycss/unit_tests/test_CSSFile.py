# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
from os import path, remove

# custom
from blowdrycss.filehandler import CSSFile
from blowdrycss.utilities import unittest_file_path
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestCSSFile(TestCase):
    def test_not_a_directory(self):
        # Save original values.
        css_directory = settings.css_directory

        # Change settings
        settings.css_directory = '/a/ invalid /directory/file.txt'    # Spaces added around 'invalid' to make it invalid.

        self.assertRaises(OSError, CSSFile)

        # Reset settings values.
        settings.css_directory = css_directory

    def test_write_created(self):
        # Save original values.
        css_directory = settings.css_directory

        # Change settings
        settings.css_directory = unittest_file_path(folder='test_css')

        css_file = CSSFile()
        file_path = path.join(settings.css_directory, 'blowdry.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_file.write()
        self.assertTrue(path.isfile(file_path))

        # Reset settings values.
        settings.css_directory = css_directory

    def test_write_verify_css_text(self):
        # Save original values.
        css_directory = settings.css_directory

        # Change settings
        settings.css_directory = unittest_file_path(folder='test_css')

        css_file = CSSFile()
        file_path = path.join(settings.css_directory, css_file.file_name + '.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_text = b'.bold {\n    font-weight: bold\n    }\n.margin-top-50px {\n    margin-top: 50px\n    }\n' \
                   b'.c-blue {\n    color: blue\n    }\n.height-50px {\n    height: 50px\n    }\n' \
                   b'.bgc-h000 {\n    background-color: #000\n    }\n.color-hfff {\n    color: #fff\n    }\n' \
                   b'.valign-middle {\n    vertical-align: middle\n    }\n.height-150px {\n    height: 150px\n    }\n' \
                   b'.text-align-center {\n    text-align: center\n    }'
        expected_string = css_text.decode('utf-8')
        css_file.write(css_text=css_text)
        with open(file_path, 'r') as css_file:
            file_string = css_file.read()
        self.assertEqual(file_string, expected_string)

        # Reset settings values.
        settings.css_directory = css_directory

    def test_minify_created(self):
        # Save original values.
        css_directory = settings.css_directory

        # Change settings
        settings.css_directory = unittest_file_path(folder='test_css')

        css_file = CSSFile()
        file_path = path.join(css_file.file_directory, 'blowdry.min.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_file.minify()
        self.assertTrue(path.isfile(file_path))

        # Reset settings values.
        settings.css_directory = css_directory

    def test_minify_verify_css_text(self):
        # Save original values.
        css_directory = settings.css_directory

        # Change settings
        settings.css_directory = unittest_file_path(folder='test_css')

        css_file = CSSFile()
        file_path = path.join(settings.css_directory, css_file.file_name + '.min.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_text = b'.bold {\n    font-weight: bold\n    }\n.margin-top-50px {\n    margin-top: 50px\n    }\n' \
                   b'.c-blue {\n    color: blue\n    }\n.height-50px {\n    height: 50px\n    }\n' \
                   b'.bgc-h000 {\n    background-color: #000\n    }\n.color-hfff {\n    color: #fff\n    }\n' \
                   b'.valign-middle {\n    vertical-align: middle\n    }\n.height-150px {\n    height: 150px\n    }\n' \
                   b'.text-align-center {\n    text-align: center\n    }'
        expected_string = '.bold{font-weight:bold}.margin-top-50px{margin-top:50px}.c-blue{color:blue}' \
                          '.height-50px{height:50px}.bgc-h000{background-color:#000}.color-hfff{color:#fff}' \
                          '.valign-middle{vertical-align:middle}.height-150px{height:150px}' \
                          '.text-align-center{text-align:center}'
        css_file.minify(css_text=css_text)
        with open(file_path, 'r') as css_file:
            file_string = css_file.read()
        self.assertEqual(file_string, expected_string, msg=file_string)

        # Reset settings values.
        settings.css_directory = css_directory

    def test_write_created_custom_output_file_data(self):
        # Save original values.
        css_directory = settings.css_directory
        output_file_name = settings.output_file_name
        output_extension = settings.output_extension

        # Change settings
        settings.css_directory = unittest_file_path(folder='test_css')
        settings.output_file_name = '_custom'
        settings.output_extension = '.scss'

        css_file = CSSFile()
        expected = '_custom.scss'
        file_path = path.join(settings.css_directory, expected)

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_file.write()
        self.assertTrue(path.isfile(file_path))

        # Reset settings values.
        settings.css_directory = css_directory
        settings.output_file_name = output_file_name
        settings.output_extension = output_extension


if __name__ == '__main__':
    main()
