# python 2
from __future__ import absolute_import, unicode_literals

# builtin
from unittest import TestCase, main
from shutil import copyfile
import os

# custom
from blowdrycss.filehandler import FileModificationComparator
from blowdrycss.utilities import unittest_file_path, change_settings_for_testing, delete_file_paths
import blowdrycss_settings as settings

change_settings_for_testing()


__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileModificationComparator(TestCase):
    def test_file_is_newer_wrong_path(self):
        not_a_directory = 'not/a/ valid /directory\\file.txt'
        file_modification_comparator = FileModificationComparator()
        self.assertRaises(OSError, file_modification_comparator.file_is_newer, not_a_directory)

    def test_file_is_newer_blowdry_css_missing(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path('test_css', '')                 # Change Setting

        html_file = unittest_file_path('test_html', 'index.html')                   # Create a temporary file

        copy_of_css = unittest_file_path('test_css', 'copy.css')
        css_file = unittest_file_path('test_css', 'blowdry.css')                    # Modify css_file
        copyfile(css_file, copy_of_css)                                             # Copy of blowdry.css
        delete_file_paths(file_paths=(css_file, ))                                  # Delete blowdry.css

        comparator = FileModificationComparator()
        self.assertRaises(OSError, comparator.file_is_newer, html_file)

        copyfile(copy_of_css, css_file)                                             # Copy back original file
        delete_file_paths(file_paths=(copy_of_css, ))                               # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings

    def test_file_is_newer(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path('test_css', '')                 # Change Setting
        temp_file = unittest_file_path('test_css', 'temp.html')                     # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('test test test')

        css_file = unittest_file_path('test_css', 'blowdry.css')
        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        file_modification_comparator = FileModificationComparator()

        self.assertTrue(a < b)
        self.assertTrue(file_modification_comparator.file_is_newer(file_path=temp_file))

        delete_file_paths(file_paths=(temp_file, ))                                 # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings

    def test_file_is_NOT_newer(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path('test_css', '')                 # Change Setting

        temp_file = unittest_file_path('test_css', 'temp.html')                     # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('test test test')

        copy_of_css = unittest_file_path('test_css', 'copy.css')
        css_file = unittest_file_path('test_css', 'blowdry.css')                    # Modify css_file
        copyfile(css_file, copy_of_css)                                             # Copy of blowdry.css

        with open(css_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        comparator = FileModificationComparator()

        self.assertFalse(a < b)
        self.assertFalse(comparator.file_is_newer(file_path=temp_file))

        copyfile(copy_of_css, css_file)                                             # Copy back original file
        delete_file_paths(file_paths=(temp_file, copy_of_css, ))                    # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings


if __name__ == '__main__':
    main()
