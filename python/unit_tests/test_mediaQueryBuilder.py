from unittest import TestCase, main
# custom
from classpropertyparser import ClassPropertyParser
from mediaquerybuilder import MediaQueryBuilder
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestMediaQueryBuilder(TestCase):
    def test_init_classes(self):
        class_set = {
            'cue-x5_0p', 'margin-top-10', 'bgc-h000', 'hide', 'margin-20', 'padding-top-10', 'height-200', 'padding-10',
            'valign-middle', 'b', 'width-150', 'width-50', 'font-size-48', 'c-blue', 'margin-top-50px',
            'text-align-center', 'height-50px', 'height-150px', 'bold', 'color-hfff', 'padding-b1 a5 c1% e5',
            'margin-1a% 10x% 3q% 1mp3',
        }
        expected_clean_set = {
            'margin-top-10', 'margin-20', 'padding-top-10', 'height-200', 'padding-10', 'width-150', 'width-50',
            'font-size-48',
            'c-blue', 'height-150px', 'bgc-h000', 'bold', 'color-hfff', 'height-50px', 'text-align-center',
            'margin-top-50px', 'valign-middle',
        }
        expected_removed_set = {
            'cue-x5_0p (cssutils invalid property value: x5.0%)',
            'hide (property_name not found in property_alias_dict.)',
            'padding-b1 a5 c1% e5 (Only a-z, 0-9, "_", and "-" are allowed in class name.)',
            'b (property_name not found in property_alias_dict.)',
            'margin-1a% 10x% 3q% 1mp3 (Only a-z, 0-9, "_", and "-" are allowed in class name.)'
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
