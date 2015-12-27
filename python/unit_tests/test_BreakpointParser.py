from unittest import TestCase, main
# custom
from breakpointparser import BreakpointParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestBreakpointParser(TestCase):
    def test_set_breakpoint_key(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        expected = ['-small', '-giant', '-xxsmall', '-large']

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            breakpoint_parser.set_breakpoint_key()
            self.assertEqual(breakpoint_parser.breakpoint_key, expected[i])

    def test_set_breakpoint_key_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-down', 'xgiant-only', 'custom-class', '-xsmall-', '-xxlarge-up']
        names = ['display', 'display', 'color', 'padding', 'invalid', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            self.assertRaises(ValueError, breakpoint_parser.set_breakpoint_key)

    def test_set_limit_key(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        expected = ['-up', '-down', '-only', '-up', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            breakpoint_parser.set_limit_key()
            self.assertEqual(breakpoint_parser.limit_key, expected[i])

    def test_set_limit_key_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-downward', '-only-', 'custom-class', '-up-', ]
        names = ['display', 'display', 'color', 'padding', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            self.assertRaises(ValueError, breakpoint_parser.set_limit_key)

    def test_build_media_query(self):
        pass


if __name__ == '__main__':
    main()
