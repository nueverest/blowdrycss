from unittest import TestCase, main
from cssutils.css import Property
# custom
from scalingparser import ScalingParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestBreakpointParser(TestCase):
    def test_is_scaling_True(self):
        valid_css_classes = ['font-size-24-s', 'font-size-24-s-i', 'padding-10-s', 'margin-30-s-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]
        values = ['24px', '24px', '10px', '30px']
        priorities = ['', 'important', '', 'important', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
            self.assertTrue(scaling_parser.is_scaling)

    def test_is_scaling_False(self):
        valid_css_classes = ['font-size-24', 'font-size-24-i', 'padding-10', 'margin-30-i', 'bold-s', 'green-s-i', ]
        names = ['font-size', 'font-size', 'padding', 'margin', 'font-weight', 'color', ]
        values = ['24px', '24px', '10px', '30px', 'bold', 'green', ]
        priorities = ['', 'important', '', 'important', '', 'important', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
            self.assertFalse(scaling_parser.is_scaling)

    def test_strip_scaling_flag(self):
        valid_css_classes = [
            'font-size-34-s', 'font-size-24-s-i', 'padding-12-s', 'margin-31-s-i',
        ]
        names = ['font-size', 'font-size', 'padding', 'margin', ]
        values = ['34px', '24px', '12px', '31px', '15px', '52px', ]
        priorities = ['', 'important', '', 'important', '', '', ]
        expected = [
            'font-size-34', 'font-size-24-i', 'padding-12', 'margin-31-i', 
        ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
            clean_css_class = scaling_parser.strip_scaling_flag()
            self.assertEqual(clean_css_class, expected[i])

    def test_generate_scaling_css_pixels(self):
        css_class = 'font-size-24-s'
        name = 'font-size'
        value = '24px'
        priority = ''
        css_property = Property(name=name, value=value, priority=priority)
        expected = (
            '.font-size-24-s { font-size: ' + value + '; }\n\n' +
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.font-size-24-s { font-size: 21.3333px; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 30.0em) {\n' +
            '\t.font-size-24-s { font-size: 19.2px; }\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_generate_scaling_css_em(self):
        css_class = 'font-size-24-s'
        name = 'font-size'
        value = '1.5em'
        priority = ''
        css_property = Property(name=name, value=value, priority=priority)
        expected = (
            '.font-size-24-s { font-size: ' + value + '; }\n\n' +
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.font-size-24-s { font-size: 1.3333em; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 30.0em) {\n' +
            '\t.font-size-24-s { font-size: 1.2em; }\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected, msg=css)

    def test_generate_scaling_css_em_important(self):
        css_class = 'font-size-24-s-i'
        name = 'font-size'
        value = '1.5em'
        priority = 'important'
        css_property = Property(name=name, value=value, priority=priority)
        expected = (
            '.font-size-24-s-i { font-size: ' + value + ' !important; }\n\n' +
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.font-size-24-s-i { font-size: 1.3333em !important; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 30.0em) {\n' +
            '\t.font-size-24-s-i { font-size: 1.2em !important; }\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected, msg=css)

if __name__ == '__main__':
    main()
