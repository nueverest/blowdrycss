import unittest
from os import chdir
import sys
from io import StringIO
# custom
import blowdry
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMain(unittest.TestCase):
    def test_main(self):
        substrings = ['Project Directory:', 'cssblowdry.css created', 'cssblowdry.min.css created']
        complete = '---\n'
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            chdir('..')
            blowdry.main()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output)
            self.assertTrue(output.endswith(complete), msg=output)
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    unittest.main()

