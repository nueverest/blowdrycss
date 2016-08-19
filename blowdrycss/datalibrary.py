# python 2.7
from __future__ import absolute_import, unicode_literals
from builtins import str
# builtins
from collections import OrderedDict
from copy import deepcopy
import logging
# plugins
from pypandoc import convert
# custom
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class DataLibrary(object):
    """
    DataLibrary is not intended for use outside of this file as each time its' called it rebuilds the dictionaries.

    **Attributes:**

    | **property_regex_dict** (*dict*)

        A regex dictionary for detecting more complex value patterns for a given property.

        **Dictionary Contains:**

        - The ``key`` is the official CSS property name.
        - The ``value`` is a ``set()`` of regex strings.

        **Regexes Cases:**

        - Hexidecimal (3 digit) -- 'h123', 'h123 bold', 'underline h123 bold'
        - Hexidecimal (6 digit) -- 'h123456', 'h123456 underline', 'underline h123456 bold'
        - Hexidecimal (3 digit + pseudo-class + importance designator) -- 'h123-hover-i', 'h123-after-i bold',
        - Hexidecimal (6 digit + pseudo-class + importance designator) -- 'h12ad56-hover-i', 'h12AD56-hover-i underline'
        - Hexidecimal (3 digit + importance designator + pseudo-class) -- 'h1f3-i-hover', 'h1F3-i-hover bold'
        - Hexidecimal (6 digit + importance designator + pseudo-class) -- 'h123456-i-hover', 'h123456-i-hover underline'

        - Hexidecimal Regex explained
            - ``r"(h[0-9a-fA-F]{3} ?)$"`` or ``r"(h[0-9a-fA-F]{6} ?)$"``
            - ``h`` -- The substring must begin with an ``h``.
            - ``[0-9a-fA-F]`` -- The characters that follow must be a hexidecimal characters.
            - ``{3}`` or ``{6}`` -- Limit the number of hexidecimal characters to either 3 or 6 only.
            - ``' ?'`` -- The substring may optionally be followed by a space.

    | **property_value_as_alias_dict** (*dict*)

      Maps valid, unique W3C CSS property values to a W3C CSS property name. This enables the use of unique
      property values as standalone class selectors i.e. ``bold`` can be used in place of ``font-weight-bold``.
      This makes the syntax succinct while remaining declarative.

      **Rules:**

      - The property value alias must be unique across all valid W3C defined property values.
      - The property value alias must be unique across all property values defined in the dictionary.
      - The ``key`` is the official CSS property name.
      - The ``value`` is a ``set()`` of valid, unique W3C CSS property values.

      **Example:** ::

        ``'font-weight': {'bold', 'bolder', 'lighter', },``

      `Allowed values <https://www.w3.org/TR/CSS21/fonts.html#propdef-font-weight>`__ for font-weight according to W3C.
      Based on the standard ``normal`` is a valid property value.
      However, ``normal`` is not unique to ``font-weight``. To verify that
      `go here <https://www.w3.org/TR/CSS21/propidx.html>`__ and search for ``normal``.
      Also, ``100 - 900`` are listed as valid values, but CSS class selectors cannot begin with a digit.
      This implies that the numeric values cannot be included.  That leaves ``bold, bolder, and lighter``.

    | **property_names** (*set*)

        The set of all CSS 2.1 property names listed here: http://www.w3.org/TR/CSS21/propidx.html on the W3C website.

    | **clashing_alias_dict** (*dict*)

      Auto-generated dictionary of clashing aliases.  An alias clashes if it exactly equals an
      alias associated with another property e.g. One alias for ``border-right`` is ``'br-'``.
      However ``background-repeat`` has an identical alias of ``'br-'``. Therefore ``'br-'`` is added to
      ``clashing_alias_dict`` and is not allowed to be used as an alias.

      **Dictionary Contains:**

      - The ``key`` is the official CSS property name.
      - The ``value`` is a ``set()`` of custom string aliases.

    | **property_alias_dict** (*dict*)

        Auto-generated dictionary of property aliases.

        *Dictionary Contains:*

        - The ``key`` is the official CSS property name.
        - The ``value`` is a ``set()`` of custom string aliases.

    | **alphabetical_clashing_dict** (*dict*)

        Alphabetized ordered dictionary of clashing aliases.

        **Ordered Dictionary Contains:**

        - The ``key`` is the official CSS property name.
        - The ``value`` is a ``set()`` of clashing string aliases.

    | **alphabetical_property_dict** (*dict*)

        Alphabetized ordered dictionary of property aliases.

        *Ordered Dictionary Contains:*

        - The ``key`` is the official CSS property name.
        - The ``value`` is a ``set()`` of custom string aliases.

    | **clashing_alias_markdown** (*str*) -- Auto-generated table of clashing aliases in markdown format.

    | **property_alias_markdown** (*str*) -- Auto-generated table of property names and aliases in markdown format.

    | **clashing_alias_html** (*str*) -- Auto-generated table of clashing aliases in HTML format.

    | **property_alias_html** (*str*) -- Auto-generated table of property names and aliases in HTML format.

    | **clashing_alias_rst** (*str*) -- Auto-generated table of clashing aliases in reStructuredText format.

    | **property_alias_rst** (*str*) -- Auto-generated table of property names and aliases in reStructuredText form.

    | **ordered_property_dict** (*dict*)

        Sorted property_alias_dict with the longest items first as the
        most verbose match is preferred i.e. If ``css_class == 'margin-top'``, then match the
        ``property_alias_dict`` key that starts with ``margin-top`` not ``margin``.

        *Ordered Dictionary Contains:*

        - The ``key`` is the official CSS property name.
        - The ``value`` is a ``set()`` of custom string aliases.

    """
    def __init__(self):
        self.property_regex_dict = {
            'color': {
                r"(h[0-9a-fA-F]{3} ?)$", r"(h[0-9a-fA-F]{6} ?)$",
                r"(h[0-9a-fA-F]{3}-i ?)$", r"(h[0-9a-fA-F]{6}-i ?)$",
                r"(h[0-9a-fA-F]{3}-.*? ?)$", r"(h[0-9a-fA-F]{6}-.* ?)$",
                r"(h[0-9a-fA-F]{3}-.*?-i ?)$", r"(h[0-9a-fA-F]{6}-.*-i ?)$",
                r"(h[0-9a-fA-F]{3}-i-.*? ?)$", r"(h[0-9a-fA-F]{6}-i-.*? ?)$",
            },
        }

        self.custom_property_alias_dict = settings.custom_property_alias_dict

        self.property_value_as_alias_dict = {
            'background-repeat': {'repeat', 'repeat-x', 'repeat-y', 'no-repeat', },
            'color': {
                # Special format cases
                'rgb', 'rgba', 'hsl', 'hsla',
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
                'yellow', 'yellowgreen',
            },
            'content': {'open-quote', 'close-quote', 'no-open-quote', 'no-close-quote', },
            'cursor': {'crosshair', 'default', 'pointer', 'move', 'e-resize', 'ne-resize', 'nw-resize', 'n-resize',
                       'se-resize', 'sw-resize', 's-resize', 'w-resize', 'text', 'wait', 'help', 'progress', },
            'direction': {'ltr', 'rtl'},
            'display': {'inline', 'block', 'flex', 'list-item', 'inline-block', 'inline-flex', 'run-in',
                        'table', 'inline-table', 'table-row-group',
                        'table-header-group', 'table-footer-group', 'table-row', 'table-column-group', 'table-column',
                        'table-cell', 'table-caption',
                        'xxsmall', 'xsmall', 'small', 'medium', 'large', 'xlarge', 'xxlarge',
                        'giant', 'xgiant', 'xxgiant', },
            'elevation': {'below', 'level', 'above', 'higher', 'lower', },
            'font-family': {'serif', 'georgia', 'palatino', 'times', 'cambria', 'didot', 'garamond', 'perpetua',
                            'rockwell', 'baskerville',
                            'sans-serif', 'arial', 'helvetica', 'gadget', 'cursive', 'impact', 'charcoal', 'tahoma',
                            'geneva', 'verdana', 'calibri', 'candara', 'futura', 'optima',
                            'monospace', 'courier', 'monaco', 'consolas',
                            'fantasy', 'copperplate', 'papyrus', },
            'font-style': {'italic', 'oblique', },
            'font-variant': {'small-caps', },
            'font-weight': {'bold', 'bolder', 'lighter', },
            'list-style-position': {'inside', 'outside', },
            'list-style-type': {'disc', 'circle', 'square', 'decimal', 'decimal-leading-zero', 'lower-roman',
                                'upper-roman', 'lower-greek', 'lower-latin', 'upper-latin', 'armenian',
                                'georgian', 'lower-alpha', 'upper-alpha', },
            'overflow': {'visible', 'hidden', 'scroll', },
            'pitch': {'x-low', 'low', 'high', 'x-high'},
            'play-during': {'mix', 'repeat', },
            'position': {'static', 'relative', 'absolute', },
            'speak-header': {'once', 'always'},
            'speak-numeral': {'digits', 'continuous', },
            'speak-punctuation': {'code', },
            'speak': {'spell-out', },
            'speech-rate': {'x-slow', 'slow', 'fast', 'x-fast', 'faster', 'slower', },
            'text-decoration': {'underline', 'overline', 'line-through', 'blink', },
            'text-transform': {'capitalize', 'uppercase', 'lowercase', },
            'unicode-bidi': {'embed', 'bidi-override', },
            'vertical-align': {'baseline', 'sub', 'super', 'middle', 'text-top', 'text-bottom', },
            'visibility': {'visible', 'hidden', 'collapse', },
            'volume': {'silent', 'x-soft', 'soft', 'loud', 'x-loud', },
        }

        self.property_names = {
            'all', 'align-items',
            'background', 'background-attachment', 'background-color', 'background-image',
            'background-position', 'background-repeat', 'border', 'border-bottom', 'border-bottom-color',
            'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-left',
            'border-left-color', 'border-left-style', 'border-left-width', 'border-right', 'border-right-color',
            'border-right-style', 'border-right-width', 'border-spacing', 'border-style', 'border-top',
            'border-radius', 'border-top-left-radius', 'border-top-right-radius', 'border-bottom-right-radius',
            'border-bottom-left-radius',
            'border-top-color', 'border-top-style', 'border-top-width', 'border-width', 'bottom',
            'caption-side', 'clear', 'clip', 'color', 'content', 'counter-increment', 'counter-reset', 'cue',
            'cue-after', 'cue-before', 'cursor', 'direction', 'display', 'elevation', 'empty-cells', 'float',
            'font', 'font-family', 'font-size', 'font-style', 'font-variant', 'font-weight', 'height', 'left',
            'letter-spacing', 'line-height', 'list-style', 'list-style-image', 'list-style-position',
            'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'max-height',
            'max-width', 'min-height', 'min-width', 'opacity', 'orphans', 'outline', 'outline-color', 'outline-style',
            'outline-width', 'overflow', 'padding', 'padding-bottom', 'padding-left', 'padding-right',
            'padding-top', 'page-break-after', 'page-break-before', 'page-break-inside', 'pause', 'pause-after',
            'pause-before', 'pitch', 'pitch-range', 'play-during', 'position', 'quotes', 'richness', 'right', 'speak',
            'speak-header', 'speak-numeral', 'speak-punctuation', 'speech-rate', 'stress', 'table-layout',
            'text-align', 'text-decoration', 'text-indent', 'text-shadow', 'text-transform', 'top', 'unicode-bidi',
            'vertical-align',
            'visibility', 'voice-family', 'volume', 'white-space', 'widows', 'width', 'word-spacing', 'z-index'
        }

        self.clashing_alias_dict = {}
        self.property_alias_dict = {}

        # Set clashing_alias_dict and property_alias_dict.
        self.autogen_property_alias_dict()  # Initialize property_alias_dict
        self.merge_dictionaries()           # Merge
        self.set_clashing_aliases()         # Set clashing_aliases_dict
        self.remove_clashing_aliases()      # Clean property_alias_dict by removing clashing aliases.

        # Alphabetical Property Dictionaries
        self.alphabetical_clashing_dict = OrderedDict(sorted(self.clashing_alias_dict.items(), key=lambda t: t[0]))
        self.alphabetical_property_dict = OrderedDict(sorted(self.property_alias_dict.items(), key=lambda t: t[0]))

        # Generate Markdown Files
        self.clashing_alias_markdown = self.dict_to_markdown(
            h1_text=str('Clashing Aliases'),
            key_title=str('Property Name'),
            value_title=str('Invalid Clashing Aliases'),
            _dict=self.alphabetical_clashing_dict
        )
        self.property_alias_markdown = self.dict_to_markdown(
            h1_text=str('Valid Property Aliases'),
            key_title=str('Property Name'),
            value_title=str('Valid Aliases'),
            _dict=self.alphabetical_property_dict
        )

        # Generate HTML Files
        self.clashing_alias_html = self.dict_to_html(
            h1_text=str('Invalid Clashing Aliases'),
            key_title=str('Property Name'),
            value_title=str('Clashing Aliases'),
            _dict=self.alphabetical_clashing_dict
        )
        self.property_alias_html = self.dict_to_html(
            h1_text=str('Valid Property Aliases'),
            key_title=str('Property Name'),
            value_title=str('Valid Aliases'),
            _dict=self.alphabetical_property_dict
        )

        # Generate reStructuredText
        clashing_html = self.clashing_alias_html.replace('&emsp;', '   ')                   # Remove 'tab'
        property_html = self.property_alias_html.replace('&emsp;', '   ')                   # Remove 'tab'
        self.clashing_alias_rst = convert(source=clashing_html, to=str('rst'), format=str('html'))
        self.property_alias_rst = convert(source=property_html, to=str('rst'), format=str('html'))

        # Debug
        logging.debug('\nproperty_alias_dict:\n' + str(self.property_alias_dict))
        logging.debug('\nclashing_alias_markdown:\n' + str(self.clashing_alias_markdown))
        logging.debug('\nclashing_alias_html:\n' + str(self.clashing_alias_html))
        logging.debug('\nproperty_alias_markdown:\n' + str(self.property_alias_markdown))

        self.ordered_property_dict = OrderedDict(
            sorted(self.property_alias_dict.items(), key=lambda t: len(t[0]), reverse=True)
        )

    @staticmethod
    def get_property_aliases(property_name=''):
        """
        Auto-generates and returns a set of aliases based on abbreviation patterns.

        **Rules:**

        - Property name does not contain a dash:
          {First three letters of property_name + ``'-'``}
        - Property name contains one dashes:

            | 1st word + 1st letter after dash + ``'-'``

            | 1st letter of 1st word + 1st letter of 2nd word + ``'-'``, (single dash case)

            | 1st letter of 1st word + 1st letter of 2nd word + 1st letter of 3rd word + ``'-'``, (double dash case)

        - Append dash '-' at the end of each abbreviation.
        - Do not abbreviate words less than or equal to 5 characters in length.

        **Examples:**

        ::

            property_name --> {...}

            color --> set()

            padding --> {'pad-'}

            margin-top --> {'margin-t-', 'mt-'}

            border-bottom-width --> {'border-b-width', 'bbw-'}

        :type property_name: str
        :param property_name: A CSS property name.
        :return: Return a set() of abbreviation patterns according to the rules defined above.

        """
        if len(property_name) <= 5:                                 # Do not abbreviate short words (<= 5 letters).
            return set()

        aliases = set()                                             # First three letters
        if '-' in property_name:                                    # First dash
            dash_index1 = property_name.index('-')
            suffix = property_name[dash_index1 + 1:]
            if '-' in suffix:                                       # Second dash (rare)
                dash_index2 = suffix.index('-')
                aliases.add(                                        # Three letter abbreviation
                    property_name[0] + property_name[dash_index1 + 1] + suffix[dash_index2 + 1] + '-'
                )
                aliases.add(property_name[:dash_index1 + 2] + '-' + suffix[dash_index2 + 1:] + '-')
            else:
                aliases.add(property_name[0] + property_name[dash_index1 + 1] + '-')
                aliases.add(property_name[:dash_index1 + 2] + '-')
        else:
            aliases.add(property_name[:3] + '-')
        return aliases

    # TODO: Ask cssutils guys about combining class names for matching properties.
    def autogen_property_alias_dict(self):
        """ Uses ``self.property_names`` to auto--generate a property aliases. Assigns the result to
        ``self.property_alias_dict``.

        **Note:** The dictionary may contain clashing aliases. More processing is required to remove them.

        """
        self.property_alias_dict = {}
        for property_name in self.property_names:
            abbreviations = self.get_property_aliases(property_name=property_name)
            value = abbreviations
            self.property_alias_dict[property_name] = value

    def merge_dictionaries(self):
        """ Merges the ``property_alias_dict`` with ``property_value_as_alias_dict``.

        **Note:** All keys in both dictionaries much match.

        :raises KeyError: Raises KeyError if property name does not exist as a key in ``property_alias_dict``.

        """
        # Merge property values
        if self.property_value_as_alias_dict is not None:
            for property_name, alias_set in self.property_value_as_alias_dict.items():
                try:
                    self.property_alias_dict[property_name] = self.property_alias_dict[property_name].union(alias_set)
                except KeyError:
                    print('KeyError: property_name ->', property_name, '<- not found in property_alias_dict.')
                    raise KeyError
        # Merge user defined custom property aliases.
        if self.custom_property_alias_dict is not None:
            for property_name, alias_set in self.custom_property_alias_dict.items():
                try:
                    self.property_alias_dict[property_name] = self.property_alias_dict[property_name].union(alias_set)
                except KeyError:
                    print('KeyError: property_name ->', property_name, '<- not found in custom_property_alias_dict.')
                    raise KeyError

    def set_clashing_aliases(self):
        """ Searches ``property_alias_dict`` for duplicate / clashing aliases and adds them to ``clashing_alias_dict``.
        """
        clone_dict = self.property_alias_dict
        self.clashing_alias_dict = {}
        for key1, alias_set1 in self.property_alias_dict.items():
            for key2, alias_set2 in clone_dict.items():
                intersection = alias_set1.intersection(alias_set2)
                if len(intersection) > 0 and key1 != key2:                  # prevent direct comparison of the same key.
                    try:
                        self.clashing_alias_dict[key1] = self.clashing_alias_dict[key1].union(intersection)
                    except KeyError:
                        self.clashing_alias_dict[key1] = intersection
        logging.debug(msg='\ndatalibrary.clashing_aliases_dict:\n' + str(self.clashing_alias_dict))

    def remove_clashing_aliases(self):
        """ Removes clashing aliases stored in ``clashing_alias_dict`` from ``property_alias_dict`` and
        deep copies the clean dictionary to ``property_alias_dict``.

        """
        clean_dict = deepcopy(self.property_alias_dict)
        for property_name in self.property_alias_dict:
            try:
                clashing_aliases = self.clashing_alias_dict[property_name]
                for clashing_alias in clashing_aliases:
                    if clashing_alias in self.property_alias_dict[property_name]:    # If clashing_alias found.
                        clean_dict[property_name].remove(clashing_alias)             # Remove it.
            except KeyError:
                pass
        logging.debug(msg='Clashing aliases removed: datalibrary clean_dict\n' + str(clean_dict))
        self.property_alias_dict = deepcopy(clean_dict)

    @staticmethod
    def dict_to_markdown(h1_text='', key_title='', value_title='', _dict=None):
        """ Convert a dictionary into a markdown formatted 2-column table.

        *Markdown Table Format:*

        | ``# h1_text``

        | ``key_title | value_title``
        | ``--- | ---``
        | ``key[0] | value``
        | ``key[1] | value``

        :type h1_text: str
        :type key_title: str
        :type value_title: str
        :type _dict: dict

        :param h1_text: Title for the table.
        :param key_title: Key name.
        :param value_title: Value stored at Key.
        :param _dict: A generic dictionary.
        :return: (str) -- Returns a markdown formatted 2-column table based on the key/value pairs in ``_dict``.

        """

        # H1 plus table header.
        _markdown = '# ' + h1_text + '\n\n' \
                    '| ' + key_title + ' | ' + value_title + ' |\n| --- | --- |\n'
        for key, value in _dict.items():
            value_str = ''
            if isinstance(value, set):
                for v in value:
                    value_str += "`" + v + "` "
            _markdown += '| ' + key + ' | ' + str(value_str) + ' |\n'                # Key | Value row(s).
        return _markdown

    @staticmethod
    def dict_to_html(h1_text= '', key_title='', value_title='', _dict=None):
        """ Convert a dictionary into an HTML formatted 2-column table.

        *HTML Table Format:*

        ::

            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="icon" type="image/x-icon" href="/images/favicon.ico" />
                    <title>value_title - blowdrycss</title>
                    <link rel="stylesheet" type="text/css" href="/css/blowdry.min.css"/>
                </head>
                <body>
                    <table>
                        <thead>
                            <tr>
                                <th>key_title</th>
                                <th>value_title</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>key[0]</td>
                                <td>value</td>
                            </tr>
                        </tbody>
                    </table>
                </body>
            </html>

        :type h1_text: str
        :type key_title: str
        :type value_title: str
        :type _dict: dict

        :param h1_text: Title for the table.
        :param key_title: Key name.
        :param value_title: Value stored at Key.
        :param _dict: A generic dictionary.
        :return: (str) -- Returns a HTML formatted 2-column table based on the key/value pairs in ``_dict``.

        """
        common_classes = ' padding-5 border-1px-solid-gray display-inline '
        alternating_bg = ' bgc-hf8f8f8 '
        _html = str(
            '<html>\n' +
            '\t<head>\n' +
            '\t\t<meta charset="UTF-8">\n' +
            '\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
            '\t\t<link rel="icon" type="image/x-icon" href="/images/favicon.ico" />\n' +
            '\t\t<title>' + value_title + ' - blowdrycss</title>\n' +
            '\t\t<link rel="stylesheet" type="text/css" href="/css/blowdry.min.css" />\n' +
            '\t</head>\n\n' +
            '\t<body>\n' +
            '\t\t<h1>' + h1_text + '</h1>\n' +
            '\t\t<table>\n' +
            '\t\t\t<tbody>\n'
            '\t\t\t\t<tr>\n' +
            '\t\t\t\t\t<td class="' + common_classes + 'talign-center bold">' + key_title + '</td>\n' +
            '\t\t\t\t\t<td class="' + common_classes + 'talign-center bold">' + value_title + '</td>\n' +
            '\t\t\t\t</tr>\n'
        )
        count = 1
        for key, value in _dict.items():
            classes = (common_classes + alternating_bg) if count % 2 == 0 else common_classes   # Alternate Style
            value_str = ''
            _html += '\t\t\t\t<tr>\n'                                                          # Open Key | Value row.
            if isinstance(value, set):
                vcount = 1
                for v in value:
                    value_str += "<code>" + v + "</code>&emsp;"
                    value_str += '<br>' if vcount % 5 == 0 else ''
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

# Pseudo Sets - reference: http://www.w3schools.com/css/css_pseudo_classes.asp

# The following pseudo classes are not implemented due to complexity and verbosity.
# 'lang([a-zA-Z\-])',
# 'not(_[a-zA-Z0-9]\-)', 'nth-child([0-9])', 'nth-last-child([0-9])',
# 'nth-last-of-type([0-9])', 'nth-of-type([0-9])',
pseudo_classes = {
    'active', 'checked', 'disabled', 'empty', 'enabled', 'first-child', 'first-of-type', 'focus', 'hover',
    'in-range', 'invalid', 'last-child', 'last-of-type', 'link', 'only-child',
    'optional', 'out-of-range', 'read-only', 'read-write', 'required', 'root', 'target', 'valid', 'visited',
}
pseudo_elements = {'after', 'before', 'first-letter', 'first-line', 'selection', }

# Markdown
clashing_alias_markdown = __data_library.clashing_alias_markdown
property_alias_markdown = __data_library.property_alias_markdown

# HTML
clashing_alias_html = __data_library.clashing_alias_html
property_alias_html = __data_library.property_alias_html

# reStructuredTest
clashing_alias_rst = __data_library.clashing_alias_rst
property_alias_rst = __data_library.property_alias_rst

