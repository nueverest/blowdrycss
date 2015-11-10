import unittest
from unittest import TestCase
from os import chdir, path, getcwd
from filehandler import FileFinder, FileConverter
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestFileFinder(TestCase):
    def test_file_finder_wrong_path(self):
        not_a_directory = 'C:\\this\\is\\not\\a\\directory.txt'
        self.assertRaises(NotADirectoryError, FileFinder, not_a_directory)

    # Reference:
    # http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python#answer-4220278
    def test_print_collection1(self):
        import sys
        from io import StringIO

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
        import sys
        from io import StringIO

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
        expected_files = [
            'C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\ExampleSite\\index.html',
            'C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\ExampleSite\\test.html'
        ]

        chdir('..\..')                                              # Navigate up two directories.
        project_directory = path.join(getcwd() + '\ExampleSite')    # Change to whatever you want.
        file_types = ('*.html', '*.aspx', '*.master', '*.ascx')
        file_finder = FileFinder(project_directory=project_directory, file_types=file_types)
        self.assertEquals(file_finder.files, expected_files)

    def test_fileconverter_wrongpath(self):
        wrong_file_path = 'C:\\this\\is\\wrong\\file\\path'
        self.assertRaises(FileNotFoundError, FileConverter, wrong_file_path)

    def test_get_file_as_string(self):
        test_file_path = 'C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\ExampleSite\\test.html'
        expected_string = '<html>	<body>		<h1 class="c-blue text-align-center padding-10">Blow Dry CSS</h1>' \
                          '        <div class="padding-10 margin-20">Testing<br class="hide" />1 2 3</div>	' \
                          '</body></html>'
        file_converter = FileConverter(file_path=test_file_path)
        self.assertEquals(file_converter.get_file_as_string(), expected_string)
