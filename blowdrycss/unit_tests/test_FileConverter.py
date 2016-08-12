# python 2
from __future__ import absolute_import

# builtin
from unittest import TestCase, main
from os import path

# custom
from blowdrycss.filehandler import FileConverter
from blowdrycss.utilities import unittest_file_path

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestFileConverter(TestCase):
    def test_file_converter_wrong_path(self):
        wrong_file_path = path.join('C:', 'this', 'is', 'wrong', 'file', 'path')
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
        self.assertEqual(
                file_converter.get_file_as_string(),
                expected_string,
                msg='\n' + file_converter.get_file_as_string() + '\n' + expected_string
        )


if __name__ == '__main__':
    main()

