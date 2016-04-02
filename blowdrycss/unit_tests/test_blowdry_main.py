# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
import sys
from io import StringIO

# custom
import blowdrycss.blowdry as blowdry

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestMain(TestCase):
    def test_main(self):
        substrings = [
            '~~~ blowdrycss started ~~~', 'Project Files Found:',
            'CSSBuilder Running...', '.css',
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            blowdry.main()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output + '\tsubstring: ' + substring)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()

