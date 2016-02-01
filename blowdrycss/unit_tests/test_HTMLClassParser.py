# builtin
from unittest import TestCase, main
from os import path, getcwd
# custom
try:
    from htmlparser import HTMLClassParser
except ImportError:
    from blowdrycss.htmlparser import HTMLClassParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestHTMLClassParser(TestCase):
    def test_set_class_set(self):
        expected_output = {'c-blue', 'text-align-center', 'margin-20', 'padding-10', 'hide'}
        test_file_path = path.join(getcwd(), 'test_html', 'test.html')
        class_parser = HTMLClassParser(files=[test_file_path])
        self.assertEquals(class_parser.class_set, expected_output)


if __name__ == '__main__':
    main()

