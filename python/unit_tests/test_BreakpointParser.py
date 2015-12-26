from unittest import TestCase, main
# custom
from breakpointparser import BreakpointParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestBreakpointParser(TestCase):
    def test_set_breakpoint(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        expected = [(241, 480), (1921, 2560), (0, 120), (721, 1024), ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            breakpoint_parser.set_breakpoint()
            self.assertEqual(breakpoint_parser.breakpoint_values, expected[i])

    def test_set_breakpoint_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-down', 'xgiant-only', 'custom-class', '-xsmall-', '-xxlarge-up']
        names = ['display', 'display', 'color', 'padding', 'invalid', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            self.assertRaises(ValueError, breakpoint_parser.set_breakpoint)

    def test_set_limit(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        expected = ['-up', '-down', '-only', '-up', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            breakpoint_parser.set_limit()
            self.assertEqual(breakpoint_parser.limit, expected[i])

    def test_set_limit_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-downward', '-only-', 'custom-class', '-up-', ]
        names = ['display', 'display', 'color', 'padding', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            breakpoint_parser = BreakpointParser(css_class=css_class, name=names[i], value=values[i])
            self.assertRaises(ValueError, breakpoint_parser.set_limit)

    def test_generate_css_with_breakpoint(self):
        pass


if __name__ == '__main__':
    main()
