# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main

# plugins
from cssutils.css import Property

# custom
from blowdrycss.breakpointparser import BreakpointParser
from blowdrycss_settings import px_to_em

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
        invalid_css_classes = ['inline-small', 'inline-down', 'custom-class', '-xsmall-', '-xxlarge-up']
        names = ['display', 'display', 'padding', 'invalid', 'invalid', ]
        values = ['inherit', 'inherit', '10', 'invalid', 'invalid', ]

        for i, css_class in enumerate(invalid_css_classes):
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
        invalid_css_classes = ['inline-small-', 'inline-downward', '-only-', 'custom-class', '-up-', ]
        names = ['display', 'display', 'color', 'padding', 'invalid', ]
        values = ['inline', 'inline', 'green', '10', 'invalid', ]

        for i, css_class in enumerate(invalid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertFalse(breakpoint_parser.is_breakpoint)

    def test_set_custom_breakpoint_key_Valid(self):
        valid_css_classes = (
            'padding-25-820-up', 'display-480-down', 'margin-5-2-5-2-1000-up', 'display-960-up-i', 'display-3_2rem-down'
        )
        names = ['padding', 'display', 'margin', 'display', 'display', ]
        values = ['25', 'none', '5-2-5-2', 'none', 'none', ]
        priorities = ['', '', '', 'important', '', ]
        limit_key = ('-up', '-down', '-up', '-up', '-down', )
        breakpoint = ('-820', '-480', '-1000', '-960', '-3_2rem', )
        converted_breakpoint = (px_to_em('820'), px_to_em('480'), px_to_em('1000'), px_to_em('960'), '3.2rem', )

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertTrue(breakpoint_parser.is_breakpoint, msg=breakpoint_parser.css_class)
            self.assertEqual(
                breakpoint_parser.breakpoint_dict['custom'][limit_key[i]],
                converted_breakpoint[i],
                msg=converted_breakpoint[i] + ' dict: ' + breakpoint_parser.breakpoint_dict['custom'][limit_key[i]]
            )
            self.assertEqual(
                breakpoint_parser.breakpoint_dict['custom']['breakpoint'],
                breakpoint[i],
                msg=breakpoint[i] + ' dict: ' + breakpoint_parser.breakpoint_dict['custom']['breakpoint']
            )

    def test_set_custom_breakpoint_key_Invalid(self):
        invalid_css_classes = (
            '-820-up', '480-down', 'margin-5-2-5-2-1000-', 'display-960-i', 'display-3_2rem',
        )
        names = ['padding', 'display', 'margin', 'display', 'display', ]
        values = ['25', 'none', '5-2-5-2', 'none', 'none', ]
        priorities = ['', '', '', 'important', '', ]
        limit_key = ('-up', '-down', '-up', '-up', '-down', )
        breakpoint = None

        for i, css_class in enumerate(invalid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority=priorities[i])
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertFalse(breakpoint_parser.is_breakpoint, msg=breakpoint_parser.css_class)
            self.assertEqual(
                breakpoint_parser.breakpoint_dict['custom'][limit_key[i]],
                breakpoint,
                msg=str(breakpoint) + ' dict: ' + str(breakpoint_parser.breakpoint_dict['custom'][limit_key[i]])
            )
            self.assertEqual(
                breakpoint_parser.breakpoint_dict['custom']['breakpoint'],
                breakpoint,
                msg=str(breakpoint) + ' dict: ' + str(breakpoint_parser.breakpoint_dict['custom']['breakpoint'])
            )

    def test_set_custom_breakpoint_key_ONLY(self):
        invalid_css_class = 'display-3_2rem-920-only'
        name = 'display'
        value = 'none'
        priority = ''
        limit_key = '-only'

        css_property = Property(name=name, value=value, priority=priority)
        breakpoint_parser = BreakpointParser(css_class=invalid_css_class, css_property=css_property)
        self.assertFalse(breakpoint_parser.is_breakpoint, msg=breakpoint_parser.css_class)

        try:
            should_not_exist = breakpoint_parser.breakpoint_dict['custom'][limit_key]
            self.assertTrue(False, msg=should_not_exist)
        except KeyError:
            self.assertTrue(True)

    def test_strip_breakpoint_limit(self):
        valid_css_classes = [
            'inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up',
            'xlarge-only', 'large-down', 'xsmall-up',
            'padding-25-820-up', 'display-480-down', 'margin-5-2-5-2-1000-up', 'display-960-up-i', 'display-3_2rem-down'
        ]
        names = [
            'display', 'display', 'color', 'padding', 'display', 'display', 'display',
            'padding', 'display', 'margin', 'display', 'display',
        ]
        values = [
            'inline', 'inline', 'green', '10', 'none', 'none', 'none',
            '25', 'none', '5-2-5-2', 'none', 'none',
        ]
        expected = [
            'inline', 'inline', 'green', 'padding-10', '', '', '',
            'padding-25', 'display', 'margin-5-2-5-2', 'display-i', 'display',
        ]

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            clean_css_class = breakpoint_parser.strip_breakpoint_limit()
            self.assertEqual(clean_css_class, expected[i])

    def test_is_display_True(self):
        valid_css_classes = ('display-small-down', 'medium-only', 'giant-up', 'display-720-up', 'display-369-down')
        names = ('display', 'display', 'display', 'display', 'display', )
        values = ('none', 'none', 'none', 'none', 'none', )

        for i, css_class in enumerate(valid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertTrue(breakpoint_parser.is_display(), msg=css_class)

    def test_is_display_False(self):
        invalid_css_classes = (
            'inline-small-up', 'inline-giant-down', 'green-xxsmall-only', 'padding-10-large-up',
            'padding-25-820-up', 'margin-5-2-5-2-1000-up',
        )
        names = ('display', 'display', 'color', 'padding', 'padding', 'margin', )
        values = ('inline', 'inline', 'green', '10', '25', '5-2-5-2', )

        for i, css_class in enumerate(invalid_css_classes):
            css_property = Property(name=names[i], value=values[i], priority='')
            breakpoint_parser = BreakpointParser(css_class=css_class, css_property=css_property)
            self.assertFalse(breakpoint_parser.is_display(), msg=css_class)

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

    def test_css_for_down_display_custom(self):
        css_class = 'display-369-down'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (min-width: 23.0625em) {\n' +
            '\t.display-369-down {\n' +
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

    def test_css_for_up_display_custom(self):
        css_class = 'display-720-up'
        name = 'display'
        value = 'none'
        expected = (
            '@media only screen and (max-width: 45.0em) {\n' +
            '\t.display-720-up {\n' +
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
