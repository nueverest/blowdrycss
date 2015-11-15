from collections import OrderedDict
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# TODO: create function that validates dictionary ensuring that no aliases clash.
# TODO: move this to a CSV file and autogenerate this dictionary from CSV.
# Dictionary contains:
#   css property name as 'keys'
#   list of aliases as 'values' - An alias can be shorthand for the property name.
old_property_alias_dict = {
    'background-color': ['bgc-', 'bg-c-', 'bg-color-', ],
    'color': ['c-', ],
    'font-size': ['fsize-', 'f-size-', 'fs-', ],
    'font-weight': ['normal', 'bold', 'bolder', 'lighter', 'initial', 'fweight-', 'f-weight-', 'fw-', ],
    'height': ['h-', ],
    'margin': ['m-', ],
    'margin-top': ['m-top-', 'mt-', ],
    'padding': ['p-', ],
    'padding-top': ['p-top-', 'pt-', ],
    'text-align': ['talign-', 't-align-', ],
    'vertical-align': ['valign-', 'v-align-', ],
    'width': ['w-', ],
}

full_property_value_dict = {
    'azimuth': "<angle> | [[ left-side | far-left | left | center-left | center | center-right | right | far-right | right-side ] || behind ] | leftwards | rightwards | inherit",
    'background-attachment': "scroll | fixed | inherit",
    'background-color': "<color> | transparent | inherit",
    'background-image': "<uri> | none | inherit",
    'background-position': "[[ <percentage> | <length> | left | center | right ] [<percentage> | <length> | top | center | bottom ]? ] | [[ left | center | right ] || [ top | center | bottom ] ] | inherit",
    'background-repeat': "	repeat | repeat-x | repeat-y | no-repeat | inherit",
    'background': "['background-color' || 'background-image' || 'background-repeat' || 'background-attachment' || 'background-position'] | inherit",
    'border-collapse': "collapse | separate | inherit",
    'border-color': "<color> | transparent ]{1,4} | inherit",
    'border-spacing': "<length> <length>? | inherit",
    'border-style': "<border-style>{1,4} | inherit",
    'border-top': "<border-width> || <border-style> || '],'border-top-color' ] |inherit",
    'border-right': "<border-width> || <border-style> || '],'border-top-color' ] |inherit",
    'border-bottom': "<border-width> || <border-style> || '],'border-top-color' ] |inherit",
    'border-left': "<border-width> || <border-style> || '],'border-top-color' ] |inherit",
    'border-top-color': "<color> | transparent | inherit",
    'border-right-color': "<color> | transparent | inherit",
    'border-bottom-color': "<color> | transparent | inherit",
    'border-left-color': "<color> | transparent | inherit",
    'border-top-style': "<border-style> | inherit",
    'border-right-style': "<border-style> | inherit",
    'border-bottom-style': "<border-style> | inherit",
    'border-left-style': "<border-style> | inherit",
    'border-top-width': "<border-style> | inherit",
    'border-right-width': "<border-style> | inherit",
    'border-bottom-width': "<border-style> | inherit",
    'border-left-width': "<border-width> | inherit",
    'border-width': "<border-width>{1,4} | inherit",
    'border': "<border-width> || <border-style> || 'border-top-color' ] |inherit",
    'bottom': "<length> | <percentage> | auto | inherit",
    'caption-side': "top | bottom | inherit",
    'clear': "none | left | right | both | inherit",
    'clip': "<shape> | auto | inherit",
    'color': "<color> | inherit",
    'content': "normal | none | [ <string> | <uri> | <counter> | attr(<identifier>) | open-quote | close-quote | no-open-quote | no-close-quote ]+ | inherit",
    'counter-increment': "<identifier> <integer>? ]+ | none | inherit",
    'counter-reset': "<identifier> <integer>? ]+ | none | inherit",
    'cue-after': "<uri> | none | inherit",
    'cue-before': "<uri> | none | inherit",
    'cue': "[ 'cue-before' || 'cue-after' ] | inherit",
    'cursor': "[ [<uri> ,]* [ auto | crosshair | default | pointer | move | e-resize | ne-resize | nw-resize | n-resize | se-resize | sw-resize | s-resize | w-resize | text | wait | help | progress ] ] | inherit",
    'direction': "	ltr | rtl | inherit",
    'display': "inline | block | list-item | inline-block | table | inline-table | table-row-group | table-header-group | table-footer-group | table-row | table-column-group | table-column | table-cell | table-caption | none | inherit",
    'elevation': "<angle> | below | level | above | higher | lower | inherit",
    'empty-cells': "show | hide | inherit",
    'float': "left | right | none | inherit",
    'font-family': "[[ <family-name> | <generic-family> ] [, <family-name>|<generic-family>]* ] | inherit",
    'font-size': "<absolute-size> | <relative-size> | <length> |<percentage> | inherit",
    'font-style': "normal | italic | oblique | inherit",
    'font-variant': "normal | small-caps | inherit",
    'font-weight': "normal | bold | bolder | lighter | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | inherit",
    'font': "[ [ 'font-style' || 'font-variant' || 'font-weight' ]? 'font-size' [ /'line-height' ]? 'font-family' ] | caption | icon | menu | message-box | small-caption | status-bar | inherit",
    'height': "<length> | <percentage> | auto | inherit",
    'left': "<length> | <percentage> | auto | inherit",
    'letter-spacing': "normal | <length> | inherit",
    'line-height': "normal | <number> | <length> | <percentage> | inherit",
    'list-style-image': "<uri> | none | inherit",
    'list-style-position': "inside | outside | inherit",
    'list-style-type': "disc | circle | square | decimal | decimal-leading-zero | lower-roman | upper-roman | lower-greek | lower-latin | upper-latin | armenian | georgian | lower-alpha | upper-alpha | none | inherit",
    'list-style': "[ 'list-style-type' || 'list-style-position' || 'list-style-image' ] |inherit",
    'margin-right': "<margin-width> | inherit",
    'margin-left': "<margin-width> | inherit",
    'margin-top': "<margin-width> | inherit",
    'margin-bottom': "<margin-width> | inherit",
    'margin': "<margin-width>{1,4} | inherit",
    'max-height': "<length> | <percentage> | none | inherit",
    'max-width': "<length> | <percentage> | none | inherit",
    'min-height': "<length> | <percentage> | inherit",
    'min-width': "<length> | <percentage> | inherit",
    'orphans': "<integer> | inherit",
    'outline-color': "<color> | invert | inherit",
    'outline-style': "<border-style> | inherit",
    'outline-width': "<border-width> | inherit",
    'outline': "[ 'outline-color' || 'outline-style' || 'outline-width' ] | inherit",
    'overflow': "visible | hidden | scroll | auto | inherit",
    'padding-top': "<padding-width> | inherit",
    'padding-right': "<padding-width> | inherit",
    'padding-bottom': "<padding-width> | inherit",
    'padding-left': "<padding-width> | inherit",
    'padding': "<padding-width>{1,4} | inherit",
    'page-break-after': "auto | always | avoid | left | right | inherit",
    'page-break-before': "auto | always | avoid | left | right | inherit",
    'page-break-inside': "avoid | auto | inherit",
    'pause-after': "<time> | <percentage> | inherit",
    'pause-before': "<time> | <percentage> | inherit",
    'pause': "[ [<time> | <percentage>]{1,2} ] | inherit",
    'pitch-range': "<number> | inherit",
    'pitch': "<frequency> | x-low | low | medium | high | x-high | inherit",
    'play-during': "<uri> [ mix || repeat ]? | auto | none | inherit",
    'position': "static | relative | absolute | fixed | inherit",
    'quotes': "<string> <string>]+ | none | inherit",
    'richness': "<number> | inherit",
    'right': "<length> | <percentage> | auto | inherit",
    'speak-header': "once | always | inherit",
    'speak-numeral': "digits | continuous | inherit",
    'speak-punctuation': "code | none | inherit",
    'speak': "normal | none | spell-out | inherit",
    'speech-rate': "<number> | x-slow | slow | medium | fast | x-fast | faster | slower | inherit",
    'stress': "<number> | inherit",
    'table-layout': "auto | fixed | inherit",
    'text-align': "left | right | center | justify | inherit",
    'text-decoration': "none | [ underline || overline || line-through || blink ] |inherit",
    'text-indent': "<length> | <percentage> | inherit",
    'text-transform': "capitalize | uppercase | lowercase | none | inherit",
    'top': "<length> | <percentage> | auto | inherit",
    'unicode-bidi': "normal | embed | bidi-override | inherit",
    'vertical-align': "baseline | sub | super | top | text-top | middle | bottom | text-bottom | <percentage> | <length> | inherit",
    'visibility': "visible | hidden | collapse | inherit",
    'voice-family': "[[<specific-voice> | <generic-voice> ],]* [<specific-voice>| <generic-voice> ] | inherit",
    'volume': "<number> | <percentage> | silent | x-soft | soft | medium | loud | x-loud | inherit",
    'white-space': "normal | pre | nowrap | pre-wrap | pre-line | inherit",
    'widows': "<integer> | inherit",
    'width': "<length> | <percentage> | auto | inherit",
    'word-spacing': "normal | <length> | inherit",
    'z-index': "auto | <integer> | inherit",
}


