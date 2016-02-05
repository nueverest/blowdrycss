from unittest import TestCase, main
import sys
from io import StringIO
# custom
try:
    import blowdry
except ImportError:
    import blowdrycss.blowdry as blowdry

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


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

            blowdry.main()

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()

