# builtins
from unittest import TestCase, main
from os import path
# custom
try:
    from filehandler import ClassExtractor, FileRegexMap
except ImportError:
    from blowdrycss.filehandler import ClassExtractor, FileRegexMap


class TestClassExtractor(TestCase):
    def test_raw_class_list_aspx(self):
        expected_raw_class_list = [
            ' row bgc-green padding-top-30 padding-bottom-30', 'row padding-top-30 padding-bottom-30 ',
            'row padding-top-30 padding-bottom-30 ', 'row '
        ]
        aspx_file = path.join('test_aspx', 'test.aspx')
        aspx_sub = r'<%.*?%>'
        aspx_findall = r'class="(.*?)"'
        class_extractor = ClassExtractor(file_path=aspx_file, sub_regex=aspx_sub, findall_regex=aspx_findall)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    def test_raw_class_list_jinja(self):
        expected_raw_class_list = [
            'purple  padding-left-5', ' squirrel text-align-center', 'large-up  border-1', 'row text-align-center', ''
        ]
        jinja2_file = path.join('test_jinja', 'test.jinja2')
        jinja2_sub = r'{.*?}?}'
        jinja2_findall = r'class="(.*?)"'
        class_extractor = ClassExtractor(file_path=jinja2_file, sub_regex=jinja2_sub, findall_regex=jinja2_findall)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    def test_class_set_aspx(self):
        expected_class_set = {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
        aspx_file = path.join('test_aspx', 'test.aspx')
        aspx_sub = r'<%.*?%>'
        aspx_findall = r'class="(.*?)"'
        class_extractor = ClassExtractor(file_path=aspx_file, sub_regex=aspx_sub, findall_regex=aspx_findall)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center'
        }
        jinja2_file = path.join('test_jinja', 'test.jinja2')
        jinja2_sub = r'{.*?}?}'
        jinja2_findall = r'class="(.*?)"'
        class_extractor = ClassExtractor(file_path=jinja2_file, sub_regex=jinja2_sub, findall_regex=jinja2_findall)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_wrong_path_OSError(self):
        self.assertRaises(OSError, ClassExtractor, 'wrong_path', r'', r'')

    # Integration testing
    def test_integration_class_set_aspx(self):
        expected_class_set = {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
        aspx_file = path.join('test_aspx', 'test.aspx')
        file_regex_map = FileRegexMap(_path=aspx_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
                file_path=aspx_file, sub_regex=regex_dict['sub_regex'], findall_regex=regex_dict['findall_regex']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center'
        }
        jinja2_file = path.join('test_jinja', 'test.jinja2')
        file_regex_map = FileRegexMap(_path=jinja2_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
                file_path=jinja2_file, sub_regex=regex_dict['sub_regex'], findall_regex=regex_dict['findall_regex']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)


if __name__ == '__main__':
    main()