# Remove unwanted strings from value string
def clean_value_string(value=''):
    remove_these_strings = [
        '<length>', '<percentage>', '<angle>', '<time>', '<frequency>', '<number>', '<integer>', '<specific-voice>',
        '<generic-voice>', '<uri>', '<color>', '<border-style>', '<border-width>', '<padding-width>', '<identifier>',
        '<shape>', '<margin-width>', '<family-name>', '<generic-family>', '<string>', '<counter>', '<absolute-size>',
        '<relative-size>',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '|', '[', ']', '{', '}', '?', ',', '/', 'inherit', '+',
        '(', ')', '*', 'attr',
        "'background-color'", "'background-image'", "'background-repeat'", "'background-attachment'",
        "'background-position'", "'border-top-color'", "'font-style'", "'font-variant'", "'font-weight'", "'font-size'",
        "'line-height'", "'font-family'", "'list-style-type'", "'list-style-position'", "'list-style-image'"
    ]
    for _str in remove_these_strings:
        value = value.replace(_str, '')
    return value


# Return abbreviation patterns.
# No dash: [First three leters]
# Multi-dash: [First word + First letter after dash, (single, double, triple letter zen css code)]
# Append dash '-' at the end of each abbreviation.
# Do not abbreviate words less than or equal to 5 characters in length.
#
# The zen css code comes from concatenating the first letter of the string with the first letter after each dash.
# e.g. 'border-top-width' --> 'btw-'
#
# Examples
# 'border-bottom-width' --> ['border-b-width', 'bbw-']
#             'padding' --> ['pad-']
#          'margin-top' --> ['margin-t-', 'mt-']
#               'color' --> ['']
def get_abbreviated_property_names(property_name=''):
    if len(property_name) <= 5:                                 # Do not abbreviate short words.
        return ['']

    abbreviations = []                                          # First three letters
    if '-' in property_name:                                    # First dash
        dash_index1 = property_name.index('-')
        suffix = property_name[dash_index1 + 1:]
        if '-' in suffix:                                       # Second dash (rare)
            dash_index2 = suffix.index('-')
            abbreviations.append(                               # Three letter abbreviation
                property_name[0] + property_name[dash_index1 + 1] + suffix[dash_index2 + 1] + '-'
            )
            abbreviations.append(property_name[:dash_index1 + 2] + '-' + suffix[dash_index2 + 1:] + '-')
        else:
            abbreviations.append(property_name[0] + property_name[dash_index1 + 1] + '-')
            abbreviations.append(property_name[:dash_index1 + 2] + '-')
    else:
        abbreviations.append(property_name[:3] + '-')
    return abbreviations


# TODO: Ask cssutils guys about combining class names for matching properties.

# Takes property value dictionary of the form.
# Key   = Property Name
# Value = String Representation of W3C Full Property Table "Value" column entry. http://www.w3.org/TR/CSS21/propidx.html
def create_property_alias_dict(property_value_dict=None):
    alias_dict = {}

    for key, value in property_value_dict.items():
        abbreviations = get_abbreviated_property_names(property_name=key)
        #value = clean_value_string(value=value)                            # Values typically do not make good aliases.
        value = abbreviations                                               # + value.split()
        alias_dict[key] = value
    return alias_dict


property_alias_dict = create_property_alias_dict(property_value_dict=full_property_value_dict)


