# python 2
from __future__ import absolute_import, unicode_literals

# builtin
from unittest import TestCase, main
from shutil import copyfile
from time import sleep
import os

# custom
from blowdrycss.filehandler import FileFinder, FileConverter
from blowdrycss.utilities import unittest_file_path, delete_file_paths, make_directory
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileFinder(TestCase):
    def test_file_finder_wrong_setting_project_directory(self):
        project_directory = settings.project_directory
        settings.project_directory = 'not/a/ valid /directory\\file.txt'
        recent = False
        self.assertRaises(OSError, FileFinder, recent)
        settings.project_directory = project_directory

    # Reference:
    # http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python#answer-4220278
    # def test_print_collection1(self):
    #     expected_output = 'test1\ntest2'
    #     project_directory = unittest_file_path()
    #     file_finder = FileFinder(project_directory=project_directory, recent=False)
    #     collection1 = ['test1', 'test2']
    #     saved_stdout = sys.stdout
    #     try:
    #         out = StringIO()
    #         sys.stdout = out
    #         file_finder.print_collection(collection1)
    #         output = out.getvalue().strip()
    #         self.assertEqual(output, expected_output)
    #     finally:
    #         sys.stdout = saved_stdout
    #
    # def test_print_collection2(self):
    #     expected_output = 'test1\ntest2'
    #     project_directory = unittest_file_path()
    #     file_finder = FileFinder(project_directory=project_directory, recent=False)
    #     collection2 = ('test1', 'test2')
    #     saved_stdout = sys.stdout
    #     try:
    #         out = StringIO()
    #         sys.stdout = out
    #         file_finder.print_collection(collection2)
    #         output = out.getvalue().strip()
    #         self.assertEqual(output, expected_output)
    #     finally:
    #         sys.stdout = saved_stdout

    def test_set_files(self):
        expected_files = {
            # unittest_file_path('test_examplesite', 'clashing_aliases.html'),
            # unittest_file_path('test_examplesite', 'property_aliases.html'),
            # unittest_file_path('test_examplesite', 'modify.html'),
            unittest_file_path('test_generic', 'blowdry.html'),
            unittest_file_path('test_html', 'index.html'),
            unittest_file_path('test_html', 'test.html'),
            unittest_file_path('test_html', 'media_query.html'),
        }
        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()
        file_finder = FileFinder(recent=False)
        for expected_file in expected_files:
            self.assertTrue(expected_file in file_finder.files)
        settings.project_directory = project_directory                                          # Reset

    def test_set_file_dict(self):
        delete_these = (
            unittest_file_path('test_examplesite', 'clashing_aliases.html'),
            unittest_file_path('test_examplesite', 'modify.html'),
            unittest_file_path('test_examplesite', 'property_aliases.html'),
        )
        delete_file_paths(file_paths=delete_these)

        valid_dict = {
            '.html': {
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
        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()
        file_finder = FileFinder(recent=False)
        for valid_key in valid_keys:
            self.assertTrue(valid_key in file_finder.file_dict, msg=file_finder.file_dict)
            self.assertEqual(
                file_finder.file_dict[valid_key],
                valid_dict[valid_key],
                msg='\n' + valid_key + str(file_finder.file_dict[valid_key]) + '\n\n' + str(valid_dict[valid_key])
            )
        settings.file_types = ('*.html', )                                                  # Reset file_types
        settings.project_directory = project_directory

    def test_set_file_dict_extension_not_found(self):
        valid_dict = {'.not_found': set(), }
        valid_keys = ['.not_found']
        settings.file_types = ('*.not_found', )                                             # Override file_types
        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()
        file_finder = FileFinder(recent=False)
        for valid_key in valid_keys:
            self.assertTrue(valid_key in file_finder.file_dict, msg=file_finder.file_dict)
            self.assertEqual(file_finder.file_dict[valid_key], valid_dict[valid_key],
                             msg=file_finder.file_dict[valid_key])
        settings.file_types = ('*.html', )                                                  # Reset file_types
        settings.project_directory = project_directory

    def test_set_recent_file_dict(self):
        css_directory = settings.css_directory                                              # Save original setting
        settings.css_directory = unittest_file_path(folder='test_recent')                   # Change Setting

        make_directory(settings.css_directory)                                              # Create dir for Travis CI
        self.assertTrue(os.path.isdir(settings.css_directory))

        css_file = unittest_file_path(settings.css_directory, 'blowdry.css')
        with open(css_file, 'w') as generic_file:
            generic_file.write('.bold {font-weight: bold}')

        temp_file = unittest_file_path('test_recent', 'new.html')                           # Create a temporary file
        with open(temp_file, 'w') as generic_file:
            generic_file.write('<html></html>')

        valid_dict = {
            '.html': {
                unittest_file_path('test_recent', 'new.html'),
            },
            '.aspx': set(),
            '.jinja2': set(),
        }
        valid_keys = ['.html', '.aspx', '.jinja2']
        settings.file_types = ('*.html', '*.aspx', '*.jinja2')                              # Override file_types
        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()
        file_finder = FileFinder(recent=True)
        for valid_key in valid_keys:
            self.assertTrue(valid_key in file_finder.file_dict, msg=file_finder.file_dict)
            self.assertEqual(
                file_finder.file_dict[valid_key],
                valid_dict[valid_key],
                msg='\n' + valid_key + str(file_finder.file_dict[valid_key]) + '\n\n' + str(valid_dict[valid_key])
            )

        delete_file_paths(file_paths=(temp_file, css_file, ))                               # Delete test files
        settings.css_directory = css_directory                                              # Reset settings
        settings.file_types = ('*.html', )
        settings.project_directory = project_directory

    def test_fileconverter_wrongpath(self):
        wrong_file_path = '/this/is/wrong/file/path'
        self.assertRaises(OSError, FileConverter, wrong_file_path)

    def test_get_file_as_string(self):
        test_file_path = unittest_file_path('test_html', 'test.html')
        expected_string = (
            '<html>	<body>        ' +
            '<!--            <p class="margin-left-22">                Class should not be found in comments' +
            '            </p>        -->		' +
            '<h1 class="c-blue text-align-center padding-10 display-960-up-i">Blow Dry CSS</h1>        ' +
            '<div id="div1" class="padding-10-s margin-20 c-red-i-hover">Testing<br class="hide" />1 2 3</div>' +
            '        <p class="hfff-hover-i">Stars</p>	' +
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
