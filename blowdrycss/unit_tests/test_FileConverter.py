# builtin
from unittest import TestCase, main
from os import path, getcwd
# custom
from blowdrycss.filehandler import FileConverter

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileConverter(TestCase):
    def test_file_converter_wrong_path(self):
        wrong_file_path = path.join('C:', 'this', 'is', 'wrong', 'file', 'path')
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

