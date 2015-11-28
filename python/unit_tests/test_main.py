from unittest import TestCase, main
from os import chdir
import sys
from io import StringIO
# custom
import blowdry
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMain(TestCase):
    def test_main(self):
        substrings = ['Project Directory:', 'File Types:', 'Project Files Found:', 'CSSBuilder Running:']
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            chdir('..')
            blowdry.main()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()

