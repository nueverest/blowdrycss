# builtin
from unittest import TestCase, main
from os import path, getcwd
import sys
from io import StringIO
# custom
from blowdrycss.filehandler import FileFinder, FileConverter

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
        file_finder = FileFinder(project_directory=getcwd())
        collection1 = ['test1', 'test2']
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            file_finder.print_collection(collection1)
            output = out.getvalue().strip()
            self.assertEquals(output, expected_output)
        finally:
            sys.stdout = saved_stdout

    def test_print_collection2(self):
        expected_output = 'test1\ntest2'
        file_finder = FileFinder(project_directory=getcwd())
        collection2 = ('test1', 'test2')
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            file_finder.print_collection(collection2)
            output = out.getvalue().strip()
            self.assertEquals(output, expected_output)
        finally:
            sys.stdout = saved_stdout

    def test_set_files(self):
        cwd = getcwd()

        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            expected_files = {
                path.join(cwd, 'test_examplesite', 'clashing_aliases.html'),
                path.join(cwd, 'test_examplesite', 'property_aliases.html'),
                path.join(cwd, 'test_generic', 'blowdry.html'),
                path.join(cwd, 'test_html', 'index.html'),
                path.join(cwd, 'test_html', 'test.html'),
                path.join(cwd, 'test_html', 'media_query.html'),
            }
        else:                                                       # Run unittest cmd from the root directory.
            expected_files = {
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite', 'clashing_aliases.html'),
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite', 'property_aliases.html'),
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_generic', 'blowdry.html'),
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_html', 'index.html'),
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_html', 'test.html'),
                path.join(cwd, 'blowdrycss', 'unit_tests', 'test_html', 'media_query.html'),
            }

        project_directory = cwd
        file_types = ('*.html', )
        file_finder = FileFinder(project_directory=project_directory)
        for expected_file in expected_files:
            self.assertTrue(expected_file in file_finder.files)

    def test_fileconverter_wrongpath(self):
        wrong_file_path = '/this/is/wrong/file/path'
        self.assertRaises(OSError, FileConverter, wrong_file_path)

    def test_get_file_as_string(self):
        cwd = getcwd()
        if cwd.endswith('unit_tests'):                                  # Allows running of pycharm unittest.
            test_file_path = path.join(cwd, 'test_html', 'test.html')
        else:                                                           # Run unittest cmd from the root directory.
            test_file_path = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_html', 'test.html')
        expected_string = '<html>	<body>		<h1 class="c-blue text-align-center padding-10">Blow Dry CSS</h1>' \
                          '        <div class="padding-10 margin-20">Testing<br class="hide" />1 2 3</div>	' \
                          '</body></html>'
        file_converter = FileConverter(file_path=test_file_path)
        self.assertEquals(file_converter.get_file_as_string(), expected_string)


if __name__ == '__main__':
    main()
