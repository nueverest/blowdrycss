from unittest import TestCase, main
# custom
from fontparser import FontParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestFontParser(TestCase):
    # font_value 'monospace' returns 'monospace'
    def test_generate_fallback_fonts_family_key(self):
        font_families = {'serif', 'sans-serif', 'monospace', 'fantasy'}
        font_parser = FontParser()
        for font_family in font_families:
            font_parser.font_value = font_family
            fallback_fonts = font_parser.generate_fallback_fonts()
            self.assertEqual(font_family, fallback_fonts)

    # font_value 'arial' returns 'arial, sans-serif'
    def test_generate_fallback_fonts_append_family(self):
        input_fonts = [
            'cambria', 'didot', 'garamond',
            'arial', 'helvetica', 'gadget',
            'courier', 'monaco', 'consolas',
            'copperplate', 'papyrus',
        ]
        expected = [
            'cambria, serif', 'didot, serif', 'garamond, serif',
            'arial, sans-serif', 'helvetica, sans-serif', 'gadget, sans-serif',
            'courier, monospace', 'monaco, monospace', 'consolas, monospace',
            'copperplate, fantasy', 'papyrus, fantasy',
        ]
        font_parser = FontParser()
        for i, font in enumerate(input_fonts):
            font_parser.font_value = font
            fallback_fonts = font_parser.generate_fallback_fonts()
            self.assertEqual(fallback_fonts, expected[i])

    # font_value 'invalid' returns 'arial, sans-serif'
    def test_generate_fallback_fonts_invalid(self):
        input_fonts = ['invalid', 'border', 'padding', 'oasnuth', 'oe2nth', '234']
        expected = 'serif'
        font_parser = FontParser()
        for font in input_fonts:
            font_parser.font_value = font
            fallback_fonts = font_parser.generate_fallback_fonts()
            self.assertEqual(fallback_fonts, expected)


if __name__ == '__main__':
    main()
