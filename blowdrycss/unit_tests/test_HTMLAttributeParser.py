# builtin
from unittest import TestCase, main
# custom
from blowdrycss.filehandler import FileConverter
from blowdrycss.htmlparser import HTMLAttributeParser
from blowdrycss.utilities import unittest_file_path


class TestHTMLAttributeParser(TestCase):
    def test_set_attribute_value_list(self):
        expected_output = ['c-blue text-align-center padding-10', 'padding-10 margin-20', 'hide']
        test_file_path = unittest_file_path('test_html', 'test.html')
        file_converter = FileConverter(file_path=test_file_path)
        file_string = file_converter.get_file_as_string()
        attribute_parser = HTMLAttributeParser(attribute_name='class')
        attribute_parser.feed(file_string)
        self.assertEqual(attribute_parser.attribute_value_list, expected_output)


if __name__ == '__main__':
    main()
