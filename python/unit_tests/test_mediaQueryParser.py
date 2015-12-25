from unittest import TestCase, main
# custom
from mediaqueryparser import MediaQueryParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMediaQueryParser(TestCase):
    def test_set_breakpoint(self):
        pass

    def test_set_direction(self):
        pass

    def test_generate_css_with_breakpoint(self):
        pass

    def test_is_responsive_True(self):
        valid_css_classes = ['font-size-24-r', 'font-size-24-r-i', 'padding-10-r', 'margin-30-r-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]
        values = ['24', '24', '10', '30', ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            self.assertTrue(media_query_parser.is_responsive())

    def test_is_responsive_False(self):
        valid_css_classes = ['font-size-24', 'font-size-24-i', 'padding-10', 'margin-30-i', 'bold-r', 'green-r-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', 'font-weight', 'color', ]
        values = ['24', '24', '10', '30', 'bold', 'green', ]

        for i, css_class in enumerate(valid_css_classes):
            media_query_parser = MediaQueryParser(css_class=css_class, name=names[i], value=values[i])
            self.assertFalse(media_query_parser.is_responsive())

    def test_generate_responsive_css(self):
        pass


if __name__ == '__main__':
    main()
