from unittest import TestCase, main
from os import getcwd, chdir
import sys
from io import StringIO
# custom
import blowdrycss
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMain(TestCase):
    def test_main(self):
        substrings = [
            'Project Directory:', 'File Types:', 'Project Files Found:', 'CSSBuilder Running...',
            '.css created.',
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            # original_directory = getcwd()
            # chdir('..')                                                 # Navigate up one directory relative to this script.
            # cur_dir = getcwd()
            blowdrycss.main()
            # chdir(original_directory)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()

