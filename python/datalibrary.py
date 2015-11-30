from collections import OrderedDict
from copy import deepcopy
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# DataLibrary is not intended for use outside of this file as each time its' called it rebuilds the dictionaries.
class DataLibrary(object):
    def __init__(self):
        # TODO: If no new regexes are added consider moving to colorparser.
        # Regexes match the following string patterns:
        # 'h123', 'h123456', 'h123 bold', 'h123456 underline', 'underline h123 bold',
        # Note: If this dictionary grows write a function that detects regex conflicts.
        self.property_regex_dict = {
            'color': {r"(h[0-9a-f]{3} ?)$", r"(h[0-9a-f]{6} ?)$"},
        }

        # Font-Family References:
        # http://www.cssfontstack.com/
        # http://www.w3schools.com/cssref/css_websafe_fonts.asp
        # https://mathiasbynens.be/notes/unquoted-font-family

        # TODO: What about fonts "san-serif", etc.
        # TODO: move this to a CSV file and autogenerate this dictionary from CSV.
        # Used to define custom class aliases for a given property_name.
        # Feel free to modify as you would like.
        # Please keep in mind that if you define an alias that clashes with an alias in this dict() or the dict()
        # auto-generated by initialize_property_alias_dict() that it will be removed.
        # Clashing aliases are printed when get_clashing_aliases() is run.
        #
        # Aliases already known to clash are: {
        #     'list-style': {'ls-'}, 'border-right': {'br-'}, 'font-style': {'fs-', 'font-s-'},
        #     'border-spacing': {'border-s-', 'bs-'}, 'max-width': {'mw-'}, 'border-color': {'bc-', 'border-c-'},
        #     'word-spacing': {'ws-'}, 'pause-before': {'pb-'}, 'border-style': {'border-s-', 'bs-'},
        #     'background-repeat': {'br-'}, 'padding-bottom': {'pb-'}, 'font-size': {'fs-', 'font-s-'},
        #     'max-height': {'mh-'}, 'min-height': {'mh-'}, 'padding-right': {'pr-'}, 'background-color': {'bc-'},
        #     'white-space': {'ws-'}, 'border-collapse': {'bc-', 'border-c-'}, 'letter-spacing': {'ls-'},
        #     'pitch-range': {'pr-'}, 'min-width': {'mw-'}
        # }
        #
        # Dictionary contains:
        #   css property name as 'keys'
        #   list of aliases as 'values' - An alias can be shorthand for the property name.
        self.custom_property_alias_dict = {
            'azimuth': {'left-side', 'far-left', 'center-left', 'center-right', 'far-right', 'right-side', 'behind',
                        'leftwards', 'rightwards', },
            'background': {'bg-', },
            'background-color': {'bgc-', 'bg-c-', 'bg-color-', },
            'background-repeat': {'repeat', 'repeat-x', 'repeat-y', 'no-repeat', },
            'color': {'c-', 'rgb', 'rgba', 'hsl', 'hsla', 'aqua', 'black', 'blue', 'fuchsia', 'gray',
                      'green', 'lime', 'maroon', 'navy', 'olive', 'orange', 'purple', 'red', 'silver',
                      'teal', 'white', 'yellow', },
            'content': {'open-quote', 'close-quote', 'no-open-quote', 'no-close-quote', },
            'cursor': {'crosshair', 'default', 'pointer', 'move', 'e-resize', 'ne-resize', 'nw-resize', 'n-resize',
                       'se-resize', 'sw-resize', 's-resize', 'w-resize', 'text', 'wait', 'help', 'progress', },
            'direction': {'ltr', 'rtl'},
            'display': {'inline', 'block', 'list-item', 'inline-block', 'table', 'inline-table', 'table-row-group',
                        'table-header-group', 'table-footer-group', 'table-row', 'table-column-group', 'table-column',
                        'table-cell', 'table-caption', },
            'elevation': {'below', 'level', 'above', 'higher', 'lower', },
            'font-family': {'serif', 'georgia', 'palatino', 'times', 'cambria', 'didot', 'garamond', 'perpetua',
                            'rockwell', 'baskerville',
                            'sans-serif', 'arial', 'helvetica', 'gadget', 'cursive', 'impact', 'charcoal', 'tahoma',
                            'geneva', 'verdana', 'calibri', 'candara', 'futura', 'optima',
                            'monospace', 'courier', 'monaco', 'consolas',
                            'fantasy', 'copperplate', 'papyrus', },
            'font-size': {'fsize-', 'f-size-', },
            'font-style': {'italic', 'oblique', },
            'font-variant': {'small-caps', },
            'font-weight': {'bold', 'bolder', 'lighter', 'fweight-', 'f-weight-', },
            'height': {'h-', },
            'list-style-position': {'inside', 'outside', },
            'list-style-type': {'disc', 'circle', 'square', 'decimal', 'decimal-leading-zero', 'lower-roman',
                                'upper-roman', 'lower-greek', 'lower-latin', 'upper-latin', 'armenian',
                                'georgian', 'lower-alpha', 'upper-alpha', },
            'margin': {'m-', },
            'margin-top': {'m-top-', },
            'margin-bottom': {'m-bot-', },
            'overflow': {'visible', 'hidden', 'scroll', },
            'padding': {'p-', 'pad-', },
            'padding-top': {'p-top-', },
            'pitch': {'x-low', 'low', 'high', 'x-high'},
            'play-during': {'mix', 'repeat', },
            'position': {'static', 'relative', 'absolute', 'pos-', },
            'speak-header': {'once', 'always'},
            'speak-numeral': {'digits', 'continuous', },
            'speak-punctuation': {'code', },
            'speak': {'spell-out', },
            'speech-rate': {'x-slow', 'slow', 'fast', 'x-fast', 'faster', 'slower', },
            'text-align': {'talign-', 't-align-', },
            'text-decoration': {'underline', 'overline', 'line-through', 'blink', },
            'text-transform': {'capitalize', 'uppercase', 'lowercase', },
            'unicode-bidi': {'embed', 'bidi-override', },
            'vertical-align': {'baseline', 'sub', 'super', 'middle', 'text-top', 'text-bottom', 'valign-', 'v-align-'},
            'visibility': {'visible', 'hidden', 'collapse', },
            'volume': {'silent', 'x-soft', 'soft', 'loud', 'x-loud', },
            'width': {'w-', },
        }

        # Source: http://www.w3.org/TR/CSS21/propidx.html
        self.property_names = {
            'azimuth', 'background', 'background-attachment', 'background-color', 'background-image',
            'background-position', 'background-repeat', 'border', 'border-bottom', 'border-bottom-color',
            'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-left',
            'border-left-color', 'border-left-style', 'border-left-width', 'border-right', 'border-right-color',
            'border-right-style', 'border-right-width', 'border-spacing', 'border-style', 'border-top',
            'border-top-color', 'border-top-style', 'border-top-width', 'border-width', 'bottom',
            'caption-side', 'clear', 'clip', 'color', 'content', 'counter-increment', 'counter-reset', 'cue',
            'cue-after', 'cue-before', 'cursor', 'direction', 'display', 'elevation', 'empty-cells', 'float',
            'font', 'font-family', 'font-size', 'font-style', 'font-variant', 'font-weight', 'height', 'left',
            'letter-spacing', 'line-height', 'list-style', 'list-style-image', 'list-style-position',
            'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'max-height',
            'max-width', 'min-height', 'min-width', 'orphans', 'outline', 'outline-color', 'outline-style',
            'outline-width', 'overflow', 'padding', 'padding-bottom', 'padding-left', 'padding-right',
            'padding-top', 'page-break-after', 'page-break-before', 'page-break-inside', 'pause', 'pause-after',
            'pause-before', 'pitch', 'pitch-range', 'play-during', 'position', 'quotes', 'richness', 'right', 'speak',
            'speak-header', 'speak-numeral', 'speak-punctuation', 'speech-rate', 'stress', 'table-layout',
            'text-align', 'text-decoration', 'text-indent', 'text-transform', 'top', 'unicode-bidi', 'vertical-align',
            'visibility', 'voice-family', 'volume', 'white-space', 'widows', 'width', 'word-spacing', 'z-index'
        }

        self.clashing_alias_dict = {}
        self.property_alias_dict = self.build_property_alias_dict()     # Calls set_clashing_aliases()

        # Alphabetical Property Dictionaries
        self.alphabetical_property_dict = OrderedDict(sorted(self.property_alias_dict.items(), key=lambda t: t[0]))
        self.alphabetical_clashing_dict = OrderedDict(sorted(self.clashing_alias_dict.items(), key=lambda t: t[0]))

        # Generate Markdown Files
        self.clashing_alias_markdown = self.dict_to_markdown(
            key_title=u'Property Name', value_title=u'Clashing Aliases', _dict=self.alphabetical_clashing_dict
        )
        self.property_alias_markdown = self.dict_to_markdown(
            key_title=u'Property Name', value_title=u'Valid Aliases', _dict=self.alphabetical_property_dict
        )

        # Generate HTML Files
        self.clashing_alias_html = self.dict_to_html(
            key_title=u'Property Name', value_title=u'Clashing Aliases', _dict=self.alphabetical_clashing_dict
        )
        self.property_alias_html = self.dict_to_html(
            key_title=u'Property Name', value_title=u'Valid Aliases', _dict=self.alphabetical_property_dict
        )

        # Debug
        # print('property_alias_dict', self.property_alias_dict)
        # print('clashing_alias_markdown', self.clashing_alias_markdown)
        # print('clashing_alias_html\n', self.clashing_alias_html)
        # print('property_alias_markdown', self.property_alias_markdown)

        # TODO: Review whether this is still necessary as [key] notation might fix this issue.
        # Sort property_alias_dict with the longest items first as the most verbose match is preferred.
        # i.e. If css_class == 'margin-top' Then match the property_alias_dict key 'margin-top' not 'margin'
        self.ordered_property_dict = OrderedDict(
            sorted(self.property_alias_dict.items(), key=lambda t: len(t[0]), reverse=True)
        )

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
    @staticmethod
    def get_abbreviated_property_names(property_name=''):
        if len(property_name) <= 5:                                 # Do not abbreviate short words (<= 5 letters).
            return set()

        abbreviations = set()                                       # First three letters
        if '-' in property_name:                                    # First dash
            dash_index1 = property_name.index('-')
            suffix = property_name[dash_index1 + 1:]
            if '-' in suffix:                                       # Second dash (rare)
                dash_index2 = suffix.index('-')
                abbreviations.add(                                  # Three letter abbreviation
                    property_name[0] + property_name[dash_index1 + 1] + suffix[dash_index2 + 1] + '-'
                )
                abbreviations.add(property_name[:dash_index1 + 2] + '-' + suffix[dash_index2 + 1:] + '-')
            else:
                abbreviations.add(property_name[0] + property_name[dash_index1 + 1] + '-')
                abbreviations.add(property_name[:dash_index1 + 2] + '-')
        else:
            abbreviations.add(property_name[:3] + '-')
        return abbreviations

    # TODO: Ask cssutils guys about combining class names for matching properties.

    # Accepts a set of property names.
    # Returns an alias dictionary with
    # Key   = Property Name
    # Value = Alias abbreviation set
    def initialize_property_alias_dict(self, property_names=set()):
        alias_dict = {}
        for property_name in property_names:
            abbreviations = self.get_abbreviated_property_names(property_name=property_name)
            value = abbreviations
            alias_dict[property_name] = value
        return alias_dict

    # Merge two dictionaries. Note that all keys in custom_dict must exist within property_dict.
    @staticmethod
    def merge_dicts(property_dict=None, custom_dict=None):
        if custom_dict is not None:
            for property_name, alias_set in custom_dict.items():
                try:
                    property_dict[property_name] = property_dict[property_name].union(alias_set)
                except KeyError:
                    print('KeyError: property_name ->', property_name, '<- not found in property_dict.')
                    raise KeyError
        return property_dict

    # Remove duplicate, clashing aliases from property_alias_dict.
    def set_clashing_aliases(self, property_dict=None):
        clone_dict = property_dict
        self.clashing_alias_dict = {}
        for key1, alias_set1 in property_dict.items():
            for key2, alias_set2 in clone_dict.items():
                intersection = alias_set1.intersection(alias_set2)
                if len(intersection) > 0 and key1 != key2:                  # prevent direct comparison of the same key.
                    try:
                        self.clashing_alias_dict[key1] = self.clashing_alias_dict[key1].union(intersection)
                    except KeyError:
                        self.clashing_alias_dict[key1] = intersection
        # print('clashing aliases', self.clashing_alias_dict)

    @staticmethod
    def remove_clashing_aliases(property_dict=None, clashing_alias_dict=None):
        clean_dict = deepcopy(property_dict)
        for property_name in property_dict:
            try:
                clashing_aliases = clashing_alias_dict[property_name]
                for clashing_alias in clashing_aliases:
                    if clashing_alias in property_dict[property_name]:      # If clashing_alias found.
                        clean_dict[property_name].remove(clashing_alias)    # Remove it.
            except KeyError:
                pass
        # print('clashing aliases removed', clean_dict)
        return clean_dict

    # Builds a property_alias_dict using the following steps:
    # Initialize,
    # Merge with custom_property_alias_dict to allow integration of user defined aliases.
    # Get Clashing Aliases.
    # Remove Clashing Aliases.
    def build_property_alias_dict(self):
        _dict = self.initialize_property_alias_dict(property_names=self.property_names)                     # Initialize
        _dict = self.merge_dicts(property_dict=_dict, custom_dict=self.custom_property_alias_dict)          # Merge
        self.set_clashing_aliases(property_dict=_dict)                                                      # Get Clash
        _dict = self.remove_clashing_aliases(_dict, self.clashing_alias_dict)                               # Fix Clash
        return _dict

    # Convert a dictionary into a markdown formatted 2-column table.
    # key_title | value_title
    # --- | ---
    # key[0] | value
    # key[1] | value
    # TODO: Experiment with ```css\n key | value \n```
    @staticmethod
    def dict_to_markdown(key_title='', value_title='', _dict=None):
        _markdown = u'| ' + key_title + u' | ' + value_title + u' |\n| --- | --- |\n'   # Header plus second row.
        for key, value in _dict.items():
            value_str = ''
            if isinstance(value, set):
                for v in value:
                    value_str += u"`" + v + u"` "
            _markdown += u'| ' + key + u' | ' + str(value_str) + u' |\n'                # Key | Value row(s).
        return _markdown

    # Convert a dictionary into an HTML formatted 2-column table.
    # Format:
    # <html>
    #   <head><link rel="stylesheet" type="text/css" href="/css/blowdry.min.css" /></head>
    #
    #   <body>
    #       <table>
    #           <thead>
    #               <tr>
    #                   <th>key_title</th>
    #                   <th>value_title</th>
    #               </tr>
    #           </thead>
    #
    #           <tbody>
    #               <tr>
    #                   <td>key[0]</td>
    #                   <td>value</td>
    #               </tr>
    #           </tbody>
    #       </table>
    #   </body>
    # </html>
    @staticmethod
    def dict_to_html(key_title='', value_title='', _dict=None):
        common_classes = u' padding-5 border-1px-solid-gray display-inline '
        alternating_bg = u' bgc-hf8f8f8 '
        _html = str(
            '<html>\n' +
            '\t<head>\n' +
            '\t\t<meta charset="UTF-8">\n' +
            '\t\t<link rel="icon" type="image/x-icon" href="/images/favicon.ico">\n' +
            '\t\t<title>' + value_title + ' - blowdrycss</title>\n' +
            '\t\t<link rel="stylesheet" type="text/css" href="/css/blowdry.min.css" />\n' +
            '\t</head>\n\n' +
            '\t<body>\n' +
            '\t\t<table>\n' +
            '\t\t\t<tbody>\n'
            '\t\t\t\t<tr>\n' +
            '\t\t\t\t\t<td class="' + common_classes + 'talign-center bold">' + key_title + u'</td>\n' +
            '\t\t\t\t\t<td class="' + common_classes + 'talign-center bold">' + value_title + u'</td>\n' +
            '\t\t\t\t</tr>\n'
        )
        count = 1
        for key, value in _dict.items():
            classes = (common_classes + alternating_bg) if count % 2 == 0 else common_classes   # Alternate Style
            value_str = u''
            _html += u'\t\t\t\t<tr>\n'                                                          # Open Key | Value row.
            if isinstance(value, set):
                vcount = 1
                for v in value:
                    value_str += u"<code>" + v + u"</code>&emsp;"
                    value_str += u'<br>' if vcount % 5 == 0 else u''
                    vcount += 1
            _html += str(
                '\t\t\t\t\t<td class="' + classes + '">' + key + '</td>\n' +
                '\t\t\t\t\t<td class="' + classes + '">' + str(value_str) + '</td>\n'
                '\t\t\t\t</tr>\n'                                                               # Close Key | Value row.
            )
            count += 1
        _html += str(
            '\t\t\t</tbody>\n' +
            '\t\t</table>\n' +
            '\t</body>\n' +
            '</html>\n'
        )
        return _html


# DataLibrary() is not intended for use outside of this file as each time its' called it rebuilds some dictionaries.
__data_library = DataLibrary()

############################################
# Only variables intended for outside use. #
############################################

# Dictionaries
property_regex_dict = __data_library.property_regex_dict
property_alias_dict = __data_library.property_alias_dict
ordered_property_dict = __data_library.ordered_property_dict

# Markdown
clashing_alias_markdown = __data_library.clashing_alias_markdown
property_alias_markdown = __data_library.property_alias_markdown

# HTML
clashing_alias_html = __data_library.clashing_alias_html
property_alias_html = __data_library.property_alias_html