# property_names with special types e.g. <angle>, <color>, <length>, etc.
# If no special types apply the value is set to <none> and the line is commented out.
# If the property_name is a shorthand property the value is set to <shorthand> and commented out.
properties_and_special_types_dict = {
    'azimuth': ["<angle>", ],
    # 'background-attachment': ["<none>", ],
    'background-color': ["<color>", ],
    'background-image': ["<uri>", ],
    'background-position': ["<percentage>", "<length>", ],
    # 'background-repeat': ["<none>", ],
    # 'background': ["<shorthand>", ],
    # 'border-collapse': ["<none>", ],
    'border-color': ["<color>", ],
    'border-spacing': ["<length>", ],
    'border-style': ["<border-style>", ],
    'border-top': ["<border-width>", "<border-style>", ],
    'border-right': ["<border-width>", "<border-style>", ],
    'border-bottom': ["<border-width>", "<border-style>", ],
    'border-left': ["<border-width>", "<border-style>", ],
    'border-top-color': ["<color>", ],
    'border-right-color': ["<color>", ],
    'border-bottom-color': ["<color>", ],
    'border-left-color': ["<color>", ],
    'border-top-style': ["<border-style>", ],
    'border-right-style': ["<border-style>", ],
    'border-bottom-style': ["<border-style>", ],
    'border-left-style': ["<border-style>", ],
    'border-top-width': ["<border-style>", ],
    'border-right-width': ["<border-style>", ],
    'border-bottom-width': ["<border-style>", ],
    'border-left-width': ["<border-width>", ],
    'border-width': ["<border-width>", ],
    'border': ["<border-width>", "<border-style>", ],
    'bottom': ["<length>", "<percentage>", ],
    # 'caption-side': ["<none>", ],
    # 'clear': ["<none>", ],
    'clip': ["<shape>", ],
    'color': ["<color>", ],
    # 'content': ["<shorthand>, <string>", "<uri>", "<counter>", "<identifier>", ],
    'counter-increment': ["<identifier>", "<integer>", ],
    'counter-reset': ["<identifier>", "<integer>", ],
    'cue-after': ["<uri>", ],
    'cue-before': ["<uri>", ],
    # 'cue': ["<none>", ],
    'cursor': ["<uri>", ],
    # 'direction': ["<none>", ],
    # 'display': ["<none>", ],
    'elevation': ["<angle>", ],
    # 'empty-cells': ["<none>", ],
    # 'float': ["<none>", ],
    'font-family': ["<family-name>", "<generic-family>", ],
    'font-size': ["<absolute-size>", "<relative-size>", "<length>", "<percentage>", ],
    # 'font-style': ["<none>", ],
    # 'font-variant': ["<none>", ],
    # 'font-weight': ["<none>", ],
    # 'font': ["<shorthand>", ],
    'height': ["<length>", "<percentage>", ],
    'left': ["<length>", "<percentage>", ],
    'letter-spacing': ["<length>", ],
    'line-height': ["<number>", "<length>", "<percentage>", ],
    'list-style-image': ["<uri>", ],
    # 'list-style-position': ["<none>", ],
    # 'list-style-type': ["<none>", ],
    # 'list-style': ["<none>", ],
    'margin-right': ["<margin-width>", ],
    'margin-left': ["<margin-width>", ],
    'margin-top': ["<margin-width>", ],
    'margin-bottom': ["<margin-width>", ],
    'margin': ["<margin-width>", ],
    'max-height': ["<length>", "<percentage>", ],
    'max-width': ["<length>", "<percentage>", ],
    'min-height': ["<length>", "<percentage>", ],
    'min-width': ["<length>", "<percentage>", ],
    'orphans': ["<integer>", ],
    'outline-color': ["<color>", ],
    'outline-style': ["<border-style>", ],
    'outline-width': ["<border-width>", ],
    # 'outline': ["<shorthand>", ],
    # 'overflow': ["<none>", ],
    'padding-top': ["<padding-width>", ],
    'padding-right': ["<padding-width>", ],
    'padding-bottom': ["<padding-width>", ],
    'padding-left': ["<padding-width>", ],
    'padding': ["<padding-width>", ],
    # 'page-break-after': ["<none>", ],
    # 'page-break-before': ["<none>", ],
    # 'page-break-inside': ["<none>", ],
    'pause-after': ["<time>", "<percentage>", ],
    'pause-before': ["<time>", "<percentage>", ],
    'pause': ["<time>", "<percentage>", ],
    'pitch-range': ["<number>", ],
    'pitch': ["<frequency>", ],
    'play-during': ["<uri>", ],
    # 'position': ["<none>", ],
    'quotes': ["<string>", ],
    'richness': ["<number>", ],
    'right': ["<length>", "<percentage>", ],
    # 'speak-header': ["<none>", ],
    # 'speak-numeral': ["<none>", ],
    # 'speak-punctuation': ["<none>", ],
    # 'speak': ["<none>", ],
    'speech-rate': ["<number>", ],
    'stress': ["<number>", ],
    # 'table-layout': ["<none>", ],
    # 'text-align': ["<none>", ],
    # 'text-decoration': ["<none>", ],
    'text-indent': ["<length>", "<percentage>", ],
    # 'text-transform': ["<none>", ],
    'top': ["<length>", "<percentage>", ],
    # 'unicode-bidi': ["<none>", ],
    'vertical-align': ["<percentage>", "<length>", ],
    # 'visibility': ["<none>", ],
    'voice-family': ["<specific-voice>", "<generic-voice>", ],
    'volume': ["<number>", "<percentage>", ],
    'white-space': ["<none>", ],
    'widows': ["<integer>", ],
    'width': ["<length>", "<percentage>", ],
    'word-spacing': ["normal", "<length>", ],
    'z-index': ["<integer>", ],
}

# Sort property_alias_dict with the longest items first as the most verbose match is preferred.
# i.e. If css_class == 'margin-top' Then we want it to match the property_alias_dict key 'margin-top' not 'margin'
ordered_property_dict = OrderedDict(
    sorted(property_alias_dict.items(), key=lambda t: len(t[0]), reverse=True)
)

# This is not necessary cssutils already does regex validation see property.valid)
# allowed = self.allowed_unit_characters()
# self.property_alias_dict = {
#     'font-weight': [['normal', 'bold', 'bolder', 'lighter', 'initial', 'fw-'], r"([0-9a-z-])"],
#     'padding': [['p-'], r"([0-9" + allowed + "_-])"],
#     'height': [['h-'], r"([0-9" + allowed + "_-])"],
# }

# Reference: http://www.w3.org/TR/CSS21/propidx.html
special_type_units = {
    '<length>': ['px', 'em', 'rem', 'ex', 'cm', 'mm', 'in', 'pt', 'pc', 'ch', 'vh', 'vw', 'vmin', 'vmax', ],
    '<percentage>': ['p', '%', ],
    '<angle>': ['deg', 'grad', 'rad', ],
    '<time>': ['ms', 's', ],
    '<frequency>': ['Hz', 'kHz', ],
    # <number>, <integer>, <specific-voice>, <generic-voice>, <uri>, <color>, <border-style>, <border-width>,
    # <padding-width>, <identifier>, <shape>
}

# Reduces css_units to a minimum set of allowed characters.
# Used in property_alias_dict regex.
# Example: converts {'px', 'em', 'rem'} --> 'pxemr' thus eliminating duplicate 'e' and 'm'
# def allowed_unit_characters(self):
#     allowed = ''
#     for css_unit in self.css_units:
#         allowed += css_unit
#     return allowed

# Reference: http://www.w3.org/TR/CSS21/propidx.html
# Extracted all properties containing Values of <angle>, <percentage>, <length>, <time>, <frequency>
# IDEA: Build webscraper that auto-extracts these.\
default_property_units_dict = {       # Possible Occurrences:
    'azimuth': 'deg',                 # single
    'background-position': '%',       # single or double

    # 'border': 'px',                 # single   Shorthand Property unit addition Not implemented
    'border-top': 'px',               # single
    'border-right': 'px',             # single
    'border-bottom': 'px',            # single
    'border-left': 'px',              # single
    'border-spacing': 'px',           # single

    'border-width': 'px',             # single
    'border-top-width': 'px',         # single
    'border-right-width': 'px',       # single
    'border-bottom-width': 'px',      # single
    'border-left-width': 'px',        # single

    'elevation': 'deg',               # single

    # 'font': 'px',                   # single    Shorthand Property unit addition Not implemented
    'font-size': 'px',                # single

    'height': 'px',                   # single
    'max-height': 'px',               # single
    'min-height': 'px',               # single

    'letter-spacing': 'px',           # single
    'word-spacing': 'px',             # single

    'line-height': 'px',              # single

    'top': 'px',                      # single
    'right': 'px',                    # single
    'bottom': 'px',                   # single
    'left': 'px',                     # single

    'margin': 'px',                   # single, double, quadruple
    'margin-top': 'px',               # single
    'margin-right': 'px',             # single
    'margin-bottom': 'px',            # single
    'margin-left': 'px',              # single

    # 'outline': 'px',                # single    Shorthand Property unit addition Not implemented
    'outline-width': 'px',            # single

    'padding': 'px',                  # single, double, quadruple
    'padding-top': 'px',              # single
    'padding-right': 'px',            # single
    'padding-bottom': 'px',           # single
    'padding-left': 'px',             # single

    'pause': 'ms',                    # single, double
    'pause-after': 'ms',              # single
    'pause-before': 'ms',             # single

    'pitch': 'Hz',                    # single

    'text-indent': 'px',              # single

    'vertical-align': '%',            # single

    'volume': '%',                    # single

    'width': 'px',                    # single
    'max-width': 'px',                # single
    'min-width': 'px',                # single
}


