from unittest import TestCase, main
# custom
from scalingparser import ScalingParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestBreakpointParser(TestCase):
    def test_is_scaling_True(self):
        valid_css_classes = ['font-size-24-s', 'font-size-24-s-i', 'padding-10-s', 'margin-30-s-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]

        for i, css_class in enumerate(valid_css_classes):
            scaling_parser = ScalingParser(css_class=css_class, name=names[i])
            self.assertTrue(scaling_parser.is_scaling())

    def test_is_scaling_False(self):
        valid_css_classes = ['font-size-24', 'font-size-24-i', 'padding-10', 'margin-30-i', 'bold-s', 'green-s-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', 'font-weight', 'color', ]

        for i, css_class in enumerate(valid_css_classes):
            scaling_parser = ScalingParser(css_class=css_class, name=names[i])
            self.assertFalse(scaling_parser.is_scaling())

    def test_generate_scaling_css(self):
        valid_css_classes = ['font-size-24-s', 'font-size-24-s-i', 'padding-10-s', 'margin-30-s-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]
        values = ['24', '24', '10', '30', ]
        expected = ['']
        pass


if __name__ == '__main__':
    main()
