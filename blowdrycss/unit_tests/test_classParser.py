# builtin
from unittest import TestCase, main
import sys
# custom
from blowdrycss.filehandler import FileFinder
from blowdrycss.classparser import ClassParser
from blowdrycss.utilities import unittest_file_path
# required for pycharm unittest feature to work under both python 2.7 and python 3.x
if sys.hexversion < 0x03000000:
    import blowdrycss.blowdrycss_settings as settings
else:
    import blowdrycss_settings as settings


class TestClassParser(TestCase):
    def test_build_file_path_list(self):
        expected_file_paths = {
            unittest_file_path('test_aspx', 'test.aspx'),
            unittest_file_path('test_jinja', 'test.jinja2'),
        }
        settings.file_types = ('*.html', '*.aspx', '*.jinja2')                                  # Override file_types
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        self.assertTrue('.aspx' in list(file_finder.file_dict), msg=settings.file_types)
        class_parser = ClassParser(file_dict=file_finder.file_dict)
        self.assertEqual(set(class_parser.file_path_list), expected_file_paths, msg=class_parser.file_path_list)
        settings.file_types = ('*.html', )                                                      # Reset file_types

    def test_build_class_set(self):
        expected_class_set = {
            'row', 'bgc-green', 'padding-top-30', 'padding-bottom-30',
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1',
        }
        settings.file_types = ('*.aspx', '*.jinja2')                                            # Override file_types
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        self.assertFalse('.html' in list(file_finder.file_dict), msg=settings.file_types)
        self.assertTrue('.aspx' in list(file_finder.file_dict), msg=settings.file_types)
        class_parser = ClassParser(file_dict=file_finder.file_dict)
        self.assertEqual(class_parser.class_set, expected_class_set, msg=class_parser.class_set)
        settings.file_types = ('*.html', )                                                      # Reset file_types


if __name__ == '__main__':
    main()