# TODO: Review and possibly modify for the purposes of this library
# Zen CSS abbreviations
# Zen Coding Cheatsheet https://code.google.com/p/zen-coding/downloads/detail?name=ZenCodingCheatSheet.pdf
# Credit: Sergey Chikuyonok (serge.che@gmail.com)
# https://code.google.com/p/zen-coding/source/browse/branches/serge.che/python/zencoding/zen_settings.py
def get_zen_css_dict():
    return {
        "@i": "@import url(|);",
        "@m": "@media print {\n\t|\n}",
        "@f": "@font-face {\n\tfont-family:|;\n\tsrc:url(|);\n}",
        "!": "!important",
        "pos": "position:|;",
        "pos:s": "position:static;",
        "pos:a": "position:absolute;",
        "pos:r": "position:relative;",
        "pos:f": "position:fixed;",
        "t": "top:|;",
        "t:a": "top:auto;",
        "r": "right:|;",
        "r:a": "right:auto;",
        "b": "bottom:|;",
        "b:a": "bottom:auto;",
        "l": "left:|;",
        "l:a": "left:auto;",
        "z": "z-index:|;",
        "z:a": "z-index:auto;",
        "fl": "float:|;",
        "fl:n": "float:none;",
        "fl:l": "float:left;",
        "fl:r": "float:right;",
        "cl": "clear:|;",
        "cl:n": "clear:none;",
        "cl:l": "clear:left;",
        "cl:r": "clear:right;",
        "cl:b": "clear:both;",
        "d": "display:|;",
        "d:n": "display:none;",
        "d:b": "display:block;",
        "d:ib": "display:inline;",
        "d:li": "display:list-item;",
        "d:ri": "display:run-in;",
        "d:cp": "display:compact;",
        "d:tb": "display:table;",
        "d:itb": "display:inline-table;",
        "d:tbcp": "display:table-caption;",
        "d:tbcl": "display:table-column;",
        "d:tbclg": "display:table-column-group;",
        "d:tbhg": "display:table-header-group;",
        "d:tbfg": "display:table-footer-group;",
        "d:tbr": "display:table-row;",
        "d:tbrg": "display:table-row-group;",
        "d:tbc": "display:table-cell;",
        "d:rb": "display:ruby;",
        "d:rbb": "display:ruby-base;",
        "d:rbbg": "display:ruby-base-group;",
        "d:rbt": "display:ruby-text;",
        "d:rbtg": "display:ruby-text-group;",
        "v": "visibility:|;",
        "v:v": "visibility:visible;",
        "v:h": "visibility:hidden;",
        "v:c": "visibility:collapse;",
        "ov": "overflow:|;",
        "ov:v": "overflow:visible;",
        "ov:h": "overflow:hidden;",
        "ov:s": "overflow:scroll;",
        "ov:a": "overflow:auto;",
        "ovx": "overflow-x:|;",
        "ovx:v": "overflow-x:visible;",
        "ovx:h": "overflow-x:hidden;",
        "ovx:s": "overflow-x:scroll;",
        "ovx:a": "overflow-x:auto;",
        "ovy": "overflow-y:|;",
        "ovy:v": "overflow-y:visible;",
        "ovy:h": "overflow-y:hidden;",
        "ovy:s": "overflow-y:scroll;",
        "ovy:a": "overflow-y:auto;",
        "ovs": "overflow-style:|;",
        "ovs:a": "overflow-style:auto;",
        "ovs:s": "overflow-style:scrollbar;",
        "ovs:p": "overflow-style:panner;",
        "ovs:m": "overflow-style:move;",
        "ovs:mq": "overflow-style:marquee;",
        "zoo": "zoom:1;",
        "cp": "clip:|;",
        "cp:a": "clip:auto;",
        "cp:r": "clip:rect(|);",
        "bxz": "box-sizing:|;",
        "bxz:cb": "box-sizing:content-box;",
        "bxz:bb": "box-sizing:border-box;",
        "bxsh": "box-shadow:|;",
        "bxsh:n": "box-shadow:none;",
        "bxsh:w": "-webkit-box-shadow:0 0 0 #000;",
        "bxsh:m": "-moz-box-shadow:0 0 0 0 #000;",
        "m": "margin:|;",
        "m:a": "margin:auto;",
        "m:0": "margin:0;",
        "m:2": "margin:0 0;",
        "m:3": "margin:0 0 0;",
        "m:4": "margin:0 0 0 0;",
        "mt": "margin-top:|;",
        "mt:a": "margin-top:auto;",
        "mr": "margin-right:|;",
        "mr:a": "margin-right:auto;",
        "mb": "margin-bottom:|;",
        "mb:a": "margin-bottom:auto;",
        "ml": "margin-left:|;",
        "ml:a": "margin-left:auto;",
        "p": "padding:|;",
        "p:0": "padding:0;",
        "p:2": "padding:0 0;",
        "p:3": "padding:0 0 0;",
        "p:4": "padding:0 0 0 0;",
        "pt": "padding-top:|;",
        "pr": "padding-right:|;",
        "pb": "padding-bottom:|;",
        "pl": "padding-left:|;",
        "w": "width:|;",
        "w:a": "width:auto;",
        "h": "height:|;",
        "h:a": "height:auto;",
        "maw": "max-width:|;",
        "maw:n": "max-width:none;",
        "mah": "max-height:|;",
        "mah:n": "max-height:none;",
        "miw": "min-width:|;",
        "mih": "min-height:|;",
        "o": "outline:|;",
        "o:n": "outline:none;",
        "oo": "outline-offset:|;",
        "ow": "outline-width:|;",
        "os": "outline-style:|;",
        "oc": "outline-color:#000;",
        "oc:i": "outline-color:invert;",
        "bd": "border:|;",
        "bd+": "border:1px solid #000;",
        "bd:n": "border:none;",
        "bdbk": "border-break:|;",
        "bdbk:c": "border-break:close;",
        "bdcl": "border-collapse:|;",
        "bdcl:c": "border-collapse:collapse;",
        "bdcl:s": "border-collapse:separate;",
        "bdc": "border-color:#000;",
        "bdi": "border-image:url(|);",
        "bdi:n": "border-image:none;",
        "bdi:w": "-webkit-border-image:url(|) 0 0 0 0 stretch stretch;",
        "bdi:m": "-moz-border-image:url(|) 0 0 0 0 stretch stretch;",
        "bdti": "border-top-image:url(|);",
        "bdti:n": "border-top-image:none;",
        "bdri": "border-right-image:url(|);",
        "bdri:n": "border-right-image:none;",
        "bdbi": "border-bottom-image:url(|);",
        "bdbi:n": "border-bottom-image:none;",
        "bdli": "border-left-image:url(|);",
        "bdli:n": "border-left-image:none;",
        "bdci": "border-corner-image:url(|);",
        "bdci:n": "border-corner-image:none;",
        "bdci:c": "border-corner-image:continue;",
        "bdtli": "border-top-left-image:url(|);",
        "bdtli:n": "border-top-left-image:none;",
        "bdtli:c": "border-top-left-image:continue;",
        "bdtri": "border-top-right-image:url(|);",
        "bdtri:n": "border-top-right-image:none;",
        "bdtri:c": "border-top-right-image:continue;",
        "bdbri": "border-bottom-right-image:url(|);",
        "bdbri:n": "border-bottom-right-image:none;",
        "bdbri:c": "border-bottom-right-image:continue;",
        "bdbli": "border-bottom-left-image:url(|);",
        "bdbli:n": "border-bottom-left-image:none;",
        "bdbli:c": "border-bottom-left-image:continue;",
        "bdf": "border-fit:|;",
        "bdf:c": "border-fit:clip;",
        "bdf:r": "border-fit:repeat;",
        "bdf:sc": "border-fit:scale;",
        "bdf:st": "border-fit:stretch;",
        "bdf:ow": "border-fit:overwrite;",
        "bdf:of": "border-fit:overflow;",
        "bdf:sp": "border-fit:space;",
        "bdl": "border-length:|;",
        "bdl:a": "border-length:auto;",
        "bdsp": "border-spacing:|;",
        "bds": "border-style:|;",
        "bds:n": "border-style:none;",
        "bds:h": "border-style:hidden;",
        "bds:dt": "border-style:dotted;",
        "bds:ds": "border-style:dashed;",
        "bds:s": "border-style:solid;",
        "bds:db": "border-style:double;",
        "bds:dtds": "border-style:dot-dash;",
        "bds:dtdtds": "border-style:dot-dot-dash;",
        "bds:w": "border-style:wave;",
        "bds:g": "border-style:groove;",
        "bds:r": "border-style:ridge;",
        "bds:i": "border-style:inset;",
        "bds:o": "border-style:outset;",
        "bdw": "border-width:|;",
        "bdt": "border-top:|;",
        "bdt+": "border-top:1px solid #000;",
        "bdt:n": "border-top:none;",
        "bdtw": "border-top-width:|;",
        "bdts": "border-top-style:|;",
        "bdts:n": "border-top-style:none;",
        "bdtc": "border-top-color:#000;",
        "bdr": "border-right:|;",
        "bdr+": "border-right:1px solid #000;",
        "bdr:n": "border-right:none;",
        "bdrw": "border-right-width:|;",
        "bdrs": "border-right-style:|;",
        "bdrs:n": "border-right-style:none;",
        "bdrc": "border-right-color:#000;",
        "bdb": "border-bottom:|;",
        "bdb+": "border-bottom:1px solid #000;",
        "bdb:n": "border-bottom:none;",
        "bdbw": "border-bottom-width:|;",
        "bdbs": "border-bottom-style:|;",
        "bdbs:n": "border-bottom-style:none;",
        "bdbc": "border-bottom-color:#000;",
        "bdl": "border-left:|;",
        "bdl+": "border-left:1px solid #000;",
        "bdl:n": "border-left:none;",
        "bdlw": "border-left-width:|;",
        "bdls": "border-left-style:|;",
        "bdls:n": "border-left-style:none;",
        "bdlc": "border-left-color:#000;",
        "bdrs": "border-radius:|;",
        "bdtrrs": "border-top-right-radius:|;",
        "bdtlrs": "border-top-left-radius:|;",
        "bdbrrs": "border-bottom-right-radius:|;",
        "bdblrs": "border-bottom-left-radius:|;",
        "bg": "background:|;",
        "bg+": "background:#FFF url(|) 0 0 no-repeat;",
        "bg:n": "background:none;",
        "bg:ie": "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='|x.png');",
        "bgc": "background-color:#FFF;",
        "bgi": "background-image:url(|);",
        "bgi:n": "background-image:none;",
        "bgr": "background-repeat:|;",
        "bgr:n": "background-repeat:no-repeat;",
        "bgr:x": "background-repeat:repeat-x;",
        "bgr:y": "background-repeat:repeat-y;",
        "bga": "background-attachment:|;",
        "bga:f": "background-attachment:fixed;",
        "bga:s": "background-attachment:scroll;",
        "bgp": "background-position:0 0;",
        "bgpx": "background-position-x:|;",
        "bgpy": "background-position-y:|;",
        "bgbk": "background-break:|;",
        "bgbk:bb": "background-break:bounding-box;",
        "bgbk:eb": "background-break:each-box;",
        "bgbk:c": "background-break:continuous;",
        "bgcp": "background-clip:|;",
        "bgcp:bb": "background-clip:border-box;",
        "bgcp:pb": "background-clip:padding-box;",
        "bgcp:cb": "background-clip:content-box;",
        "bgcp:nc": "background-clip:no-clip;",
        "bgo": "background-origin:|;",
        "bgo:pb": "background-origin:padding-box;",
        "bgo:bb": "background-origin:border-box;",
        "bgo:cb": "background-origin:content-box;",
        "bgz": "background-size:|;",
        "bgz:a": "background-size:auto;",
        "bgz:ct": "background-size:contain;",
        "bgz:cv": "background-size:cover;",
        "c": "color:#000;",
        "tbl": "table-layout:|;",
        "tbl:a": "table-layout:auto;",
        "tbl:f": "table-layout:fixed;",
        "cps": "caption-side:|;",
        "cps:t": "caption-side:top;",
        "cps:b": "caption-side:bottom;",
        "ec": "empty-cells:|;",
        "ec:s": "empty-cells:show;",
        "ec:h": "empty-cells:hide;",
        "lis": "list-style:|;",
        "lis:n": "list-style:none;",
        "lisp": "list-style-position:|;",
        "lisp:i": "list-style-position:inside;",
        "lisp:o": "list-style-position:outside;",
        "list": "list-style-type:|;",
        "list:n": "list-style-type:none;",
        "list:d": "list-style-type:disc;",
        "list:c": "list-style-type:circle;",
        "list:s": "list-style-type:square;",
        "list:dc": "list-style-type:decimal;",
        "list:dclz": "list-style-type:decimal-leading-zero;",
        "list:lr": "list-style-type:lower-roman;",
        "list:ur": "list-style-type:upper-roman;",
        "lisi": "list-style-image:|;",
        "lisi:n": "list-style-image:none;",
        "q": "quotes:|;",
        "q:n": "quotes:none;",
        "q:ru": "quotes:'\00AB' '\00BB' '\201E' '\201C';",
        "q:en": "quotes:'\201C' '\201D' '\2018' '\2019';",
        "ct": "content:|;",
        "ct:n": "content:normal;",
        "ct:oq": "content:open-quote;",
        "ct:noq": "content:no-open-quote;",
        "ct:cq": "content:close-quote;",
        "ct:ncq": "content:no-close-quote;",
        "ct:a": "content:attr(|);",
        "ct:c": "content:counter(|);",
        "ct:cs": "content:counters(|);",
        "coi": "counter-increment:|;",
        "cor": "counter-reset:|;",
        "va": "vertical-align:|;",
        "va:sup": "vertical-align:super;",
        "va:t": "vertical-align:top;",
        "va:tt": "vertical-align:text-top;",
        "va:m": "vertical-align:middle;",
        "va:bl": "vertical-align:baseline;",
        "va:b": "vertical-align:bottom;",
        "va:tb": "vertical-align:text-bottom;",
        "va:sub": "vertical-align:sub;",
        "ta": "text-align:|;",
        "ta:l": "text-align:left;",
        "ta:c": "text-align:center;",
        "ta:r": "text-align:right;",
        "tal": "text-align-last:|;",
        "tal:a": "text-align-last:auto;",
        "tal:l": "text-align-last:left;",
        "tal:c": "text-align-last:center;",
        "tal:r": "text-align-last:right;",
        "td": "text-decoration:|;",
        "td:n": "text-decoration:none;",
        "td:u": "text-decoration:underline;",
        "td:o": "text-decoration:overline;",
        "td:l": "text-decoration:line-through;",
        "te": "text-emphasis:|;",
        "te:n": "text-emphasis:none;",
        "te:ac": "text-emphasis:accent;",
        "te:dt": "text-emphasis:dot;",
        "te:c": "text-emphasis:circle;",
        "te:ds": "text-emphasis:disc;",
        "te:b": "text-emphasis:before;",
        "te:a": "text-emphasis:after;",
        "th": "text-height:|;",
        "th:a": "text-height:auto;",
        "th:f": "text-height:font-size;",
        "th:t": "text-height:text-size;",
        "th:m": "text-height:max-size;",
        "ti": "text-indent:|;",
        "ti:-": "text-indent:-9999px;",
        "tj": "text-justify:|;",
        "tj:a": "text-justify:auto;",
        "tj:iw": "text-justify:inter-word;",
        "tj:ii": "text-justify:inter-ideograph;",
        "tj:ic": "text-justify:inter-cluster;",
        "tj:d": "text-justify:distribute;",
        "tj:k": "text-justify:kashida;",
        "tj:t": "text-justify:tibetan;",
        "to": "text-outline:|;",
        "to+": "text-outline:0 0 #000;",
        "to:n": "text-outline:none;",
        "tr": "text-replace:|;",
        "tr:n": "text-replace:none;",
        "tt": "text-transform:|;",
        "tt:n": "text-transform:none;",
        "tt:c": "text-transform:capitalize;",
        "tt:u": "text-transform:uppercase;",
        "tt:l": "text-transform:lowercase;",
        "tw": "text-wrap:|;",
        "tw:n": "text-wrap:normal;",
        "tw:no": "text-wrap:none;",
        "tw:u": "text-wrap:unrestricted;",
        "tw:s": "text-wrap:suppress;",
        "tsh": "text-shadow:|;",
        "tsh+": "text-shadow:0 0 0 #000;",
        "tsh:n": "text-shadow:none;",
        "lh": "line-height:|;",
        "whs": "white-space:|;",
        "whs:n": "white-space:normal;",
        "whs:p": "white-space:pre;",
        "whs:nw": "white-space:nowrap;",
        "whs:pw": "white-space:pre-wrap;",
        "whs:pl": "white-space:pre-line;",
        "whsc": "white-space-collapse:|;",
        "whsc:n": "white-space-collapse:normal;",
        "whsc:k": "white-space-collapse:keep-all;",
        "whsc:l": "white-space-collapse:loose;",
        "whsc:bs": "white-space-collapse:break-strict;",
        "whsc:ba": "white-space-collapse:break-all;",
        "wob": "word-break:|;",
        "wob:n": "word-break:normal;",
        "wob:k": "word-break:keep-all;",
        "wob:l": "word-break:loose;",
        "wob:bs": "word-break:break-strict;",
        "wob:ba": "word-break:break-all;",
        "wos": "word-spacing:|;",
        "wow": "word-wrap:|;",
        "wow:nm": "word-wrap:normal;",
        "wow:n": "word-wrap:none;",
        "wow:u": "word-wrap:unrestricted;",
        "wow:s": "word-wrap:suppress;",
        "lts": "letter-spacing:|;",
        "f": "font:|;",
        "f+": "font:1em Arial,sans-serif;",
        "fw": "font-weight:|;",
        "fw:n": "font-weight:normal;",
        "fw:b": "font-weight:bold;",
        "fw:br": "font-weight:bolder;",
        "fw:lr": "font-weight:lighter;",
        "fs": "font-style:|;",
        "fs:n": "font-style:normal;",
        "fs:i": "font-style:italic;",
        "fs:o": "font-style:oblique;",
        "fv": "font-variant:|;",
        "fv:n": "font-variant:normal;",
        "fv:sc": "font-variant:small-caps;",
        "fz": "font-size:|;",
        "fza": "font-size-adjust:|;",
        "fza:n": "font-size-adjust:none;",
        "ff": "font-family:|;",
        "ff:s": "font-family:serif;",
        "ff:ss": "font-family:sans-serif;",
        "ff:c": "font-family:cursive;",
        "ff:f": "font-family:fantasy;",
        "ff:m": "font-family:monospace;",
        "fef": "font-effect:|;",
        "fef:n": "font-effect:none;",
        "fef:eg": "font-effect:engrave;",
        "fef:eb": "font-effect:emboss;",
        "fef:o": "font-effect:outline;",
        "fem": "font-emphasize:|;",
        "femp": "font-emphasize-position:|;",
        "femp:b": "font-emphasize-position:before;",
        "femp:a": "font-emphasize-position:after;",
        "fems": "font-emphasize-style:|;",
        "fems:n": "font-emphasize-style:none;",
        "fems:ac": "font-emphasize-style:accent;",
        "fems:dt": "font-emphasize-style:dot;",
        "fems:c": "font-emphasize-style:circle;",
        "fems:ds": "font-emphasize-style:disc;",
        "fsm": "font-smooth:|;",
        "fsm:a": "font-smooth:auto;",
        "fsm:n": "font-smooth:never;",
        "fsm:aw": "font-smooth:always;",
        "fst": "font-stretch:|;",
        "fst:n": "font-stretch:normal;",
        "fst:uc": "font-stretch:ultra-condensed;",
        "fst:ec": "font-stretch:extra-condensed;",
        "fst:c": "font-stretch:condensed;",
        "fst:sc": "font-stretch:semi-condensed;",
        "fst:se": "font-stretch:semi-expanded;",
        "fst:e": "font-stretch:expanded;",
        "fst:ee": "font-stretch:extra-expanded;",
        "fst:ue": "font-stretch:ultra-expanded;",
        "op": "opacity:|;",
        "op:ie": "filter:progid:DXImageTransform.Microsoft.Alpha(Opacity=100);",
        "op:ms": "-ms-filter:'progid:DXImageTransform.Microsoft.Alpha(Opacity=100)';",
        "rz": "resize:|;",
        "rz:n": "resize:none;",
        "rz:b": "resize:both;",
        "rz:h": "resize:horizontal;",
        "rz:v": "resize:vertical;",
        "cur": "cursor:|;",
        "cur:a": "cursor:auto;",
        "cur:d": "cursor:default;",
        "cur:c": "cursor:crosshair;",
        "cur:ha": "cursor:hand;",
        "cur:he": "cursor:help;",
        "cur:m": "cursor:move;",
        "cur:p": "cursor:pointer;",
        "cur:t": "cursor:text;",
        "pgbb": "page-break-before:|;",
        "pgbb:au": "page-break-before:auto;",
        "pgbb:al": "page-break-before:always;",
        "pgbb:l": "page-break-before:left;",
        "pgbb:r": "page-break-before:right;",
        "pgbi": "page-break-inside:|;",
        "pgbi:au": "page-break-inside:auto;",
        "pgbi:av": "page-break-inside:avoid;",
        "pgba": "page-break-after:|;",
        "pgba:au": "page-break-after:auto;",
        "pgba:al": "page-break-after:always;",
        "pgba:l": "page-break-after:left;",
        "pgba:r": "page-break-after:right;",
        "orp": "orphans:|;",
        "wid": "widows:|;"
    }


