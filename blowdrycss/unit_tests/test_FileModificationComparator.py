# python 2
from __future__ import absolute_import, unicode_literals

# builtin
from unittest import TestCase, main
from shutil import copyfile
from time import sleep
import os

# custom
from blowdrycss.filehandler import FileModificationComparator
from blowdrycss.utilities import unittest_file_path, change_settings_for_testing, delete_file_paths, make_directory
import blowdrycss_settings as settings

change_settings_for_testing()


__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileModificationComparator(TestCase):
    def test_is_newer_wrong_path(self):
        not_a_directory = 'not/a/ valid /directory\\file.txt'
        file_modification_comparator = FileModificationComparator()
        self.assertRaises(OSError, file_modification_comparator.is_newer, not_a_directory)

    def test_is_newer_blowdry_css_missing(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_css')              # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))
        
        fake_file = unittest_file_path(filename='fake.html')                        # Define a fake file path

        copy_of_css = unittest_file_path('test_css', 'copy.css')
        css_file = unittest_file_path('test_css', 'blowdry.css')                    # Modify css_file
        copyfile(css_file, copy_of_css)                                             # Copy of blowdry.css
        delete_file_paths(file_paths=(css_file, ))                                  # Delete blowdry.css

        comparator = FileModificationComparator()
        self.assertRaises(OSError, comparator.is_newer, fake_file)

        copyfile(copy_of_css, css_file)                                             # Copy back original file
        delete_file_paths(file_paths=(copy_of_css, ))                               # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings

    def test_is_newer(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_css')              # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        css_file = unittest_file_path('test_css', 'blowdry.css')
        if not os.path.isfile(css_file):                                            # Create blowdry.css for Travis CI
            with open(css_file, 'w') as generic_file:
                generic_file.write('.bold {font-weight: bold}')
            sleep(0.001)

        temp_file = unittest_file_path('test_css', 'temp.html')                     # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('test test test')

        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        file_modification_comparator = FileModificationComparator()

        self.assertTrue(a < b)
        self.assertTrue(file_modification_comparator.is_newer(file_path=temp_file))

        delete_file_paths(file_paths=(temp_file, ))                                 # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings

    def test_file_is_NOT_newer(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_css')              # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        temp_file = unittest_file_path('test_css', 'temp.html')                     # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('test test test')

        css_file = unittest_file_path('test_css', 'blowdry.css')
        try:
            copy_of_css = unittest_file_path('test_css', 'copy.css')
            css_file = unittest_file_path('test_css', 'blowdry.css')                # Modify css_file
            copyfile(css_file, copy_of_css)                                         # Copy of blowdry.css
        except UnboundLocalError:
            sleep(0.001)                                                            # Travis Case

        with open(css_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        comparator = FileModificationComparator()

        self.assertFalse(a < b)
        self.assertFalse(comparator.is_newer(file_path=temp_file))

        copyfile(copy_of_css, css_file)                                             # Copy back original file
        delete_file_paths(file_paths=(temp_file, copy_of_css, ))                    # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings


if __name__ == '__main__':
    main()
