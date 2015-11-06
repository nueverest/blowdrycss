from unittest import TestCase
from os import chdir, path, getcwd
from filefinder import FileFinder
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestFileFinder(TestCase):
    def test_print_collection1(self):
        import sys
        from io import StringIO

        expected_output = 'test1\ntest2'
        file_finder = FileFinder()
        collection1 = ['test1','test2']
        collection2 = ('test1','test2')
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
        file_finder = FileFinder()
        collection2 = ('test1','test2')
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
        expected_files = ['C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\ExampleSite\\index.html']

        chdir('..\..')                                              # Navigate up two directories.
        project_directory = path.join(getcwd() + '\ExampleSite')    # Change to whatever you want.
        file_types = ('*.html', '*.aspx', '*.master', '*.ascx')
        file_finder = FileFinder(project_directory=project_directory, file_types=file_types)
        self.assertEquals(file_finder.files, expected_files)