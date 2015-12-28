from unittest import TestCase, main
# custom
import settings
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

    def test_generate_scaling_css_pixels(self):
        css_class = 'font-size-24-s'
        name = 'font-size'
        value = '24px'
        expected = (
            '.font-size-24-s {\n' +
            '\tfont-size: ' + value + ';\n\n' +
            '\t@media only screen and (max-width: 45.0em) {\n' +
            '\t\tfont-size: 21.3333px;\n' +
            '}\n\n' +
            '\t@media only screen and (max-width: 30.0em) {\n' +
            '\t\tfont-size: 19.2px;\n' +
            '\t}\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, name=name)
        css = scaling_parser.generate_scaling_css(value=value)
        self.assertEqual(css, expected)

    def test_generate_scaling_css_em(self):
        css_class = 'font-size-24-s'
        name = 'font-size'
        value = '1.5em'
        expected = (
            '.font-size-24-s {\n' +
            '\tfont-size: ' + value + ';\n\n' +
            '\t@media only screen and (max-width: 45.0em) {\n' +
            '\t\tfont-size: 1.3333em;\n' +
            '}\n\n' +
            '\t@media only screen and (max-width: 30.0em) {\n' +
            '\t\tfont-size: 1.2em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, name=name)
        css = scaling_parser.generate_scaling_css(value=value)
        self.assertEqual(css, expected)

if __name__ == '__main__':
    main()
