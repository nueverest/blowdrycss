# python 2
from __future__ import absolute_import, unicode_literals

# builtin
from unittest import TestCase, main
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

    def test_is_newer_SystemError_wrong_settings(self):
        css_directory = settings.css_directory                                      # Save original setting
        human_readable = settings.human_readable
        minify = settings.minify

        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting
        settings.human_readable = False
        settings.minify = False

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        css_file = unittest_file_path(settings.css_directory, 'blowdry.css')
        with open(css_file, 'w') as generic_file:
            generic_file.write('test test test')

        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        comparator = FileModificationComparator()
        self.assertRaises(SystemError, comparator.is_newer, temp_file)

        delete_file_paths((temp_file, css_file, ))
        settings.css_directory = css_directory                                      # Reset Settings
        settings.human_readable = human_readable
        settings.minify = minify

    def test_is_newer_blowdry_css_missing(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))
        
        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        css_file = unittest_file_path('test_recent', 'blowdry.css')                 # Modify css_file
        delete_file_paths(file_paths=(css_file, ))                                  # Delete blowdry.css

        comparator = FileModificationComparator()
        self.assertTrue(comparator.is_newer(temp_file))

        settings.css_directory = css_directory                                      # Reset Settings

    def test_is_newer_blowdry_min_css_missing(self):
        css_directory = settings.css_directory                                      # Save original setting
        human_readable = settings.human_readable
        minify = settings.minify

        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting
        settings.human_readable = False
        settings.minify = True

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        css_file = unittest_file_path('test_recent', 'blowdry.css')                 # Modify css_file
        delete_file_paths(file_paths=(css_file, ))                                  # Delete blowdry.css

        comparator = FileModificationComparator()
        self.assertTrue(comparator.is_newer(temp_file))

        delete_file_paths((temp_file, css_file))
        settings.css_directory = css_directory                                      # Reset Settings
        settings.human_readable = human_readable
        settings.minify = minify

    def test_is_newer_blowdry_css(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        css_file = unittest_file_path(settings.css_directory, 'blowdry.css')
        with open(css_file, 'w') as generic_file:
            generic_file.write('test test test')

        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        file_modification_comparator = FileModificationComparator()

        self.assertTrue(a <= b, msg='%s is not less than or equal to %s' % (a, b))
        self.assertTrue(file_modification_comparator.is_newer(file_path=temp_file))

        delete_file_paths(file_paths=(temp_file, css_file))                         # Clean up files
        settings.css_directory = css_directory                                      # Reset Settings

    def test_is_newer_blowdry_min_css(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting
        human_readable = settings.human_readable
        minify = settings.minify

        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting
        settings.human_readable = False
        settings.minify = True

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        css_min_file = unittest_file_path(settings.css_directory, 'blowdry.min.css')
        with open(css_min_file, 'w') as generic_file:
            generic_file.write('test test test')

        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        a = os.path.getmtime(css_min_file)                                          # Get Modification Times
        b = os.path.getmtime(temp_file)

        file_modification_comparator = FileModificationComparator()

        self.assertTrue(a <= b, msg='%s is not less than or equal to %s' % (a, b))
        self.assertTrue(file_modification_comparator.is_newer(file_path=temp_file))

        delete_file_paths((temp_file, css_min_file))
        settings.css_directory = css_directory                                      # Reset Settings
        settings.human_readable = human_readable
        settings.minify = minify

    def test_file_is_NOT_newer(self):
        css_directory = settings.css_directory                                      # Save original setting
        settings.css_directory = unittest_file_path(folder='test_recent')           # Change Setting

        make_directory(settings.css_directory)                                      # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        temp_file = unittest_file_path('test_recent', 'temp.html')                  # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('test test test')

        sleep(0.1)                                                                  # blowdry.css for Travis CI

        css_file = unittest_file_path(settings.css_directory, 'blowdry.css')
        with open(css_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        a = os.path.getmtime(css_file)                                              # Get Modification Times
        b = os.path.getmtime(temp_file)

        comparator = FileModificationComparator()

        self.assertFalse(a < b)
        self.assertFalse(comparator.is_newer(file_path=temp_file))

        delete_file_paths(file_paths=(temp_file, ))                                 # Delete temporary file
        settings.css_directory = css_directory                                      # Reset Settings


if __name__ == '__main__':
    main()
