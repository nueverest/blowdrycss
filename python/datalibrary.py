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
        return set()

    abbreviations = set()                                          # First three letters
    if '-' in property_name:                                    # First dash
        dash_index1 = property_name.index('-')
        suffix = property_name[dash_index1 + 1:]
        if '-' in suffix:                                       # Second dash (rare)
            dash_index2 = suffix.index('-')
            abbreviations.add(                               # Three letter abbreviation
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


def list_clashing_aliases(_dict=None):
    clone_dict = _dict
    _clashing_aliases = set()
    for key1, alias_set1 in _dict.items():
        for key2, alias_set2 in clone_dict.items():
            intersection = alias_set1.intersection(alias_set2)
            if len(intersection) > 0 and key1 != key2:      # prevent direct comparison of the same key.
                _clashing_aliases = _clashing_aliases.union(intersection)
    return _clashing_aliases


property_alias_dict = create_property_alias_dict(property_value_dict=full_property_value_dict)
clashing_aliases = list_clashing_aliases(_dict=property_alias_dict)

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