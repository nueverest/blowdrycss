# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
from cssutils.css import Property

# custom
from blowdrycss.scalingparser import ScalingParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


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
            'font-size-10', 'font-size-13-i',
        ]
        names = ['font-size', 'font-size', 'padding', 'margin', 'font-size', 'font-size', ]
        values = ['34px', '24px', '12px', '31px', '15px', '52px', '10px', '13px', ]
        priorities = ['', 'important', '', 'important', '', '', '', '', ]
        expected = [
            'font-size-34', 'font-size-24-i', 'padding-12', 'margin-31-i',
            'font-size-10', 'font-size-13-i',
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
            '@media only screen and (max-width: 64.0em) {\n' +
            '\t.font-size-24-s { font-size: 23.0105px; }\n' +
            '}\n\n' +
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
            '@media only screen and (max-width: 64.0em) {\n' +
            '\t.font-size-24-s { font-size: 1.4382em; }\n' +
            '}\n\n' +
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
            '@media only screen and (max-width: 64.0em) {\n' +
            '\t.font-size-24-s-i { font-size: 1.4382em !important; }\n' +
            '}\n\n' +
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

    def test_generate_scaling_css_invalid_property_name_is_not_scaling(self):
        css_class = 'white-space-nowrap-s'
        name = 'white-space'
        value = 'nowrap'
        priority = ''
        css_property = Property(name=name, value=value, priority=priority)
        expected = ''
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected, msg=css)

    def test_generate_scaling_css_rem_important(self):
        css_class = 'font-size-24rem-s-i'
        name = 'font-size'
        value = '24rem'
        priority = 'important'
        css_property = Property(name=name, value=value, priority=priority)
        expected = (
            '.font-size-24rem-s-i { font-size: ' + value + ' !important; }\n\n' +
            '@media only screen and (max-width: 64.0em) {\n' +
            '\t.font-size-24rem-s-i { font-size: 23.0105rem !important; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.font-size-24rem-s-i { font-size: 21.3333rem !important; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 30.0em) {\n' +
            '\t.font-size-24rem-s-i { font-size: 19.2rem !important; }\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected, msg=css)

    def test_generate_scaling_css_invalid_units(self):
        # TODO: Decide whether to create unit validator or to continue relying on cssutils for validation.
        css_class = 'font-size-24parsecs-s-i'
        name = 'font-size'
        value = '24parsecs'
        priority = 'important'
        css_property = Property(name=name, value=value, priority=priority)
        expected = (
            '.font-size-24parsecs-s-i { font-size: ' + value + ' !important; }\n\n' +
            '@media only screen and (max-width: 64.0em) {\n' +
            '\t.font-size-24parsecs-s-i { font-size: 23.0105parsecs !important; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.font-size-24parsecs-s-i { font-size: 21.3333parsecs !important; }\n' +
            '}\n\n' +
            '@media only screen and (max-width: 30.0em) {\n' +
            '\t.font-size-24parsecs-s-i { font-size: 19.2parsecs !important; }\n' +
            '}\n\n'
        )
        scaling_parser = ScalingParser(css_class=css_class, css_property=css_property)
        css = scaling_parser.build_media_query()
        self.assertEqual(css, expected, msg=css)

if __name__ == '__main__':
    main()
