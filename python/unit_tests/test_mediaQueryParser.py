from unittest import TestCase, main
# custom
from mediaqueryparser import MediaQueryParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMediaQueryParser(TestCase):
    def test_set_breakpoint(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        expected = [(241, 480), (1921, 2560), (0, 120), (721, 1024), ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            media_query_parser.set_breakpoint()
            self.assertEqual(media_query_parser.breakpoint, expected[i])

    def test_set_breakpoint_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-down', 'xgiant-only', 'custom-class', '-xsmall-', '-xxlarge-up']
        names = ['display', 'display', 'color', 'padding', 'invalid', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            self.assertRaises(ValueError, media_query_parser.set_breakpoint)

    def test_set_limit(self):
        pass

    def test_generate_css_with_breakpoint(self):
        pass

    def test_is_responsive_True(self):
        valid_css_classes = ['font-size-24-r', 'font-size-24-r-i', 'padding-10-r', 'margin-30-r-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]
        values = ['24', '24', '10', '30', ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            self.assertTrue(media_query_parser.is_scaling())

    def test_is_responsive_False(self):
        valid_css_classes = ['font-size-24', 'font-size-24-i', 'padding-10', 'margin-30-i', 'bold-r', 'green-r-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', 'font-weight', 'color', ]
        values = ['24', '24', '10', '30', 'bold', 'green', ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            self.assertFalse(media_query_parser.is_scaling())

    def test_generate_responsive_css(self):
        pass


if __name__ == '__main__':
    main()