_property_alias_dict = {
    'elevation': ['e-', 'ele-', 'elev-', '<angle>', '|', 'below', '|', 'level', '|', 'above', '|', 'higher', '|', 'lower', '|', 'inherit'],
    'font-size': ['f-', 'fon-', 'font-', '<absolute-size>', '|', '<relative-size>', '|', '<length>', '|<percentage>', '|', 'inherit'],
    'pause-before': ['p-', 'pau-', 'paus-', '<time>', '|', '<percentage>', '|', 'inherit'], 'font-family': ['f-', 'fon-', 'font-', '[[', '<family-name>', '|', '<generic-family>', ']', '[,', '<family-name>|<generic-family>]*', ']', '|', 'inherit'], 'list-style-position': ['l-', 'lis-', 'list-', 'inside', '|', 'outside', '|', 'inherit'], 'caption-side': ['c-', 'cap-', 'capt-', 'top', '|', 'bottom', '|', 'inherit'], 'border': ['b-', 'bor-', 'bord-', '<border-width>', '||', '<border-style>', '||', "'border-top-color'", ']', '|inherit'], 'pause': ['p-', 'pau-', 'paus-', '[', '[<time>', '|', '<percentage>]{1,2}', ']', '|', 'inherit'], 'clip': ['c-', 'cli-', 'clip-', '<shape>', '|', 'auto', '|', 'inherit'], 'background-image': ['b-', 'bac-', 'back-', '<uri>', '|', 'none', '|', 'inherit'], 'margin-left': ['m-', 'mar-', 'marg-', '<margin-width>', '|', 'inherit'], 'content': ['c-', 'con-', 'cont-', 'normal', '|', 'none', '|', '[', '<string>', '|', '<uri>', '|', '<counter>', '|', 'attr(<identifier>)', '|', 'open-quote', '|', 'close-quote', '|', 'no-open-quote', '|', 'no-close-quote', ']+', '|', 'inherit'], 'border-right': ['b-', 'bor-', 'bord-', '<border-width>', '||', '<border-style>', '||', "'],'border-top-color'", ']', '|inherit'], 'max-height': ['m-', 'max-', 'max--', '<length>', '|', '<percentage>', '|', 'none', '|', 'inherit'], 'padding-right': ['p-', 'pad-', 'padd-', '<padding-width>', '|', 'inherit'], 'voice-family': ['v-', 'voi-', 'voic-', '[[<specific-voice>', '|', '<generic-voice>', '],]*', '[<specific-voice>|', '<generic-voice>', ']', '|', 'inherit'], 'list-style-type': ['l-', 'lis-', 'list-', 'disc', '|', 'circle', '|', 'square', '|', 'decimal', '|', 'decimal-leading-zero', '|', 'lower-roman', '|', 'upper-roman', '|', 'lower-greek', '|', 'lower-latin', '|', 'upper-latin', '|', 'armenian', '|', 'georgian', '|', 'lower-alpha', '|', 'upper-alpha', '|', 'none', '|', 'inherit'], 'margin': ['m-', 'mar-', 'marg-', '<margin-width>{1,4}', '|', 'inherit'], 'border-left-width': ['b-', 'bor-', 'bord-', '<border-width>', '|', 'inherit'], 'min-width': ['m-', 'min-', 'min--', '<length>', '|', '<percentage>', '|', 'inherit'], 'text-align': ['t-', 'tex-', 'text-', 'left', '|', 'right', '|', 'center', '|', 'justify', '|', 'inherit'], 'border-style': ['b-', 'bor-', 'bord-', '<border-style>{1,4}', '|', 'inherit'], 'pause-after': ['p-', 'pau-', 'paus-', '<time>', '|', '<percentage>', '|', 'inherit'], 'direction': ['d-', 'dir-', 'dire-', 'ltr', '|', 'rtl', '|', 'inherit'], 'stress': ['s-', 'str-', 'stre-', '<number>', '|', 'inherit'], 'azimuth': ['a-', 'azi-', 'azim-', '<angle>', '|', '[[', 'left-side', '|', 'far-left', '|', 'left', '|', 'center-left', '|', 'center', '|', 'center-right', '|', 'right', '|', 'far-right', '|', 'right-side', ']', '||', 'behind', ']', '|', 'leftwards', '|', 'rightwards', '|', 'inherit'], 'outline-color': ['o-', 'out-', 'outl-', '<color>', '|', 'invert', '|', 'inherit'], 'text-indent': ['t-', 'tex-', 'text-', '<length>', '|', '<percentage>', '|', 'inherit'], 'border-bottom-color': ['b-', 'bor-', 'bord-', '<color>', '|', 'transparent', '|', 'inherit'], 'border-bottom-width': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'right': ['r-', 'rig-', 'righ-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'text-decoration': ['t-', 'tex-', 'text-', 'none', '|', '[', 'underline', '||', 'overline', '||', 'line-through', '||', 'blink', ']', '|inherit'], 'page-break-after': ['p-', 'pag-', 'page-', 'auto', '|', 'always', '|', 'avoid', '|', 'left', '|', 'right', '|', 'inherit'], 'bottom': ['b-', 'bot-', 'bott-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'unicode-bidi': ['u-', 'uni-', 'unic-', 'normal', '|', 'embed', '|', 'bidi-override', '|', 'inherit'], 'background-position': ['b-', 'bac-', 'back-', '[[', '<percentage>', '|', '<length>', '|', 'left', '|', 'center', '|', 'right', ']', '[<percentage>', '|', '<length>', '|', 'top', '|', 'center', '|', 'bottom', ']?', ']', '|', '[[', 'left', '|', 'center', '|', 'right', ']', '||', '[', 'top', '|', 'center', '|', 'bottom', ']', ']', '|', 'inherit'], 'clear': ['c-', 'cle-', 'clea-', 'none', '|', 'left', '|', 'right', '|', 'both', '|', 'inherit'], 'border-top-color': ['b-', 'bor-', 'bord-', '<color>', '|', 'transparent', '|', 'inherit'], 'border-left-color': ['b-', 'bor-', 'bord-', '<color>', '|', 'transparent', '|', 'inherit'], 'margin-right': ['m-', 'mar-', 'marg-', '<margin-width>', '|', 'inherit'], 'counter-reset': ['c-', 'cou-', 'coun-', '<identifier>', '<integer>?', ']+', '|', 'none', '|', 'inherit'], 'vertical-align': ['v-', 'ver-', 'vert-', 'baseline', '|', 'sub', '|', 'super', '|', 'top', '|', 'text-top', '|', 'middle', '|', 'bottom', '|', 'text-bottom', '|', '<percentage>', '|', '<length>', '|', 'inherit'], 'empty-cells': ['e-', 'emp-', 'empt-', 'show', '|', 'hide', '|', 'inherit'], 'list-style-image': ['l-', 'lis-', 'list-', '<uri>', '|', 'none', '|', 'inherit'], 'play-during': ['p-', 'pla-', 'play-', '<uri>', '[', 'mix', '||', 'repeat', ']?', '|', 'auto', '|', 'none', '|', 'inherit'], 'speech-rate': ['s-', 'spe-', 'spee-', '<number>', '|', 'x-slow', '|', 'slow', '|', 'medium', '|', 'fast', '|', 'x-fast', '|', 'faster', '|', 'slower', '|', 'inherit'], 'border-bottom': ['b-', 'bor-', 'bord-', '<border-width>', '||', '<border-style>', '||', "'],'border-top-color'", ']', '|inherit'], 'counter-increment': ['c-', 'cou-', 'coun-', '<identifier>', '<integer>?', ']+', '|', 'none', '|', 'inherit'], 'pitch': ['p-', 'pit-', 'pitc-', '<frequency>', '|', 'x-low', '|', 'low', '|', 'medium', '|', 'high', '|', 'x-high', '|', 'inherit'], 'border-spacing': ['b-', 'bor-', 'bord-', '<length>', '<length>?', '|', 'inherit'], 'speak-punctuation': ['s-', 'spe-', 'spea-', 'code', '|', 'none', '|', 'inherit'], 'padding-top': ['p-', 'pad-', 'padd-', '<padding-width>', '|', 'inherit'], 'min-height': ['m-', 'min-', 'min--', '<length>', '|', '<percentage>', '|', 'inherit'], 'letter-spacing': ['l-', 'let-', 'lett-', 'normal', '|', '<length>', '|', 'inherit'], 'richness': ['r-', 'ric-', 'rich-', '<number>', '|', 'inherit'], 'margin-top': ['m-', 'mar-', 'marg-', '<margin-width>', '|', 'inherit'], 'overflow': ['o-', 'ove-', 'over-', 'visible', '|', 'hidden', '|', 'scroll', '|', 'auto', '|', 'inherit'], 'outline': ['o-', 'out-', 'outl-', '[', "'outline-color'", '||', "'outline-style'", '||', "'outline-width'", ']', '|', 'inherit'], 'volume': ['v-', 'vol-', 'volu-', '<number>', '|', '<percentage>', '|', 'silent', '|', 'x-soft', '|', 'soft', '|', 'medium', '|', 'loud', '|', 'x-loud', '|', 'inherit'], 'speak-numeral': ['s-', 'spe-', 'spea-', 'digits', '|', 'continuous', '|', 'inherit'], 'speak-header': ['s-', 'spe-', 'spea-', 'once', '|', 'always', '|', 'inherit'], 'background-repeat': ['b-', 'bac-', 'back-', 'repeat', '|', 'repeat-x', '|', 'repeat-y', '|', 'no-repeat', '|', 'inherit'], 'list-style': ['l-', 'lis-', 'list-', '[', "'list-style-type'", '||', "'list-style-position'", '||', "'list-style-image'", ']', '|inherit'], 'position': ['p-', 'pos-', 'posi-', 'static', '|', 'relative', '|', 'absolute', '|', 'fixed', '|', 'inherit'], 'border-right-width': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'padding': ['p-', 'pad-', 'padd-', '<padding-width>{1,4}', '|', 'inherit'], 'border-right-style': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'cue-after': ['c-', 'cue-', 'cue--', '<uri>', '|', 'none', '|', 'inherit'], 'outline-width': ['o-', 'out-', 'outl-', '<border-width>', '|', 'inherit'], 'page-break-inside': ['p-', 'pag-', 'page-', 'avoid', '|', 'auto', '|', 'inherit'], 'orphans': ['o-', 'orp-', 'orph-', '<integer>', '|', 'inherit'], 'top': ['t-', 'top-', 'top-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'table-layout': ['t-', 'tab-', 'tabl-', 'auto', '|', 'fixed', '|', 'inherit'], 'border-left-style': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'border-left': ['b-', 'bor-', 'bord-', '<border-width>', '||', '<border-style>', '||', "'],'border-top-color'", ']', '|inherit'], 'display': ['d-', 'dis-', 'disp-', 'inline', '|', 'block', '|', 'list-item', '|', 'inline-block', '|', 'table', '|', 'inline-table', '|', 'table-row-group', '|', 'table-header-group', '|', 'table-footer-group', '|', 'table-row', '|', 'table-column-group', '|', 'table-column', '|', 'table-cell', '|', 'table-caption', '|', 'none', '|', 'inherit'], 'padding-bottom': ['p-', 'pad-', 'padd-', '<padding-width>', '|', 'inherit'], 'border-color': ['b-', 'bor-', 'bord-', '<color>', '|', 'transparent', ']{1,4}', '|', 'inherit'], 'widows': ['w-', 'wid-', 'wido-', '<integer>', '|', 'inherit'], 'border-bottom-style': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'border-right-color': ['b-', 'bor-', 'bord-', '<color>', '|', 'transparent', '|', 'inherit'], 'font-style': ['f-', 'fon-', 'font-', 'normal', '|', 'italic', '|', 'oblique', '|', 'inherit'], 'left': ['l-', 'lef-', 'left-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'border-collapse': ['b-', 'bor-', 'bord-', 'collapse', '|', 'separate', '|', 'inherit'], 'border-top-style': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'word-spacing': ['w-', 'wor-', 'word-', 'normal', '|', '<length>', '|', 'inherit'], 'background-color': ['b-', 'bac-', 'back-', '<color>', '|', 'transparent', '|', 'inherit'], 'cursor': ['c-', 'cur-', 'curs-', '[', '[<uri>', ',]*', '[', 'auto', '|', 'crosshair', '|', 'default', '|', 'pointer', '|', 'move', '|', 'e-resize', '|', 'ne-resize', '|', 'nw-resize', '|', 'n-resize', '|', 'se-resize', '|', 'sw-resize', '|', 's-resize', '|', 'w-resize', '|', 'text', '|', 'wait', '|', 'help', '|', 'progress', ']', ']', '|', 'inherit'], 'outline-style': ['o-', 'out-', 'outl-', '<border-style>', '|', 'inherit'], 'font-variant': ['f-', 'fon-', 'font-', 'normal', '|', 'small-caps', '|', 'inherit'], 'cue': ['c-', 'cue-', 'cue-', '[', "'cue-before'", '||', "'cue-after'", ']', '|', 'inherit'], 'max-width': ['m-', 'max-', 'max--', '<length>', '|', '<percentage>', '|', 'none', '|', 'inherit'], 'margin-bottom': ['m-', 'mar-', 'marg-', '<margin-width>', '|', 'inherit'], 'visibility': ['v-', 'vis-', 'visi-', 'visible', '|', 'hidden', '|', 'collapse', '|', 'inherit'], 'border-top': ['b-', 'bor-', 'bord-', '<border-width>', '||', '<border-style>', '||', "'],'border-top-color'", ']', '|inherit'], 'border-width': ['b-', 'bor-', 'bord-', '<border-width>{1,4}', '|', 'inherit'], 'white-space': ['w-', 'whi-', 'whit-', 'normal', '|', 'pre', '|', 'nowrap', '|', 'pre-wrap', '|', 'pre-line', '|', 'inherit'], 'text-transform': ['t-', 'tex-', 'text-', 'capitalize', '|', 'uppercase', '|', 'lowercase', '|', 'none', '|', 'inherit'], 'width': ['w-', 'wid-', 'widt-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'background-attachment': ['b-', 'bac-', 'back-', 'scroll', '|', 'fixed', '|', 'inherit'], 'speak': ['s-', 'spe-', 'spea-', 'normal', '|', 'none', '|', 'spell-out', '|', 'inherit'], 'page-break-before': ['p-', 'pag-', 'page-', 'auto', '|', 'always', '|', 'avoid', '|', 'left', '|', 'right', '|', 'inherit'], 'height': ['h-', 'hei-', 'heig-', '<length>', '|', '<percentage>', '|', 'auto', '|', 'inherit'], 'background': ['b-', 'bac-', 'back-', "['background-color'", '||', "'background-image'", '||', "'background-repeat'", '||', "'background-attachment'", '||', "'background-position']", '|', 'inherit'], 'font-weight': ['f-', 'fon-', 'font-', 'normal', '|', 'bold', '|', 'bolder', '|', 'lighter', '|', '100', '|', '200', '|', '300', '|', '400', '|', '500', '|', '600', '|', '700', '|', '800', '|', '900', '|', 'inherit'], 'z-index': ['z-', 'z-i-', 'z-in-', 'auto', '|', '<integer>', '|', 'inherit'], 'padding-left': ['p-', 'pad-', 'padd-', '<padding-width>', '|', 'inherit'], 'cue-before': ['c-', 'cue-', 'cue--', '<uri>', '|', 'none', '|', 'inherit'], 'quotes': ['q-', 'quo-', 'quot-', '<string>', '<string>]+', '|', 'none', '|', 'inherit'], 'line-height': ['l-', 'lin-', 'line-', 'normal', '|', '<number>', '|', '<length>', '|', '<percentage>', '|', 'inherit'], 'float': ['f-', 'flo-', 'floa-', 'left', '|', 'right', '|', 'none', '|', 'inherit'], 'color': ['c-', 'col-', 'colo-', '<color>', '|', 'inherit'], 'pitch-range': ['p-', 'pit-', 'pitc-', '<number>', '|', 'inherit'], 'border-top-width': ['b-', 'bor-', 'bord-', '<border-style>', '|', 'inherit'], 'font': ['f-', 'fon-', 'font-', '[', '[', "'font-style'", '||', "'font-variant'", '||', "'font-weight'", ']?', "'font-size'", '[', "/'line-height'", ']?', "'font-family'", ']', '|', 'caption', '|', 'icon', '|', 'menu', '|', 'message-box', '|', 'small-caption', '|', 'status-bar', '|', 'inherit']}