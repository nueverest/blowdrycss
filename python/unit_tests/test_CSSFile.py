from unittest import TestCase, main
from os import path, getcwd, remove
# Custom
from filehandler import CSSFile
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestCSSFile(TestCase):
    def test_not_a_directory(self):
        not_a_directory = '/a/ invalid /directory/file.txt'    # Spaces added around 'invalid' to make it invalid.
        file_name = 'some_file'
        self.assertRaises(OSError, CSSFile, not_a_directory, file_name)

    def test_file_path(self):
        extensions = ['.css', '.min.css', '.txt', '.mp3', '.anything']
        css_file = CSSFile()

        for extension in extensions:
            expected_file_path = path.join(getcwd(), 'blowdry' + extension)
            file_path = css_file.file_path(extension=extension)
            self.assertEqual(file_path, expected_file_path)

    def test_file_path_invalid(self):
        extensions = ['.c$@$0f00ss', '.min.!@#css', '.tx^*()&)/\t', '.a@\nything']
        css_file = CSSFile()

        for extension in extensions:
            self.assertRaises(ValueError, css_file.file_path, extension)

    def test_write_created(self):
        css_directory = path.join(getcwd(), 'test_css')
        file_name = 'blowdry'
        css_file = CSSFile(file_directory=css_directory, file_name=file_name)
        file_path = path.join(css_directory, css_file.file_name + '.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_file.write()
        self.assertTrue(path.isfile(file_path))

    def test_write_verify_css_text(self):
        css_directory = path.join(getcwd(), 'test_css')
        file_name = 'blowdry'
        css_file = CSSFile(file_directory=css_directory, file_name=file_name)
        file_path = path.join(css_directory, css_file.file_name + '.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_text = b'.bold {\n    font-weight: bold\n    }\n.margin-top-50px {\n    margin-top: 50px\n    }\n' \
                   b'.c-blue {\n    color: blue\n    }\n.height-50px {\n    height: 50px\n    }\n' \
                   b'.bgc-h000 {\n    background-color: #000\n    }\n.color-hfff {\n    color: #fff\n    }\n' \
                   b'.valign-middle {\n    vertical-align: middle\n    }\n.height-150px {\n    height: 150px\n    }\n' \
                   b'.text-align-center {\n    text-align: center\n    }'
        expected_string = css_text.decode('utf-8')
        css_file.write(css_text=css_text)
        with open(file_path, 'r') as css_file:
            file_string = css_file.read()
        self.assertEqual(file_string, expected_string)

    def test_minify_created(self):
        css_directory = path.join(getcwd(), 'test_css')
        file_name = 'blowdry'
        css_file = CSSFile(file_directory=css_directory, file_name=file_name)
        file_path = path.join(css_directory, css_file.file_name + '.min.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_file.minify()
        self.assertTrue(path.isfile(file_path))

    def test_minify_verify_css_text(self):
        css_directory = path.join(getcwd(), 'test_css')
        file_name = 'blowdry'
        css_file = CSSFile(file_directory=css_directory, file_name=file_name)
        file_path = path.join(css_directory, css_file.file_name + '.min.css')

        if path.isfile(file_path):      # Ensure that file is deleted before testing.
            remove(file_path)

        css_text = b'.bold {\n    font-weight: bold\n    }\n.margin-top-50px {\n    margin-top: 50px\n    }\n' \
                   b'.c-blue {\n    color: blue\n    }\n.height-50px {\n    height: 50px\n    }\n' \
                   b'.bgc-h000 {\n    background-color: #000\n    }\n.color-hfff {\n    color: #fff\n    }\n' \
                   b'.valign-middle {\n    vertical-align: middle\n    }\n.height-150px {\n    height: 150px\n    }\n' \
                   b'.text-align-center {\n    text-align: center\n    }'
        expected_string = '.bold{font-weight:bold}.margin-top-50px{margin-top:50px}.c-blue{color:blue}' \
                          '.height-50px{height:50px}.bgc-h000{background-color:#000}.color-hfff{color:#fff}' \
                          '.valign-middle{vertical-align:middle}.height-150px{height:150px}' \
                          '.text-align-center{text-align:center}'
        css_file.minify(css_text=css_text)
        with open(file_path, 'r') as css_file:
            file_string = css_file.read()
        self.assertEqual(file_string, expected_string, msg=file_string)


if __name__ == '__main__':
    main()
