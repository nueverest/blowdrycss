# python 2
from __future__ import absolute_import, unicode_literals

# builtin
from unittest import TestCase, main
import sys
from io import StringIO

# custom
from blowdrycss.filehandler import FileFinder, FileConverter
from blowdrycss.utilities import unittest_file_path
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileFinder(TestCase):
    def test_file_finder_wrong_path(self):
        not_a_directory = 'not/a/ valid /directory\\file.txt'
        self.assertRaises(OSError, FileFinder, not_a_directory)

    # Reference:
    # http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python#answer-4220278
    def test_print_collection1(self):
        expected_output = 'test1\ntest2'
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        collection1 = ['test1', 'test2']
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            file_finder.print_collection(collection1)
            output = out.getvalue().strip()
            self.assertEqual(output, expected_output)
        finally:
            sys.stdout = saved_stdout

    def test_print_collection2(self):
        expected_output = 'test1\ntest2'
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        collection2 = ('test1', 'test2')
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            file_finder.print_collection(collection2)
            output = out.getvalue().strip()
            self.assertEqual(output, expected_output)
        finally:
            sys.stdout = saved_stdout

    def test_set_files(self):
        expected_files = {
            unittest_file_path('test_examplesite', 'clashing_aliases.html'),
            unittest_file_path('test_examplesite', 'property_aliases.html'),
            unittest_file_path('test_examplesite', 'modify.html'),
            unittest_file_path('test_generic', 'blowdry.html'),
            unittest_file_path('test_html', 'index.html'),
            unittest_file_path('test_html', 'test.html'),
            unittest_file_path('test_html', 'media_query.html'),
        }
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        for expected_file in expected_files:
            self.assertTrue(expected_file in file_finder.files)

    def test_set_file_dict(self):
        valid_dict = {
            '.html': {
                unittest_file_path('test_examplesite', 'clashing_aliases.html'),
                unittest_file_path('test_examplesite', 'modify.html'),
                unittest_file_path('test_examplesite', 'property_aliases.html'),
                unittest_file_path('test_generic', 'blowdry.html'),
                unittest_file_path('test_html', 'index.html'),
                unittest_file_path('test_html', 'test.html'),
                unittest_file_path('test_html', 'media_query.html'),
            },
            '.aspx': {
                unittest_file_path('test_aspx', 'test.aspx'),
            },
            '.jinja2': {
                unittest_file_path('test_jinja', 'test.jinja2'),
            }
        }
        valid_keys = ['.html', '.aspx', '.jinja2']
        settings.file_types = ('*.html', '*.aspx', '*.jinja2')                              # Override file_types
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        for valid_key in valid_keys:
            self.assertTrue(valid_key in file_finder.file_dict, msg=file_finder.file_dict)
            self.assertEqual(file_finder.file_dict[valid_key], valid_dict[valid_key],
                             msg='\n' + valid_key + str(file_finder.file_dict[valid_key]) + '\n\n' + str(valid_dict[valid_key]))
        settings.file_types = ('*.html', )                                                  # Reset file_types

    def test_set_file_dict_extension_not_found(self):
        valid_dict = {'.not_found': set(), }
        valid_keys = ['.not_found']
        settings.file_types = ('*.not_found', )                                             # Override file_types
        project_directory = unittest_file_path()
        file_finder = FileFinder(project_directory=project_directory)
        for valid_key in valid_keys:
            self.assertTrue(valid_key in file_finder.file_dict, msg=file_finder.file_dict)
            self.assertEqual(file_finder.file_dict[valid_key], valid_dict[valid_key],
                             msg=file_finder.file_dict[valid_key])
        settings.file_types = ('*.html', )                                                  # Reset file_types

    def test_fileconverter_wrongpath(self):
        wrong_file_path = '/this/is/wrong/file/path'
        self.assertRaises(OSError, FileConverter, wrong_file_path)

    def test_get_file_as_string(self):
        test_file_path = unittest_file_path('test_html', 'test.html')
        expected_string = (
            '<html>	<body>        <!-- <p class="margin-left-22">Class should not be found in comments</p> -->		' +
            '<h1 class="c-blue text-align-center padding-10 display-960-up-i">Blow Dry CSS</h1>        ' +
            '<div id="div1" class="padding-10-s margin-20 c-red-i-hover">Testing<br class="hide" />1 2 3</div>	' +
            '</body></html><script>    // create element    var element = document.getElementById("div1");    ' +
            'var notimplemented = " not implemented ";    // element.classList.add() variant 1    ' +
            'element.classList.add("addclass1");    // element.classList.add() variant 2    ' +
            'element.classList.add( "addclass2" );    // element.classList.add() variant 3    ' +
            'element.classList.add(        "addclass3"    );    // element.classList.add() variant 4    ' +
            'element.classList.add(\'addclass4\');    // element.classList.add() variant 5    ' +
            'element.classList.add( \'addclass5\' );    // element.classList.add() variant 6    ' +
            'element.classList.add(        \'addclass6\'    );    // className variables not implemented    ' +
            'element.classList.add(notimplemented);</script>'
        )
        file_converter = FileConverter(file_path=test_file_path)
        self.assertEqual(file_converter.get_file_as_string(), expected_string, msg=file_converter.get_file_as_string())


if __name__ == '__main__':
    main()
