from unittest import TestCase, main
from filehandler import FileConverter
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestFileConverter(TestCase):
    def test_file_converter_wrong_path(self):
        wrong_file_path = 'C:\\this\\is\\wrong\\file\\path'
        self.assertRaises(FileNotFoundError, FileConverter, wrong_file_path)

    def test_get_file_as_string(self):
        test_file_path = 'C:\\Users\\Chad Nu\\PycharmProjects\\blowdrycss\\ExampleSite\\test.html'
        expected_string = '<html>	<body>		<h1 class="c-blue text-align-center padding-10">Blow Dry CSS</h1>' \
                          '        <div class="padding-10 margin-20">Testing<br class="hide" />1 2 3</div>	' \
                          '</body></html>'
        file_converter = FileConverter(file_path=test_file_path)
        self.assertEquals(file_converter.get_file_as_string(), expected_string)


if __name__ == '__main__':
    main()

