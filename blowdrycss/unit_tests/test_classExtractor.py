# builtins
from unittest import TestCase, main
# custom
from blowdrycss.classparser import ClassExtractor
from blowdrycss.utilities import unittest_file_path


class TestClassExtractor(TestCase):
    # raw_class_list
    def test_raw_class_list_js(self):
        expected_raw_class_set = {
            'addclass1', 'addclass2', 'addclass3', 'addclass4', 'addclass5', 'addclass6',
            'removeclass1', 'removeclass2', 'removeclass3', 'removeclass4', 'removeclass5', 'removeclass6',
            'className1', 'className2', ' className3 ', 'className4a className4b className4c', 'className5',
            'className6', ' className7 ', 'className8a className8b className8c', 'className9a', 'className9b',
            'className10', 'className11', 'className12', ' className13 ', 'className14a className14b className14c',
            'className15', 'className16', 'className17', 'className18', 'className19', 'className20', 'className21',
            'className22', 'blue',
            'setAttribute1', 'setAttribute2', 'setAttribute3a setAttribute3b setAttribute3c',
            'getElementsByClassName1', 'getElementsByClassName2',
            'dojo1', 'dojo2', 'dojo3 dojo4', 'dojo5 dojo6', 'dojo7', 'dojo8', 'dojo9 dojo10', 'dojo11 dojo12',
            'dojo13', 'dojo14', 'dojo15 dojo16', 'dojo17 dojo18', 'dojo19', 'dojo20',
            'dojo21 dojo22', 'dojo23 dojo24',
            'jquery1', 'jquery2', 'jquery3', 'jquery4 jquery5', 'jquery6 jquery7', 'jquery8',
            'jquery9 jquery10', 'jquery11', 'jquery12 jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
            'yui1', 'yui2', ' yui3 yui4 ', ' yui5 yui6 ', 'yui7', 'yui8',
        }
        js_file = unittest_file_path('test_js', 'test.js')
        class_extractor = ClassExtractor(file_path=js_file)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(set(actual_raw_class_list), expected_raw_class_set)

    def test_raw_class_list_aspx(self):
        expected_raw_class_list = [
            ' row bgc-green padding-top-30 padding-bottom-30', 'row padding-top-30 padding-bottom-30 ',
            'row padding-top-30 padding-bottom-30 ', 'row ',
            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4 jquery5', 'jquery6 jquery7', 'jquery8',
            'jquery9 jquery10', 'jquery11', 'jquery12 jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        ]
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    def test_raw_class_list_jinja(self):
        expected_raw_class_list = [
            'purple  padding-left-5', ' squirrel text-align-center', 'large-up  border-1', 'row text-align-center', '',
            # Embedded <script></script>
            'dojo1', 'dojo2', 'dojo3 dojo4', 'dojo5 dojo6', 'dojo7', 'dojo8', 'dojo9 dojo10', 'dojo11 dojo12',
        ]
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        class_extractor = ClassExtractor(file_path=jinja2_file)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list)

    # class_set
    def test_class_set_js(self):
        expected_class_set = {
            'addclass1', 'addclass2', 'addclass3', 'addclass4', 'addclass5', 'addclass6',
            'removeclass1', 'removeclass2', 'removeclass3', 'removeclass4', 'removeclass5', 'removeclass6',
            'className1', 'className2', 'className3', 'className4a', 'className4b', 'className4c', 'className5',
            'className6', 'className7', 'className8a', 'className8b', 'className8c', 'className9a', 'className9b',
            'className10', 'className11', 'className12', 'className13', 'className14a', 'className14b', 'className14c',
            'className15', 'className16', 'className17', 'className18', 'className19', 'className20', 'className21',
            'className22', 'blue',
            'setAttribute1', 'setAttribute2', 'setAttribute3a', 'setAttribute3b', 'setAttribute3c',
            'getElementsByClassName1', 'getElementsByClassName2',
            'dojo1', 'dojo2', 'dojo3', 'dojo4', 'dojo5', 'dojo6', 'dojo7', 'dojo8', 'dojo9', 'dojo10', 'dojo11',
            'dojo12', 'dojo13', 'dojo14', 'dojo15', 'dojo16', 'dojo17', 'dojo18', 'dojo19', 'dojo20',
            'dojo21', 'dojo22', 'dojo23', 'dojo24',
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
            'yui1', 'yui2', 'yui3', 'yui4', 'yui5', 'yui6', 'yui7', 'yui8',
        }
        js_file = unittest_file_path('test_js', 'test.js')
        class_extractor = ClassExtractor(file_path=js_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_aspx(self):
        expected_class_set = {
            'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green',
            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        }
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center',
            # Embedded <script></script>
            'dojo1', 'dojo2', 'dojo3', 'dojo4', 'dojo5', 'dojo6', 'dojo7', 'dojo8', 'dojo9', 'dojo10', 'dojo11',
            'dojo12',
        }
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        class_extractor = ClassExtractor(file_path=jinja2_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_ruby_erb(self):
        expected_class_set = {
            'font-size-53', 'brown', 'text-align-right', 'medium-down',
            # Embedded <script></script>
            'yui1', 'yui2', 'yui3', 'yui4', 'yui5', 'yui6', 'yui7', 'yui8',
        }
        erb_file = unittest_file_path('test_erb', 'test.erb')
        class_extractor = ClassExtractor(file_path=erb_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_wrong_path_OSError(self):
        self.assertRaises(OSError, ClassExtractor, 'wrong_path')

    # Integration testing
    def test_integration_class_set_js(self):
        expected_class_set = {
            'addclass1', 'addclass2', 'addclass3', 'addclass4', 'addclass5', 'addclass6',
            'removeclass1', 'removeclass2', 'removeclass3', 'removeclass4', 'removeclass5', 'removeclass6',
            'className1', 'className2', 'className3', 'className4a', 'className4b', 'className4c', 'className5',
            'className6', 'className7', 'className8a', 'className8b', 'className8c', 'className9a', 'className9b',
            'className10', 'className11', 'className12', 'className13', 'className14a', 'className14b', 'className14c',
            'className15', 'className16', 'className17', 'className18', 'className19', 'className20', 'className21',
            'className22', 'blue',
            'setAttribute1', 'setAttribute2', 'setAttribute3a', 'setAttribute3b', 'setAttribute3c',
            'getElementsByClassName1', 'getElementsByClassName2',
            'dojo1', 'dojo2', 'dojo3', 'dojo4', 'dojo5', 'dojo6', 'dojo7', 'dojo8', 'dojo9', 'dojo10', 'dojo11',
            'dojo12', 'dojo13', 'dojo14', 'dojo15', 'dojo16', 'dojo17', 'dojo18', 'dojo19', 'dojo20',
            'dojo21', 'dojo22', 'dojo23', 'dojo24',
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
            'yui1', 'yui2', 'yui3', 'yui4', 'yui5', 'yui6', 'yui7', 'yui8',
        }
        js_file = unittest_file_path('test_js', 'test.js')
        class_extractor = ClassExtractor(file_path=js_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)
    
    def test_integration_class_set_aspx(self):
        expected_class_set = {
            'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green',
            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        }
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center',
            # Embedded <script></script>
            'dojo1', 'dojo2', 'dojo3', 'dojo4', 'dojo5', 'dojo6', 'dojo7', 'dojo8', 'dojo9', 'dojo10', 'dojo11',
            'dojo12',
        }
        jinja2_file = unittest_file_path('test_jinja', 'test.jinja2')
        class_extractor = ClassExtractor(file_path=jinja2_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_ruby_erb(self):
        expected_class_set = {
            'font-size-53', 'brown', 'text-align-right', 'medium-down',
            # Embedded <script></script>
            'yui1', 'yui2', 'yui3', 'yui4', 'yui5', 'yui6', 'yui7', 'yui8',
        }
        erb_file = unittest_file_path('test_erb', 'test.erb')
        class_extractor = ClassExtractor(file_path=erb_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)


if __name__ == '__main__':
    main()
