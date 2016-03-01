# builtins
from unittest import TestCase, main
# custom
from blowdrycss.classparser import ClassExtractor, FileRegexMap
from blowdrycss.utilities import unittest_file_path


class TestClassExtractor(TestCase):
    # raw_class_list
    def test_raw_class_list_js(self):
        expected_raw_class_list = [
            'addclass1', ' addclass2 ', 'addclass3', ' addclass4a addclass4b addclass4c ',
            'addclass5', ' addclass6 ', 'addclass7', ' addclass8a addclass8b addclass8c ',
        ]
        js_file = unittest_file_path('test_js', 'test.js')
        sub_js = (r'//.*?\n', r'/\*.*?\*/', )
        findall_js = (r'.classList.add\(\s*[\'"](.*?)["\']\s*\)', )
        class_extractor = ClassExtractor(file_path=js_file, sub_regexes=sub_js, findall_regexes=findall_js)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    def test_raw_class_list_aspx(self):
        expected_raw_class_list = [
            ' row bgc-green padding-top-30 padding-bottom-30', 'row padding-top-30 padding-bottom-30 ',
            'row padding-top-30 padding-bottom-30 ', 'row '
        ]
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        aspx_sub = (r'<%.*?%>', )
        aspx_findall = (r'class="(.*?)"', )
        class_extractor = ClassExtractor(file_path=aspx_file, sub_regexes=aspx_sub, findall_regexes=aspx_findall)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    def test_raw_class_list_jinja(self):
        expected_raw_class_list = [
            'purple  padding-left-5', ' squirrel text-align-center', 'large-up  border-1', 'row text-align-center', ''
        ]
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        jinja2_sub = (r'{.*?}?}', )
        jinja2_findall = (r'class="(.*?)"', )
        class_extractor = ClassExtractor(file_path=jinja2_file, sub_regexes=jinja2_sub, findall_regexes=jinja2_findall)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    # class_set
    def test_class_set_js(self):
        expected_class_set = {
            'addclass1', 'addclass2', 'addclass3', 'addclass4a', 'addclass4b', 'addclass4c',
            'addclass5', 'addclass6', 'addclass7', 'addclass8a', 'addclass8b', 'addclass8c',
        }
        js_file = unittest_file_path('test_js', 'test.js')
        sub_js = (r'//.*?\n', r'/\*.*?\*/', )
        findall_js = (r'.classList.add\(\s*[\'"](.*?)["\']\s*\)', )
        class_extractor = ClassExtractor(file_path=js_file, sub_regexes=sub_js, findall_regexes=findall_js)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_aspx(self):
        expected_class_set = {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        aspx_sub = (r'<%.*?%>', )
        aspx_findall = (r'class="(.*?)"', )
        class_extractor = ClassExtractor(file_path=aspx_file, sub_regexes=aspx_sub, findall_regexes=aspx_findall)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center'
        }
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        jinja2_sub = (r'{.*?}?}', )
        jinja2_findall = (r'class="(.*?)"', )
        class_extractor = ClassExtractor(file_path=jinja2_file, sub_regexes=jinja2_sub, findall_regexes=jinja2_findall)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_ruby_erb(self):
        expected_class_set = {
            'font-size-53', 'brown', 'text-align-right', 'medium-down',
        }
        erb_file = unittest_file_path('test_erb', 'test.erb')
        erb_sub = (r'{.*?}?}', )
        erb_findall = (r'class="(.*?)"', )
        class_extractor = ClassExtractor(file_path=erb_file, sub_regexes=erb_sub, findall_regexes=erb_findall)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_wrong_path_OSError(self):
        self.assertRaises(OSError, ClassExtractor, 'wrong_path', r'', r'')

    # Integration testing
    def test_integration_class_set_js(self):
        expected_class_set = {
            'addclass1', 'addclass2', 'addclass3', 'addclass4a', 'addclass4b', 'addclass4c',
            'addclass5', 'addclass6', 'addclass7', 'addclass8a', 'addclass8b', 'addclass8c',
            'removeclass1', 'removeclass2', 'removeclass3', 'removeclass4a', 'removeclass4b', 'removeclass4c',
            'removeclass5', 'removeclass6', 'removeclass7', 'removeclass8a', 'removeclass8b', 'removeclass8c',
        }
        js_file = unittest_file_path('test_js', 'test.js')
        file_regex_map = FileRegexMap(file_path=js_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
            file_path=js_file, sub_regexes=regex_dict['sub_regexes'], findall_regexes=regex_dict['findall_regexes']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)
    
    def test_integration_class_set_aspx(self):
        expected_class_set = {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        file_regex_map = FileRegexMap(file_path=aspx_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
            file_path=aspx_file, sub_regexes=regex_dict['sub_regexes'], findall_regexes=regex_dict['findall_regexes']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center'
        }
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        file_regex_map = FileRegexMap(file_path=jinja2_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
            file_path=jinja2_file, sub_regexes=regex_dict['sub_regexes'], findall_regexes=regex_dict['findall_regexes']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_ruby_erb(self):
        expected_class_set = {
            'font-size-53', 'brown', 'text-align-right', 'medium-down',
        }
        erb_file = unittest_file_path('test_erb', 'test.erb')
        file_regex_map = FileRegexMap(file_path=erb_file)
        regex_dict = file_regex_map.regex_dict
        class_extractor = ClassExtractor(
            file_path=erb_file, sub_regexes=regex_dict['sub_regexes'], findall_regexes=regex_dict['findall_regexes']
        )
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)


if __name__ == '__main__':
    main()
