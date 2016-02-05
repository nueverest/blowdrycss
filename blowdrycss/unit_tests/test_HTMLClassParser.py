# builtin
from unittest import TestCase, main
# custom
from blowdrycss.htmlparser import HTMLClassParser
from blowdrycss.utilities import unittest_file_path

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestHTMLClassParser(TestCase):
    def test_set_class_set(self):
        expected_output = {'c-blue', 'text-align-center', 'margin-20', 'padding-10', 'hide'}
        test_file_path = unittest_file_path('test_html', 'test.html')
        class_parser = HTMLClassParser(files=[test_file_path])
        self.assertEquals(class_parser.class_set, expected_output)


if __name__ == '__main__':
    main()

