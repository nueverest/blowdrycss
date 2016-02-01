from unittest import TestCase, main
from cssutils.css import Property
# custom
from breakpointparser import BreakpointParser
from settings.blowdrycss_settings import px_to_em

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestBreakpointParser(TestCase):
    def test_set_breakpoint_key(self):
        valid_css_classes = [
            'inline-small-up', 'inline-giant-down-i', 'green-xxsmall-only', 'padding-10-large-up', 'xsmall-down',
            'medium-only', 'giant-up', 'giant-only-i', 'display-large-down',
        ]
        names = ['display', 'display', 'color', 'padding', 'display', 'display', 'display', 'display', 'display', ]
        values = ['inherit', 'inherit', 'green', '10', 'inherit', 'inherit', 'inherit', 'inherit', 'inherit', ]
        priorities = ['', 'important', '', '', '', '', '', 'important', '']
        expected = ['-small', '-giant', '-xxsmall', '-large', '-xsmall', '-medium', '-giant', '-giant', '-large', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            breakpoint_parser.set_breakpoint_key()
            self.assertEqual(breakpoint_parser.breakpoint_key, expected[i])

    def test_set_breakpoint_key_ValueError(self):
        valid_css_classes = ['inline-small', 'inline-down', 'custom-class', '-xsmall-', '-xxlarge-up']
        names = ['display', 'display', 'padding', 'invalid', 'invalid', ]
        values = ['inherit', 'inherit', '10', 'invalid', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertFalse(breakpoint_parser.is_breakpoint)

    def test_set_limit_key(self):
        valid_css_classes = ['inline-small-up', 'inline-giant-down-i', 'green-xxsmall-only', 'padding-10-large-up', ]
        names = ['display', 'display', 'color', 'padding', ]
        values = ['inline', 'inline', 'green', '10', ]
        priorities = ['', 'important', '', '', ]
        expected = ['-up', '-down', '-only', '-up', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            breakpoint_parser.set_limit_key()
            self.assertEqual(breakpoint_parser.limit_key, expected[i])

    def test_set_limit_key_ValueError(self):
        valid_css_classes = ['inline-small-', 'inline-downward', '-only-', 'custom-class', '-up-', ]
        names = ['display', 'display', 'color', 'padding', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertFalse(breakpoint_parser.is_breakpoint)

    def test_strip_breakpoint_limit(self):
        valid_css_classes = [
            'inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up',
            'xlarge-only', 'large-down', 'xsmall-up',
        ]
        names = ['display', 'display', 'color', 'padding', 'display', 'display', 'display', ]
        values = ['inline', 'inline', 'green', '10', 'none', 'none', 'none', ]
        expected = ['inline', 'inline', 'green', 'padding-10', '', '', '', ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            clean_css_class = breakpoint_parser.strip_breakpoint_limit()
            self.assertEqual(clean_css_class, expected[i])

    def test_css_for_only_display(self):
        css_class = 'display-large-only'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 45.0625em) {\n' +
            '\t.display-large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n' +
            '@media only screen and (min-width: 64.0em) {\n' +
            '\t.display-large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected)

    def test_css_for_only_display_shorthand(self):
        css_class = 'large-only'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 45.0625em) {\n' +
            '\t.large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n' +
            '@media only screen and (min-width: 64.0em) {\n' +
            '\t.large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected)

    def test_css_for_only_display_shorthand_important(self):
        css_class = 'large-only-i'
        name = 'display'
        value = 'none'
        priority = 'important'
        expected = (
            '@media only screen and (max-width: 45.0625em) {\n' +
            '\t.large-only-i {\n' +
            '\t\tdisplay: none !important;\n' +
            '\t}\n' +
            '}\n\n' +
            '@media only screen and (min-width: 64.0em) {\n' +
            '\t.large-only-i {\n' +
            '\t\tdisplay: none !important;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority=priority)
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected, msg=css)

    def test_css_for_only_general_usage(self):
        css_class = 'padding-100-large-only'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (min-width: 45.0625em) and (max-width: 64.0em) {\n' +
            '\t.padding-100-large-only {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected)

    def test_css_for_only_general_usage_important(self):
        css_class = 'padding-100-large-only-i'
        name = 'padding'
        value = px_to_em('100')
        priority = 'important'
        expected = (
            '@media only screen and (min-width: 45.0625em) and (max-width: 64.0em) {\n' +
            '\t.padding-100-large-only-i {\n' +
            '\t\tpadding: 6.25em !important;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority=priority)
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected)

    def test_css_for_only_wrong_limit_key(self):
        css_class = 'padding-100-large-only'
        name = 'padding'
        value = px_to_em('100')
        expected = ''
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        breakpoint_parser.limit_key = '-up'     # Change to WRONG LIMIT KEY
        css = breakpoint_parser.css_for_only()
        self.assertEqual(css, expected)

    def test_css_for_down_display(self):
        css_class = 'display-medium-down'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (min-width: 45.0em) {\n' +
            '\t.display-medium-down {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_down()
        self.assertEqual(css, expected)

    def test_css_for_down_display_shorthand(self):
        css_class = 'medium-down'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (min-width: 45.0em) {\n' +
            '\t.medium-down {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_down()
        self.assertEqual(css, expected)

    def test_css_for_down_general_usage(self):
        css_class = 'padding-100-medium-down'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.padding-100-medium-down {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_down()
        self.assertEqual(css, expected)

    def test_css_for_down_wrong_limit_key(self):
        css_class = 'padding-100-medium-down'
        name = 'padding'
        value = px_to_em('100')
        expected = ''
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        breakpoint_parser.limit_key = '-only'   # Change to WRONG LIMIT KEY.
        css = breakpoint_parser.css_for_down()
        self.assertEqual(css, expected)

    def test_css_for_up_display(self):
        css_class = 'display-small-up'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 15.0625em) {\n' +
            '\t.display-small-up {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_up()
        self.assertEqual(css, expected)

    def test_css_for_up_display_shorthand(self):
        css_class = 'small-up'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 15.0625em) {\n' +
            '\t.small-up {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_up()
        self.assertEqual(css, expected)

    def test_css_for_up_general_usage(self):
        css_class = 'padding-100-small-up'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (min-width: 15.0625em) {\n' +
            '\t.padding-100-small-up {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.css_for_up()
        self.assertEqual(css, expected)

    def test_css_for_up_wrong_limit_key(self):
        css_class = 'padding-100-small-up'
        name = 'padding'
        value = px_to_em('100')
        expected = ''
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        breakpoint_parser.limit_key = '-only'   # Change to WRONG LIMIT KEY
        css = breakpoint_parser.css_for_up()
        self.assertEqual(css, expected)

    # build_media_query
    def test_build_media_query_only_display(self):
        css_class = 'display-large-only'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 45.0625em) {\n' +
            '\t.display-large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n' +
            '@media only screen and (min-width: 64.0em) {\n' +
            '\t.display-large-only {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_only_general_usage(self):
        css_class = 'padding-100-large-only'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (min-width: 45.0625em) and (max-width: 64.0em) {\n' +
            '\t.padding-100-large-only {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_down_display(self):
        css_class = 'display-medium-down'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (min-width: 45.0em) {\n' +
            '\t.display-medium-down {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_down_general_usage(self):
        css_class = 'padding-100-medium-down'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.padding-100-medium-down {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_up_display(self):
        css_class = 'display-small-up'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 15.0625em) {\n' +
            '\t.display-small-up {\n' +
            '\t\tdisplay: none;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_up_general_usage(self):
        css_class = 'padding-100-small-up'
        name = 'padding'
        value = px_to_em('100')
        expected = (
            '@media only screen and (min-width: 15.0625em) {\n' +
            '\t.padding-100-small-up {\n' +
            '\t\tpadding: 6.25em;\n' +
            '\t}\n' +
            '}\n\n'
        )
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)

    def test_build_media_query_invalid_limit_key(self):
        css_class = 'padding-100-small-up'
        name = 'padding'
        value = px_to_em('100')
        expected = ''
        css_property = Property(name=name, value=value, priority='')
        breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
        breakpoint_parser.limit_key = 'invalid_key'
        css = breakpoint_parser.build_media_query()
        self.assertEqual(css, expected)


if __name__ == '__main__':
    main()
