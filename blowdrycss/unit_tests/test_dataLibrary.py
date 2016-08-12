# python 2
from __future__ import absolute_import

# builtin
from unittest import TestCase, main

# custom
from blowdrycss.datalibrary import DataLibrary
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestDataLibrary(TestCase):
    data_library = DataLibrary()

    # Return a set() abbreviation patterns.
    # No dash: [First three letters]
    # Multi-dash: [First word + First letter after dash, (single, double, triple letter zen css code)]
    # Append dash '-' at the end of each abbreviation.
    # Do not abbreviate words less than or equal to 5 characters in length.
    #
    # The zen css code comes from concatenating the first letter of the string with the first letter after each dash.
    # e.g. 'border-top-width' --> 'btw-'
    #
    # Examples
    #               'color' --> set()
    #             'padding' --> {'pad-'}
    #          'margin-top' --> {'margin-t-', 'mt-'}
    # 'border-bottom-width' --> {'border-b-width', 'bbw-'}
    def test_get_property_aliases_short_word(self):
        property_names = ['top', 'color', 'cue', ]
        expected_abbreviation = set()
        for property_name in property_names:
            abbreviations = self.data_library.get_property_aliases(property_name=property_name)
            self.assertEqual(abbreviations, expected_abbreviation, msg=abbreviations)

    def test_get_property_aliases_single_word(self):
        property_names = ['padding', 'margin', 'background', ]
        expected_abbreviations = [{'pad-'}, {'mar-'}, {'bac-'}, ]
        for i, property_name in enumerate(property_names):
            abbreviations = self.data_library.get_property_aliases(property_name=property_name)
            self.assertEqual(abbreviations, expected_abbreviations[i], msg=abbreviations)

    def test_get_property_aliases_double_word(self):
        property_names = ['padding-top', 'margin-bottom', 'background-color', ]
        expected_abbreviations = [{'padding-t-', 'pt-'}, {'margin-b-', 'mb-'}, {'background-c-', 'bc-'}, ]
        for i, property_name in enumerate(property_names):
            abbreviations = self.data_library.get_property_aliases(property_name=property_name)
            self.assertEqual(abbreviations, expected_abbreviations[i], msg=abbreviations)

    def test_get_property_aliases_triple_word(self):
        property_names = ['border-bottom-width', 'page-break-inside', 'border-top-color', 'border-right-color', ]
        expected_abbreviations = [
            {'border-b-width-', 'bbw-'}, {'page-b-inside-', 'pbi-'}, {'border-t-color-', 'btc-'},
            {'border-r-color-', 'brc-'},
        ]
        for i, property_name in enumerate(property_names):
            abbreviations = self.data_library.get_property_aliases(property_name=property_name)
            self.assertEqual(abbreviations, expected_abbreviations[i], msg=abbreviations)

    def test_autogen_property_alias_dict(self):
        expected_dict = {
            'all': set(),
            'align-items': {'ai-', 'align-i-'},
            'outline': {'out-'}, 'border-left-width': {'blw-', 'border-l-width-'},
            'counter-reset': {'cr-', 'counter-r-'}, 'counter-increment': {'counter-i-', 'ci-'},
            'cue-before': {'cb-', 'cue-b-'}, 'text-decoration': {'td-', 'text-d-'},
            'background-color': {'bc-', 'background-c-'}, 'richness': {'ric-'},
            'border-right-color': {'brc-', 'border-r-color-'},
            'quotes': {'quo-'}, 'top': set(), 'outline-color': {'outline-c-', 'oc-'},
            'border-top-color': {'btc-', 'border-t-color-'}, 'position': {'pos-'},
            'speak-punctuation': {'sp-', 'speak-p-'}, 'elevation': {'ele-'}, 'border-left': {'bl-', 'border-l-'},
            'margin': {'mar-'}, 'border-right-width': {'brw-', 'border-r-width-'},
            'background-image': {'background-i-', 'bi-'}, 'visibility': {'vis-'}, 'cue-after': {'ca-', 'cue-a-'},
            'text-align': {'ta-', 'text-a-'}, 'font-variant': {'font-v-', 'fv-'}, 'volume': {'vol-'},
            'table-layout': {'table-l-', 'tl-'}, 'border-top-width': {'btw-', 'border-t-width-'}, 'widows': {'wid-'},
            'white-space': {'ws-', 'white-s-'}, 'outline-style': {'os-', 'outline-s-'}, 'height': {'hei-'},
            'margin-right': {'mr-', 'margin-r-'}, 'list-style-type': {'list-s-type-', 'lst-'},
            'border-spacing': {'border-s-', 'bs-'}, 'border-style': {'border-s-', 'bs-'},
            'border-left-style': {'border-l-style-', 'bls-'}, 'pause-after': {'pause-a-', 'pa-'}, 'clip': set(),
            'empty-cells': {'empty-c-', 'ec-'}, 'text-indent': {'ti-', 'text-i-'}, 'border-width': {'bw-', 'border-w-'},
            'line-height': {'lh-', 'line-h-'}, 'margin-top': {'mt-', 'margin-t-'}, 'speak-numeral': {'sn-', 'speak-n-'},
            'background': {'bac-'}, 'border-bottom-style': {'bbs-', 'border-b-style-'},
            'text-transform': {'text-t-', 'tt-'}, 'vertical-align': {'va-', 'vertical-a-'},
            'border-bottom-color': {'border-b-color-', 'bbc-'}, 'play-during': {'pd-', 'play-d-'}, 'cue': set(),
            'color': set(), 'pause': set(), 'border-bottom': {'bb-', 'border-b-'}, 'max-height': {'mh-', 'max-h-'},
            'list-style-image': {'lsi-', 'list-s-image-'}, 'padding-top': {'pt-', 'padding-t-'}, 'float': set(),
            'width': set(), 'page-break-inside': {'pbi-', 'page-b-inside-'}, 'word-spacing': {'ws-', 'word-s-'},
            'font-family': {'ff-', 'font-f-'}, 'border-top-style': {'border-t-style-', 'bts-'},
            'pause-before': {'pb-', 'pause-b-'}, 'bottom': {'bot-'}, 'cursor': {'cur-'}, 'min-width': {'mw-', 'min-w-'},
            'speak': set(), 'overflow': {'ove-'}, 'list-style': {'ls-', 'list-s-'},
            'opacity': {'opa-'},
            'margin-bottom': {'mb-', 'margin-b-'}, 'border-collapse': {'bc-', 'border-c-'},
            'border-left-color': {'border-l-color-', 'blc-'}, 'display': {'dis-'},
            'outline-width': {'ow-', 'outline-w-'}, 'border-color': {'bc-', 'border-c-'}, 'pitch': set(),
            'direction': {'dir-'}, 'border-bottom-width': {'bbw-', 'border-b-width-'}, 'clear': set(),
            'list-style-position': {'lsp-', 'list-s-position-'}, 'font-style': {'fs-', 'font-s-'},
            'padding-right': {'padding-r-', 'pr-'}, 'speech-rate': {'sr-', 'speech-r-'},
            'border-top': {'bt-', 'border-t-'}, 'font-size': {'fs-', 'font-s-'},
            'background-attachment': {'ba-', 'background-a-'}, 'min-height': {'mh-', 'min-h-'}, 'left': set(),
            'page-break-before': {'pbb-', 'page-b-before-'}, 'stress': {'str-'}, 'right': set(), 'font': set(),
            'padding-left': {'padding-l-', 'pl-'}, 'unicode-bidi': {'ub-', 'unicode-b-'},
            'padding-bottom': {'pb-', 'padding-b-'}, 'caption-side': {'caption-s-', 'cs-'}, 'content': {'con-'},
            'page-break-after': {'page-b-after-', 'pba-'}, 'border': {'bor-'}, 'z-index': {'z-i-', 'zi-'},
            'background-position': {'background-p-', 'bp-'}, 'font-weight': {'font-w-', 'fw-'},
            'voice-family': {'vf-', 'voice-f-'}, 'max-width': {'mw-', 'max-w-'}, 'letter-spacing': {'ls-', 'letter-s-'},
            'text-shadow': {'ts-', 'text-s-', },
            'speak-header': {'speak-h-', 'sh-'}, 'pitch-range': {'pr-', 'pitch-r-'},
            'border-right-style': {'brs-', 'border-r-style-'}, 'padding': {'pad-'},
            'background-repeat': {'br-', 'background-r-'}, 'margin-left': {'margin-l-', 'ml-'}, 'orphans': {'orp-'},
            'border-right': {'border-r-', 'br-'},
            'border-radius': {'border-r-', 'br-'},
            'border-top-left-radius': {'btl-', 'border-t-left-radius-'},
            'border-top-right-radius': {'btr-', 'border-t-right-radius-'},
            'border-bottom-left-radius': {'bbl-', 'border-b-left-radius-'},
            'border-bottom-right-radius': {'bbr-', 'border-b-right-radius-'},
        }
        self.data_library.autogen_property_alias_dict()
        self.assertEqual(
                self.data_library.property_alias_dict,
                expected_dict,
                msg=self.data_library.property_alias_dict
        )

    def test_merge_dictionaries(self):
        data_library2 = DataLibrary()
        full_dict = {
            'background': {'bg-', },
            'background-color': set(),
            'color': {'c-', },
            'font-size': {'fsize-', 'f-size-', },
            'font-weight': {'bold', 'bolder', 'lighter', 'fweight-', 'f-weight-', },
            'height': {'h-', },
            'margin': {'m-', },
        }
        value_as_dict = {
            'color': {'col-', },
            'margin': {'mar-', },
        }
        settings_custom_alias_dict = {
            'background-color': {'bgc-', 'bg-c-', 'bg-color-', },
            'color': {'coco-', },
        }
        expected_dict = {
            'background': {'bg-', },
            'background-color': {'bgc-', 'bg-c-', 'bg-color-', },
            'color': {'c-', 'col-', 'coco-', },
            'font-size': {'fsize-', 'f-size-', },
            'font-weight': {'bold', 'bolder', 'lighter', 'fweight-', 'f-weight-', },
            'height': {'h-', },
            'margin': {'m-', 'mar-', },
        }
        data_library2.property_alias_dict = full_dict
        data_library2.property_value_as_alias_dict = value_as_dict
        data_library2.custom_property_alias_dict = settings_custom_alias_dict
        data_library2.merge_dictionaries()
        self.assertEqual(data_library2.property_alias_dict, expected_dict)

    def test_merge_dictionaries_invalid_key(self):
        dict1 = {'font-size': {'fsize-', 'f-size-', }, }
        dict2 = {'invalid_key': {'col-', }, }
        self.data_library.property_alias_dict = dict1
        self.data_library.property_value_as_alias_dict = dict2
        self.assertRaises(KeyError, self.data_library.merge_dictionaries)

    def test_merge_dictionaries_custom_property_alias_dict_invalid_key(self):
        original = settings.custom_property_alias_dict                      # Save settings.

        dict1 = {'font-size': {'fsize-', 'f-size-', }, }
        dict2 = {'invalid_key': {'col-', }, }
        self.data_library.property_alias_dict = dict1
        self.data_library.property_value_as_alias_dict = dict1
        settings.custom_property_alias_dict = dict2
        self.assertRaises(KeyError, self.data_library.merge_dictionaries)

        settings.custom_property_alias_dict = original                      # Reset settings.

    # Expects that dict1 will pass straight through since there is nothing to merge with it.
    def test_merge_dictionaries_empty_custom_dict(self):
        data_library2 = DataLibrary()
        dict1 = {'font-size': {'fsize-', 'f-size-', }, }
        value_as_dict = None
        data_library2.property_alias_dict = dict1
        data_library2.property_value_as_alias_dict = value_as_dict
        data_library2.custom_property_alias_dict = None
        data_library2.merge_dictionaries()
        self.assertEqual(data_library2.property_alias_dict, dict1)

    def test_set_clashing_aliases(self):
        expected_clashes = {
            'border-collapse': {'border-c-', 'bc-'}, 'border-style': {'bs-', 'border-s-'},
            'font-style': {'font-s-', 'fs-'}, 'background-repeat': {'br-'}, 'pitch-range': {'pr-'},
            'padding-bottom': {'pb-'}, 'min-width': {'mw-'},
            'border-right': {'br-', 'border-r-'},
            'border-radius': {'br-', 'border-r-'},
            'letter-spacing': {'ls-'},
            'border-spacing': {'bs-', 'border-s-'}, 'white-space': {'ws-'}, 'word-spacing': {'ws-'},
            'max-width': {'mw-'}, 'padding-right': {'pr-'}, 'background-color': {'bc-'}, 'max-height': {'mh-'},
            'border-color': {'border-c-', 'bc-'}, 'pause-before': {'pb-'}, 'min-height': {'mh-'}, 'list-style': {'ls-'},
            'font-size': {'font-s-', 'fs-'}
        }
        unused_on_purpose_dict = self.data_library.autogen_property_alias_dict()
        self.data_library.set_clashing_aliases()
        actual_clashes = self.data_library.clashing_alias_dict
        self.assertEqual(actual_clashes, expected_clashes)

    def test_remove_clashing_aliases(self):
        expected_clean_dict = {
            'border-left': {'bl-', 'border-l-'},
            'white-space': set(),
            'cursor': {'cur-'},
        }
        initial_dict = {
            'border-left': {'bl-', 'border-l-', 'clash1-', 'clash2-'},
            'white-space': {'clash2-'},
            'cursor': {'cur-', 'clash1-', },
        }
        expected_clashes = {
            'border-left': {'clash2-', 'clash1-'},
            'white-space': {'clash2-'},
            'cursor': {'clash1-'}
        }
        self.data_library.property_alias_dict = initial_dict
        self.data_library.set_clashing_aliases()
        clash_dict = self.data_library.clashing_alias_dict
        self.assertEqual(clash_dict, expected_clashes, msg=clash_dict)  # Sanity check
        self.data_library.remove_clashing_aliases()
        self.assertEqual(self.data_library.property_alias_dict, expected_clean_dict)

    def test_default_property_alias_dict(self):
        self.maxDiff = None
        expected = {
            'all': set(),
            'align-items': {'ai-', 'align-i-', },
            'min-width': {'min-w-'}, 'speak': {'spell-out'}, 'width': {'w-'},
            'page-break-inside': {'page-b-inside-', 'pbi-'}, 'padding-right': {'padding-r-'}, 'outline': {'out-'},
            'margin-right': {'mr-', 'margin-r-'}, 'speak-numeral': {'digits', 'speak-n-', 'sn-', 'continuous'},
            'border-right-style': {'brs-', 'border-r-style-'}, 'padding-bottom': {'padding-b-'},
            'volume': {'loud', 'x-soft', 'silent', 'vol-', 'x-loud', 'soft'},
            'list-style-type': {'upper-alpha', 'disc', 'lst-', 'lower-greek', 'lower-alpha', 'georgian', 'circle',
                                'upper-latin', 'list-s-type-', 'lower-latin', 'upper-roman', 'armenian', 'decimal',
                                'lower-roman', 'square', 'decimal-leading-zero'},
            'border-bottom-width': {'border-b-width-', 'bbw-'}, 'right': set(),
            'text-align': {'ta-', 'talign-', 'text-a-', 't-align-'}, 'padding': {'pad-', 'p-'},
            'outline-width': {'outline-w-', 'ow-'}, 'speak-punctuation': {'code', 'sp-', 'speak-p-'},
            'font-size': {'fsize-', 'f-size-'}, 'visibility': {'collapse', 'vis-'},
            'counter-increment': {'counter-i-', 'ci-'}, 'border-right': set(), 'cue': set(),
            'vertical-align': {'baseline', 'sub', 'v-align-', 'text-top', 'middle', 'text-bottom', 'vertical-a-',
                               'valign-', 'va-', 'super'}, 'page-break-after': {'pba-', 'page-b-after-'},
            'elevation': {'higher', 'ele-', 'lower', 'above', 'below', 'level'}, 'line-height': {'lh-', 'line-h-'},
            'font': set(), 'min-height': {'min-h-'},
            'speech-rate': {'sr-', 'speech-r-', 'x-fast', 'fast', 'faster', 'x-slow', 'slow', 'slower'},
            'z-index': {'zi-', 'z-i-'}, 'list-style': {'list-s-'}, 'background-position': {'bp-', 'background-p-'},
            'background-color': {'bg-color-', 'background-c-', 'bgc-', 'bg-c-'}, 'margin-left': {'margin-l-', 'ml-'},
            'pitch': {'x-high', 'low', 'high', 'x-low'}, 'pitch-range': {'pitch-r-'},
            'background-repeat': {'no-repeat', 'repeat-x', 'background-r-', 'repeat-y'},
            'pause': set(), 'word-spacing': {'word-s-'},
            'border-bottom': {'bb-', 'border-b-'}, 'border-right-width': {'brw-', 'border-r-width-'},
            'page-break-before': {'page-b-before-', 'pbb-'}, 'border-collapse': set(),
            'list-style-position': {'list-s-position-', 'lsp-', 'inside', 'outside'},
            'list-style-image': {'list-s-image-', 'lsi-'}, 'stress': {'str-'}, 'height': {'h-', 'hei-'},
            'font-variant': {'fv-', 'small-caps', 'font-v-'}, 'cue-after': {'ca-', 'cue-a-'},
            'cursor': {'wait', 'default', 'crosshair', 'move', 'pointer', 'text', 'se-resize', 'help', 'n-resize',
                       'e-resize', 's-resize', 'progress', 'w-resize', 'ne-resize', 'nw-resize', 'cur-', 'sw-resize'},
            'table-layout': {'table-l-', 'tl-'}, 'speak-header': {'once', 'sh-', 'always', 'speak-h-'}, 'clip': set(),
            'unicode-bidi': {'bidi-override', 'ub-', 'unicode-b-', 'embed'},
            'border-left-style': {'border-l-style-', 'bls-'}, 'margin': {'mar-', 'm-'}, 'widows': {'wid-'},
            'pause-before': {'pause-b-'}, 'text-indent': {'ti-', 'text-i-'},
            'border-top-style': {'border-t-style-', 'bts-'}, 'overflow': {'ove-', 'scroll'},
            'color': {'c-', 'rgb', 'rgba', 'hsl', 'hsla',
                # SVG 1.1 Color Keyword Reference: http://www.w3.org/TR/SVG/types.html#ColorKeywords
                'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood',
                'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan',
                'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
                'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon',
                'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise',
                'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue',
                'firebrick', 'floralwhite', 'forestgreen', 'fuchsia',
                'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow',
                'honeydew', 'hotpink',
                'indianred', 'indigo', 'ivory',
                'khaki',
                'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
                'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink',
                'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey',
                'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen',
                'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
                'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
                'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
                'navajowhite', 'navy',
                'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid',
                'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff',
                'peru', 'pink', 'plum', 'powderblue', 'purple',
                'red', 'rosybrown', 'royalblue',
                'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue',
                'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue',
                'tan', 'teal', 'thistle', 'tomato', 'turquoise',
                'violet',
                'wheat', 'white', 'whitesmoke',
                'yellow', 'yellowgreen',}, 'top': set(), 'bottom': {'bot-'}, 'pause-after': {'pause-a-', 'pa-'},
            'voice-family': {'voice-f-', 'vf-'}, 'border-bottom-color': {'border-b-color-', 'bbc-'},
            'border-right-color': {'border-r-color-', 'brc-'}, 'caption-side': {'cs-', 'caption-s-'},
            'outline-color': {'oc-', 'outline-c-'}, 'position': {'pos-', 'relative', 'absolute', 'static'},
            'border-left': {'bl-', 'border-l-'}, 'direction': {'rtl', 'dir-', 'ltr'}, 'clear': set(), 'left': set(),
            'cue-before': {'cue-b-', 'cb-'}, 'border-top': {'border-t-', 'bt-'},
            'padding-top': {'p-top-', 'padding-t-', 'pt-'}, 'max-width': {'max-w-'}, 'background': {'bg-', 'bac-'},
            'border-bottom-style': {'border-b-style-', 'bbs-'},
            'text-transform': {'tt-', 'text-t-', 'uppercase', 'capitalize', 'lowercase'},
            'display': {
                'block', 'list-item', 'flex', 'inline-flex', 'run-in',
                'table-header-group', 'table-caption', 'inline', 'table-column-group',
                'table-row', 'inline-block', 'inline-table', 'table', 'table-cell', 'dis-',
                'table-footer-group', 'table-row-group', 'table-column',
                'xxsmall', 'xsmall', 'small', 'medium', 'large', 'xlarge', 'xxlarge',
                'giant', 'xgiant', 'xxgiant',
            },
            'border-top-color': {'btc-', 'border-t-color-'}, 'letter-spacing': {'letter-s-'},
            'border-radius': set(),
            'border-top-left-radius': {'btl-', 'border-t-left-radius-'},
            'border-top-right-radius': {'btr-', 'border-t-right-radius-'},
            'border-bottom-left-radius': {'bbl-', 'border-b-left-radius-'},
            'border-bottom-right-radius': {'bbr-', 'border-b-right-radius-'},
            'font-weight': {'font-w-', 'f-weight-', 'fweight-', 'lighter', 'bold', 'fw-', 'bolder'},
            'border-spacing': set(), 'padding-left': {'pl-', 'padding-l-'}, 'font-style': {'oblique', 'italic'},
            'empty-cells': {'empty-c-', 'ec-', }, 'margin-top': {'margin-t-', 'm-top-', 'mt-'},
            'border-color': set(),
            'text-decoration': {'overline', 'text-d-', 'underline', 'td-', 'blink', 'line-through'}, 'quotes': {'quo-'},
            'text-shadow': {'ts-', 'text-s-'},
            'opacity': {'opa-'},
            'outline-style': {'outline-s-', 'os-'}, 'border-style': set(), 'counter-reset': {'counter-r-', 'cr-'},
            'margin-bottom': {'margin-b-', 'm-bot-', 'mb-'}, 'orphans': {'orp-'},
            'background-attachment': {'ba-', 'background-a-'}, 'border-width': {'border-w-', 'bw-'},
            'border': {'bor-'}, 'content': {'no-close-quote', 'no-open-quote', 'close-quote', 'con-', 'open-quote'},
            'richness': {'ric-'}, 'float': set(), 'white-space': {'white-s-'}, 'max-height': {'max-h-'},
            'border-left-color': {'border-l-color-', 'blc-'}, 'border-left-width': {'blw-', 'border-l-width-'},
            'background-image': {'background-i-', 'bi-'}, 'border-top-width': {'border-t-width-', 'btw-'},
            'play-during': {'mix', 'play-d-', 'pd-'},
            'font-family': {'serif', 'georgia', 'palatino', 'times', 'cambria', 'didot', 'garamond', 'perpetua',
                            'rockwell', 'baskerville',
                            'sans-serif', 'arial', 'helvetica', 'gadget', 'cursive', 'impact', 'charcoal', 'tahoma',
                            'geneva', 'verdana', 'calibri', 'candara', 'futura', 'optima',
                            'monospace', 'courier', 'monaco', 'consolas',
                            'fantasy', 'copperplate', 'papyrus', 'ff-', 'font-f-'},
        }
        data_library = DataLibrary()
        actual = data_library.property_alias_dict
        self.assertEqual(actual, expected, msg=expected)


if __name__ == '__main__':
    main()
