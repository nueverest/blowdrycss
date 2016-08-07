# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main

# custom
from blowdrycss.classparser import FileRegexMap
from blowdrycss.utilities import unittest_file_path

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileRegexMap(TestCase):
    def test_is_valid_extension_true(self):
        file_paths = [unittest_file_path('test_aspx', 'test.aspx'), unittest_file_path('test_jinja', 'test.jinja2')]
        for _path in file_paths:
            file_regex_map = FileRegexMap(file_path=_path)
            self.assertTrue(file_regex_map.is_valid_extension(), msg=_path)

    def test_is_valid_extension_whitespace(self):
        file_paths = [unittest_file_path('test_aspx', 'test.aspx  '), unittest_file_path('test_jinja', 'test.jinja2 ')]
        for _path in file_paths:
            file_regex_map = FileRegexMap(file_path=_path)
            self.assertTrue(file_regex_map.is_valid_extension(), msg=_path)

    def test_is_valid_extension_false(self):
        wrong_extensions = ['.wrong', '.squirrel', '.incorrect']
        file_path = unittest_file_path('test_aspx', 'test.aspx')
        for wrong_extension in wrong_extensions:
            file_regex_map = FileRegexMap(file_path=file_path)
            file_regex_map.extension = wrong_extension
            self.assertFalse(file_regex_map.is_valid_extension())

    def test_is_valid_extension_raises_OSError(self):
        file_paths = [
            unittest_file_path('test_files', 'test.wrong'), unittest_file_path('test_files', 'test.incorrect')
        ]
        for _path in file_paths:
            self.assertRaises(OSError, FileRegexMap, _path)

    def test_regexes(self):
        sub_uri = (r'://', )
        sub_js = (
            r'//.*?\n',                                                     # Remove JS Comments.
            r'\n',                                                          # Remove new lines before block quotes.
            r'/\*.*?\*/',                                                   # Remove block quotes.
            r'(domClass.add\(\s*.*?,\s*["\'])',                             # dojo
            r'(domClass.add\(\s*.*?,\s*["\'])',
            r'(dojo.addClass\(\s*.*?,\s*["\'])',
            r'(domClass.remove\(\s*.*?,\s*["\'])',
            r'(dojo.removeClass\(\s*.*?,\s*["\'])',
            r'(YAHOO.util.Dom.addClass\(\s*.*?,\s*["\'])',                  # yui
            r'(YAHOO.util.Dom.hasClass\(\s*.*?,\s*["\'])',
            r'(YAHOO.util.Dom.removeClass\(\s*.*?,\s*["\'])',
            r'(.addClass\(\s*["\'])',                                       # jquery
            r'(.removeClass\(\s*["\'])',
            r'(\$\(\s*["\']\.)',
        )
        sub_html = sub_uri + sub_js + (r'<!--.*?-->', )
        sub_dotnet = sub_html + (r'<%--.*?--%>', r'<%.*?%>', )

        js_substring = r'extract__class__set'
        findall_regex_js = (
            r'.classList.add\(\s*[\'"](.*?)["\']\s*\)',
            r'.classList.remove\(\s*[\'"](.*?)["\']\s*\)',
            r'.className\s*\+?=\s*.*?[\'"](.*?)["\']',
            r'.getElementsByClassName\(\s*[\'"](.*?)["\']\s*\)',
            r'.setAttribute\(\s*[\'"]class["\']\s*,\s*[\'"](.*?)["\']\s*\)',
            js_substring + r'\(\s*[\'"](.*?)["\']\s*\)',                    # Find cases designated by js_substring.
        )

        expected_dicts = [
            {
                'sub_regexes': sub_dotnet,
                'findall_regexes': (r'class=[\'"](.*?)["\']', ) + findall_regex_js,
            },
            {
                'sub_regexes': (r'{.*?}?}', ) + sub_html + (r'{#.*?#}', ),
                'findall_regexes': (r'class=[\'"](.*?)["\']', ) + findall_regex_js,
            },
        ]
        file_paths = [unittest_file_path('test_aspx', 'test.aspx'), unittest_file_path('test_jinja', 'test.jinja2')]
        for i, _path in enumerate(file_paths):
            file_regex_map = FileRegexMap(file_path=_path)
            actual_dict = file_regex_map.regex_dict
            self.assertEqual(actual_dict, expected_dicts[i], msg=_path)


if __name__ == '__main__':
    main()
