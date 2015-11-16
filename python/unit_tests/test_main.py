from unittest import TestCase
from os import chdir, getcwd
import sys
from io import StringIO
# Custom
from blowdry import main
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMain(TestCase):
    def test_main(self):
        substrings = ['clean ran', 'cssblowdry.css created', 'cssblowdry.min.css created']
        complete = '--- Complete ---\n'
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            # Change to match your file system.
            chdir('C:\\Users\\Chad Nu\\PycharmProjects\\BlowDryCSS\\python\\')
            main()
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output)
            self.assertTrue(output.endswith(complete), msg=output)
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    main()

