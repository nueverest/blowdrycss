from unittest import TestCase, main
# custom
import settings
from classpropertyparser import ClassPropertyParser
from mediaquerybuilder import MediaQueryBuilder
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMediaQueryBuilder(TestCase):
    def test_init_classes(self):
        class_set = {
            'margin-top-50px-xlarge-down', 'small-up', 'giant-only-i', 'display-large-down',
            'text-align-center-medium-down',  'bold-small-only', 'color-hfff-xsmall-only',
            'font-size-13-s-i', 'font-size-48em-s',
            'height-150px', 'valign-middle', 'font-size-48',
            'b', 'cue-x5_0p', 'hide', 'padding-b1 a5 c1% e5', 'margin-1a% 10x% 3q% 1mp3',
        }
        expected_clean_set = {
            'margin-top-50px-xlarge-down', 'small-up', 'giant-only-i', 'display-large-down',
            'text-align-center-medium-down',  'bold-small-only', 'color-hfff-xsmall-only',
            'font-size-13-s-i', 'font-size-48em-s',
        }
        expected_removed_set = {
            'cue-x5_0p (cssutils invalid property value: x5.0%)',
            'hide (property_name not found in property_alias_dict.)',
            'padding-b1 a5 c1% e5 (Only a-z, 0-9, "_", and "-" are allowed in class name.)',
            'b (property_name not found in property_alias_dict.)',
            'margin-1a% 10x% 3q% 1mp3 (Only a-z, 0-9, "_", and "-" are allowed in class name.)'
            'height-150px ()',
            'valign-middle ()',
            'font-size-48 ()',
        }
        property_parser = ClassPropertyParser(class_set=class_set)
        media_query_builder = MediaQueryBuilder(property_parser=property_parser)
        self.assertTrue(media_query_builder.property_parser.class_set == expected_clean_set,
                        msg=media_query_builder.property_parser.class_set)
        self.assertTrue(media_query_builder.property_parser.removed_class_set == expected_removed_set,
                        msg=media_query_builder.property_parser.removed_class_set)

    def test_class_is_parsable(self):
        pass

    def test_minify(self):
        pass

    def test_get_css_text(self):
        pass


if __name__ == '__main__':
    main()
