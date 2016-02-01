# builtin
from unittest import TestCase, main
from os import path, getcwd
# custom
try:
    from filehandler import FileConverter
    from htmlparser import HTMLAttributeParser
except ImportError:
    from blowdrycss.filehandler import FileConverter
    from blowdrycss.htmlparser import HTMLAttributeParser


class TestHTMLAttributeParser(TestCase):
    def test_set_attribute_value_list(self):
        expected_output = ['c-blue text-align-center padding-10', 'padding-10 margin-20', 'hide']
        test_file_path = path.join(getcwd(), 'test_html', 'test.html')
        file_converter = FileConverter(file_path=test_file_path)
        file_string = file_converter.get_file_as_string()
        attribute_parser = HTMLAttributeParser(attribute_name='class')
        attribute_parser.feed(file_string)
        self.assertEquals(attribute_parser.attribute_value_list, expected_output)


if __name__ == '__main__':
    main()
