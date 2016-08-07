# python 2
from __future__ import absolute_import

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
            'className22', 'blue', 'white', 'class',
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
            ' row bgc-green padding-top-30 padding-bottom-30', 'bgc-pink', 'color-h979591',
            'row padding-top-30 padding-bottom-30 ', 'row padding-top-30 padding-bottom-30 ', 'row padding-25-820-up ',

            'row', 'font-size-12 arial h4b4f54 margin-top-33', 'font-size-42 bold h333333 margin-top-13',

            # These two were missed in the past. (URI / Inline comment match issue)
            'small-6 medium-4 large-3 xlarge-2 xxlarge-2 columns end padding-left-5-i padding-right-5-i margin-top-10',
            'bgc-h1989ce width-250 hide',

            'small-12 columns text-align-center margin-top-40',
            'inline-block bgc-h333333 width-140 height-48 white bold padding-top-16 padding-bottom-19 border-radius-5',

            # These two were missed in the past. (URI / Inline comment match issue)
            'inline-block bgc-h1989ce width-250 height-48 white bold padding-top-16 padding-bottom-19 border-radius-5 margin-left-16',
            'material-icons vertical-align-middle font-size-18-i',

            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4 jquery5', 'jquery6 jquery7', 'jquery8',
            'jquery9 jquery10', 'jquery11', 'jquery12 jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        ]
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list, msg=actual_raw_class_list)

    def test_raw_class_list_cs(self):
        expected_raw_class_list = [
            # class=*
            'font-size-14', 'large-up', 'padding-bottom-2', 'white-hover',
            'hide small-6 columns border-right-width-2',
            'material-icons vertical-align-middle padding-bottom-2',
            'incorrect-class-25',
            'large-up large-3 xlarge-2 columns',
            'material-icons vertical-align-middle padding-bottom-2',
            'squirrel', 'padding-bottom-17',
            'material-icons vertical-align-middle padding-bottom-2',
            'orange',   # In this case 'orange' appears twice as it is detected by both regexes.
            # iframe concatentation case returns empty string
            '',
            # CssClass
            'orange', ' h000 ', ' margin-top-10 margin-bottom-72 ',
            # Attributes.Add("class", ...)
            'pink', 'xsmall-only', ' height-12 ', ' width-100p inline ',
        ]
        cs_file = unittest_file_path('test_cs', 'test.aspx.cs')
        class_extractor = ClassExtractor(file_path=cs_file)
        actual_raw_class_list = class_extractor.raw_class_list
        self.assertEqual(actual_raw_class_list, expected_raw_class_list, msg=actual_raw_class_list)

    def test_raw_class_list_jinja(self):
        expected_raw_class_list = [
            'purple  padding-left-5', ' squirrel text-align-center margin-5-2-5-2-1000-up', 'large-up  border-1',
            'row text-align-center', '',
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
            'className22', 'blue', 'white', 'class',
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

    def test_class_set_html(self):
        expected_class_set = {
            'c-blue', 'text-align-center', 'padding-10', 'padding-10-s', 'margin-20', 'hide', 'display-960-up-i',
            'c-red-i-hover', 'hfff-hover-i',
            # Embedded <script></script>
            'addclass1', 'addclass2', 'addclass3', 'addclass4', 'addclass5', 'addclass6',
        }
        html_file = unittest_file_path('test_html', 'test.html')
        class_extractor = ClassExtractor(file_path=html_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_aspx(self):
        expected_class_set = {
            'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green', 'bgc-pink', 'color-h979591', 'padding-25-820-up',
            # Previously problematic section
            'font-size-12', 'arial', 'h4b4f54', 'margin-top-33', 'font-size-42', 'bold', 'h333333', 'margin-top-13',
            'small-6', 'medium-4', 'large-3', 'xlarge-2', 'xxlarge-2', 'columns', 'end', 'padding-left-5-i',
            'padding-right-5-i', 'margin-top-10', 'bgc-h1989ce', 'width-250', 'hide', 'small-12', 'columns',
            'text-align-center', 'margin-top-40', 'inline-block', 'bgc-h333333', 'width-140', 'height-48', 'white',
            'padding-top-16', 'padding-bottom-19', 'border-radius-5', 'height-48', 'white', 'bold', 'margin-left-16',
            'material-icons', 'vertical-align-middle', 'font-size-18-i',
            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        }
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_cs(self):
        expected_class_set = {
            # class=*
            'font-size-14', 'large-up', 'padding-bottom-2', 'white-hover',
            'hide', 'small-6', 'columns', 'border-right-width-2',
            'incorrect-class-25', 'squirrel',
            'material-icons', 'large-3', 'xlarge-2', 'vertical-align-middle', 'padding-bottom-17',
            # CssClass
            'orange', 'h000', 'margin-top-10', 'margin-bottom-72',
            # Attributes.Add("class", ...)
            'pink', 'xsmall-only', 'height-12', 'width-100p', 'inline',
        }
        cs_file = unittest_file_path('test_cs', 'test.aspx.cs')
        class_extractor = ClassExtractor(file_path=cs_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center', 'margin-5-2-5-2-1000-up',
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
            'className22', 'blue', 'white', 'class',
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

    def test_integration_class_set_html(self):
        expected_class_set = {
            'c-blue', 'text-align-center', 'padding-10', 'margin-20', 'hide', 'display-960-up-i',
            'padding-10-s', 'c-red-i-hover', 'hfff-hover-i',
            # Embedded <script></script>
            'addclass1', 'addclass2', 'addclass3', 'addclass4', 'addclass5', 'addclass6',
        }
        html_file = unittest_file_path('test_html', 'test.html')
        class_extractor = ClassExtractor(file_path=html_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_aspx(self):
        expected_class_set = {
            'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green', 'bgc-pink', 'color-h979591', 'padding-25-820-up',
            # Previously problematic section
            'font-size-12', 'arial', 'h4b4f54', 'margin-top-33', 'font-size-42', 'bold', 'h333333', 'margin-top-13',
            'small-6', 'medium-4', 'large-3', 'xlarge-2', 'xxlarge-2', 'columns', 'end', 'padding-left-5-i',
            'padding-right-5-i', 'margin-top-10', 'bgc-h1989ce', 'width-250', 'hide', 'small-12', 'columns',
            'text-align-center', 'margin-top-40', 'inline-block', 'bgc-h333333', 'width-140', 'height-48', 'white',
            'padding-top-16', 'padding-bottom-19', 'border-radius-5', 'height-48', 'white', 'bold', 'margin-left-16',
            'material-icons', 'vertical-align-middle', 'font-size-18-i',
            # Embedded <script></script>
            'jquery1', 'jquery2', 'jquery3', 'jquery4', 'jquery5', 'jquery6', 'jquery7', 'jquery8',
            'jquery9', 'jquery10', 'jquery11', 'jquery12', 'jquery13', 'jquery14', 'jquery15', 'jquery16',
            'jquery17',
        }
        aspx_file = unittest_file_path('test_aspx', 'test.aspx')
        class_extractor = ClassExtractor(file_path=aspx_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_cs(self):
        expected_class_set = {
            # class=*
            'font-size-14', 'large-up', 'padding-bottom-2', 'white-hover',
            'hide', 'small-6', 'columns', 'border-right-width-2',
            'incorrect-class-25', 'squirrel',
            'material-icons', 'large-3', 'xlarge-2', 'vertical-align-middle', 'padding-bottom-17',
            # CssClass
            'orange', 'h000', 'margin-top-10', 'margin-bottom-72',
            # Attributes.Add("class", ...)
            'pink', 'xsmall-only', 'height-12', 'width-100p', 'inline',
        }
        cs_file = unittest_file_path('test_cs', 'test.aspx.cs')
        class_extractor = ClassExtractor(file_path=cs_file)
        actual_class_set = class_extractor.class_set
        self.assertEqual(actual_class_set, expected_class_set)

    def test_integration_class_set_jinja(self):
        expected_class_set = {
            'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row',
            'text-align-center', 'margin-5-2-5-2-1000-up',
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
