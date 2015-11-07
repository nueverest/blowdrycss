from unittest import TestCase
from htmlattributeparser import HTMLClassParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestHTMLClassParser(TestCase):
    def test_set_class_set(self):
        expected_output = {'c-blue', 'text-align-center', 'margin-20', 'padding-10', 'hide'}
        test_file_path = 'C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\ExampleSite\\test.html'
        class_parser = HTMLClassParser(files=[test_file_path])
        self.assertEquals(class_parser.class_set, expected_output)
