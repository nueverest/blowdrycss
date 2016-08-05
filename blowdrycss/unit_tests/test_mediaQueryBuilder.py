# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main

# custom
from blowdrycss.classpropertyparser import ClassPropertyParser
from blowdrycss.mediaquerybuilder import MediaQueryBuilder

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestMediaQueryBuilder(TestCase):
    def test_init_classes(self):
        class_set = {
            # Valid
            'margin-top-50px-xlarge-down', 'small-up', 'giant-only-i', 'display-large-down',
            'text-align-center-medium-down',  'bold-small-only', 'color-hfff-xsmall-only',
            'font-size-13-s-i', 'font-size-48em-s',
            # Invalid - The following should be removed.
            'width-100-xxlarge-down-s', 'padding-50-xxsmall-only-s',                        # mixed
            'squirrel-medium-only',                                                         # invalid css property name
            'font-size-AA-s',                                                               # invalid property value
            'height-150px', 'valign-middle', 'font-size-48',
            'b', 'cue-x5_0p', 'hide', 'padding-b1 a5 c1% e5', 'margin-1a% 10x% 3q% 1mp3',
            'display-720-down',
        }
        expected_clean_set = {
            'margin-top-50px-xlarge-down', 'small-up', 'giant-only-i', 'display-large-down',
            'text-align-center-medium-down', 'bold-small-only', 'color-hfff-xsmall-only',
            'font-size-13-s-i', 'font-size-48em-s', 'display-720-down',
        }
        expected_removed_set = {
            'width-100-xxlarge-down-s (Breakpoint and scaling media query syntax cannot be combined.)',
            'padding-50-xxsmall-only-s (Breakpoint and scaling media query syntax cannot be combined.)',
            'squirrel-medium-only is not a media query css_class selector.',
            'font-size-aa-s (cssutils invalid property value: aa)',
            'cue-x5_0p is not a media query css_class selector.',
            'hide is not a media query css_class selector.',
            'padding-b1 a5 c1% e5 (Only a-z, 0-9, "_", and "-" are allowed in class name.)',
            'b is not a media query css_class selector.',
            'margin-1a% 10x% 3q% 1mp3 (Only a-z, 0-9, "_", and "-" are allowed in class name.)',
            'height-150px is not a media query css_class selector.',
            'valign-middle is not a media query css_class selector.',
            'font-size-48 is not a media query css_class selector.',
        }
        property_parser = ClassPropertyParser(class_set=class_set)
        media_query_builder = MediaQueryBuilder(property_parser=property_parser)
        self.assertTrue(media_query_builder.property_parser.class_set == expected_clean_set,
                        msg=media_query_builder.property_parser.class_set)
        self.assertTrue(media_query_builder.property_parser.removed_class_set == expected_removed_set,
                        msg=media_query_builder.property_parser.removed_class_set)

    def test_init_css_media_queries(self):
        class_set = {
            'margin-top-50px-xlarge-down',
            'small-up',
            'giant-only-i',
            'display-large-down',
            'text-align-center-medium-down',
            'bold-small-only',
            'color-hfff-xsmall-only',
            'display-720-up',

            'font-size-13-s-i',
            'font-size-48em-s',
            'padding-16-s-i',

            'height-150px', 'valign-middle', 'font-size-48',
            'b', 'cue-x5_0p', 'hide', 'padding-b1 a5 c1% e5', 'margin-1a% 10x% 3q% 1mp3',
        }
        expected_css_media_queries = {
            (
                '@media only screen and (max-width: 85.375em) {\n' +
                '\t.margin-top-50px-xlarge-down {\n' +
                '\t\tmargin-top: 3.125em;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (max-width: 15.0625em) {\n' +
                '\t.small-up {\n' +
                '\t\tdisplay: none;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (max-width: 120.0625em) {\n' +
                '\t.giant-only-i {\n' +
                '\t\tdisplay: none !important;\n' +
                '\t}\n' +
                '}\n\n' +
                '@media only screen and (min-width: 160.0em) {\n' +
                '\t.giant-only-i {\n' +
                '\t\tdisplay: none !important;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (min-width: 64.0em) {\n' +
                '\t.display-large-down {\n' +
                '\t\tdisplay: none;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.text-align-center-medium-down {\n' +
                '\t\ttext-align: center;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (min-width: 15.0625em) and (max-width: 30.0em) {\n' +
                '\t.bold-small-only {\n' +
                '\t\tfont-weight: bold;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (min-width: 7.5625em) and (max-width: 15.0em) {\n' +
                '\t.color-hfff-xsmall-only {\n' +
                '\t\tcolor: #fff;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '.font-size-13-s-i { font-size: 0.8125em !important; }\n\n' +
                '@media only screen and (max-width: 64.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.779em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.7222em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 30.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.65em !important; }\n' +
                '}\n\n'
            ),
            (
                '.font-size-48em-s { font-size: 48em; }\n\n' +
                '@media only screen and (max-width: 64.0em) {\n' +
                '\t.font-size-48em-s { font-size: 46.0211em; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.font-size-48em-s { font-size: 42.6667em; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 30.0em) {\n' +
                '\t.font-size-48em-s { font-size: 38.4em; }\n' +
                '}\n\n'
            ),
            (
                '.padding-16-s-i { padding: 1em !important; }\n\n' +
                '@media only screen and (max-width: 64.0em) {\n' +
                '\t.padding-16-s-i { padding: 0.9588em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.padding-16-s-i { padding: 0.8889em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 30.0em) {\n' +
                '\t.padding-16-s-i { padding: 0.8em !important; }\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.display-720-up {\n' +
                '\t\tdisplay: none;\n' +
                '\t}\n' +
                '}\n\n'
            ),
        }
        property_parser = ClassPropertyParser(class_set=class_set)
        media_query_builder = MediaQueryBuilder(property_parser=property_parser)
        self.assertTrue(media_query_builder.css_media_queries == expected_css_media_queries,
                        msg=media_query_builder.css_media_queries)

    # def test_class_is_parsable(self):
    #     pass

    def test_get_css_text(self):
        class_set = {'giant-only-i', 'color-hfff-xsmall-only', 'font-size-13-s-i', }
        expected_media_query = {
            (
                '@media only screen and (max-width: 120.0625em) {\n' +
                '\t.giant-only-i {\n' +
                '\t\tdisplay: none !important;\n' +
                '\t}\n' +
                '}\n\n' +
                '@media only screen and (min-width: 160.0em) {\n' +
                '\t.giant-only-i {\n' +
                '\t\tdisplay: none !important;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '@media only screen and (min-width: 7.5625em) and (max-width: 15.0em) {\n' +
                '\t.color-hfff-xsmall-only {\n' +
                '\t\tcolor: #fff;\n' +
                '\t}\n' +
                '}\n\n'
            ),
            (
                '.font-size-13-s-i { font-size: 0.8125em !important; }\n\n' +
                '@media only screen and (max-width: 64.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.779em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 45.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.7222em !important; }\n' +
                '}\n\n' +
                '@media only screen and (max-width: 30.0em) {\n' +
                '\t.font-size-13-s-i { font-size: 0.65em !important; }\n' +
                '}\n\n'
            ),
        }
        property_parser = ClassPropertyParser(class_set=class_set)
        media_query_builder = MediaQueryBuilder(property_parser=property_parser)
        css = media_query_builder.get_css_text()

        for media_query in expected_media_query:
            self.assertTrue(media_query in css, msg=css)


if __name__ == '__main__':
    main()
