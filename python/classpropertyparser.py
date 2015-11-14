from cssutils import parseString
from string import ascii_lowercase, digits
from collections import OrderedDict
# Custom
from cssvalueparser import CSSPropertyValueParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ClassPropertyParser(object):
    # CSS Unit Reference: http://www.w3schools.com/cssref/css_units.asp
    # CSS Value Reference: http://www.w3.org/TR/CSS21/propidx.html
    def __init__(self, class_set=set()):
        css = u'''/* Generated with BlowDryCSS. */'''
        self.sheet = parseString(css)
        self.rules = []
        self.css_units = {
            'px', 'em', 'rem', 'p', 'ex', 'cm', 'mm', 'in', 'pt', 'pc', 'ch', 'vh', 'vw', 'vmin', 'vmax',   # distance
            'deg', 'grad', 'rad',                                                                           # angle
            'ms', 's',                                                                                      # time
            'Hz', 'kHz',                                                                                    # frequency

        }
        self.importance_designator = '-i'       # '-i' is used to designate that the priority level is '!important'
        self.removed_class_set = set()
        self.class_set = class_set
        self.clean_class_set()
        print('clean ran')

        # TODO: create function that validates dictionary ensuring that no aliases clash.
        # TODO: move this to a CSV file and autogenerate this dictionary from CSV.
        # Dictionary contains:
        #   css property name as 'keys'
        #   list of aliases as 'values' - An alias can be shorthand for the property name.
        self.property_dict = {
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
        # Sort property_dict with the longest items first as the most verbose match is preferred.
        # i.e. If css_class == 'margin-top' Then we want it to match the property_dict key 'margin-top' not 'margin'
        self.ordered_property_dict = OrderedDict(
            sorted(self.property_dict.items(), key=lambda t: len(t[0]), reverse=True)
        )

        # TODO: explore another way using regex for property (no cssutils already does regex validation)
        # allowed = self.allowed_unit_characters()
        # self.property_dict = {
        #     'font-weight': [['normal', 'bold', 'bolder', 'lighter', 'initial', 'fw-'], r"([0-9a-z-])"],
        #     'padding': [['p-'], r"([0-9" + allowed + "_-])"],
        #     'height': [['h-'], r"([0-9" + allowed + "_-])"],
        # }

    # Reduces css_units to a minimum set of allowed characters.
    # Used in property_dict regex.
    # Example: converts {'px', 'em', 'rem'} --> 'pxemr' thus eliminating duplicate 'e' and 'm'
    # def allowed_unit_characters(self):
    #     allowed = ''
    #     for css_unit in self.css_units:
    #         allowed += css_unit
    #     return allowed

    # Take list, tuple, or set of strings an convert to lowercase.
    def class_set_to_lowercase(self):
        self.class_set = {css_class.lower() for css_class in self.class_set}

    # Validate underscore usage in a single css_class.
    # Underscores are only allowed to designate a decimal point between numbers.
    #   Valid: '6_3'
    # Invalid: '_b', 'b_', 'padding-_2", '2_rem', 'm_px', and '__'
    @staticmethod
    def underscores_valid(css_class=''):
        # underscore is not allowed to be the first or last character of css_class
        if css_class[0] == '_' or css_class[-1] == '_':
            return False

        # Check character before and after underscore index.
        index = css_class.find('_')
        allowed_before = set(digits)
        allowed_after = set(digits)
        if index > 0:                                                   # Underscore is not the first character.
            valid = set(css_class[index-1]) <= allowed_before           # Check Character before
            valid = valid and set(css_class[index+1]) <= allowed_after  # Check Character after.
        else:
            valid = True

        return valid

    # Detect and Remove invalid css classes from class_set
    # Class names must abide by: http://www.w3.org/TR/CSS2/syndata.html#characters
    # For purposes of this library only a SUBSET of the standard is permissible as follows:
    # Classes are only allowed to begin with [a-z]
    # Classes are only allowed to end with [a-z0-9]
    # Classes are allowed to contain [_a-z0-9-]
    # Underscores are only allowed between digits [0-9]
    # Reference: stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
    def clean_class_set(self):
        # Set all strings to lowercase first.
        self.class_set_to_lowercase()

        # Validate against character sets.
        allowed_first = set(ascii_lowercase)
        allowed_middle = set(ascii_lowercase + digits + '_-')
        allowed_last = set(ascii_lowercase + digits)

        # Gather invalid_css_classes
        invalid_css_classes = []
        reasons = []

        # 'continue' is used to prevent the same css_class from being added to the invalid_css_classes multiple times.
        for css_class in self.class_set:
            if not set(css_class[0]) <= allowed_first:              # First character
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z allowed for first character of class.)')
                continue
            if not set(css_class) <= allowed_middle:                # All characters
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z, 0-9, "_", and "-" are allowed in class name.)')
                continue
            if not set(css_class[-1]) <= allowed_last:              # Last character
                invalid_css_classes.append(css_class)
                reasons.append(' (Only a-z and 0-9 allowed for last character of class.)')
                continue
            if not self.underscores_valid(css_class=css_class):     # Underscore
                invalid_css_classes.append(css_class)
                reasons.append(' (Invalid underscore usage in class.)')
                continue

        # Remove invalid_css_classes from self.class_set
        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.class_set.remove(invalid_css_class)
            self.removed_class_set.add(invalid_css_class + reasons[i])

    # Property Name
    #
    # Class returns the property_name or removes/cleans the unrecognized class and returns ''.
    # Classes that use identical property names must set a property value
    # i.e. 'font-weight' is invalid because no value is included AND 'font-weight-700' is valid because 700 is a value.
    def get_property_name(self, css_class=''):
        for property_name, aliases in self.ordered_property_dict.items():
            # Try identical key match first. An exact css_class match must also end with a '-' dash to be valid.
            if css_class.startswith(property_name + '-'):
                return property_name

            # Sort the aliases by descending string length
            # This is necessary when the css_class == 'bolder' since 'bold' appears before 'bolder'
            # TODO: Instead of doing this multiple times do it once in self.property_dict.
            aliases = sorted(aliases, key=len, reverse=True)

            # Try matching with alias. An alias is not required to end with a dash, but could if it is an abbreviation.
            for alias in aliases:
                if css_class.startswith(alias):
                    return property_name

        # No match found. Remove from class_set.
        # self.class_set.remove(css_class)
        # self.removed_class_set.add(css_class + ' (Property name does not match patterns in self.property_dict.)')
        return ''

    # Strip property name from encoded_property_value if applicable and return encoded_property_value.
    @staticmethod
    def strip_property_name(property_name='', encoded_property_value=''):
        # Deny empty string. If it doesn't have a property name ignore it.
        if property_name == '':
            raise ValueError('CSS property_name cannot be empty.')
        # Append '-' to property to match the class format.
        else:
            property_name += '-'

        # Strip property name
        if encoded_property_value.startswith(property_name):
            return encoded_property_value[len(property_name):]
        else:
            return encoded_property_value

    # Some alias could be abbreviations e.g. 'fw-' stands for 'font-weight-'
    # In these cases a dash is added in the dictionary to indicate an abbreviation.
    @staticmethod
    def alias_is_abbreviation(alias=''):
        return alias.endswith('-')

    # Returns a list of all property abbreviations appearing in property_dict
    def get_property_abbreviations(self, property_name=''):
        property_abbreviations = list()
        for alias in self.property_dict[property_name]:
            if self.alias_is_abbreviation(alias=alias):
                property_abbreviations.append(alias)
        return property_abbreviations

    # Strip property abbreviation from encoded_property_value if applicable and return encoded_property_value.
    def strip_property_abbreviation(self, property_name='', encoded_property_value=''):
        property_abbreviations = self.get_property_abbreviations(property_name=property_name)

        for property_abbreviation in property_abbreviations:
            if encoded_property_value.startswith(property_abbreviation):
                return encoded_property_value[len(property_abbreviation):]
        return encoded_property_value

    # Property Value
    #
    # Valid encoded_property_values: '1p-2p-1p-1p', '5rem', '6ex', 'bold'
    # def encoded_property_value_is_valid(self, encoded_property_value):
    #     for value in self.text_only_values:
    #         if encoded_property_value == value:
    #             return True
    #         handle suffix

    # Strip property name or abbreviation prefix and property priority designator
    # Examples:
    # 'fw-bold-i' --> 'bold'                [abbreviated font-weight property_name]
    # 'padding-1-10-10-5-i' --> '1-10-10-5' [standard property_name]
    # 'height-7_25rem-i' --> '7_25rem'      [contains underscores]
    # The term encoded_property_value means a property value that may or may not contain dashes and underscores.
    def get_encoded_property_value(self, property_name='', css_class=''):
        encoded_property_value = css_class
        encoded_property_value = self.strip_property_name(property_name, encoded_property_value)
        encoded_property_value = self.strip_property_abbreviation(property_name, encoded_property_value)
        encoded_property_value = self.strip_priority_designator(encoded_property_value)
        return encoded_property_value

    # Accepts an encoded_property_value that's been stripped of it's property named and priority
    # Returns a valid css property value or ''.
    @staticmethod
    def get_property_value(css_class='', property_name='', encoded_property_value='', property_priority=''):
        property_parser = CSSPropertyValueParser()
        value = property_parser.decode_property_value(property_name=property_name, value=encoded_property_value)
        return value

    # Property Priority
    #
    def is_important(self, css_class=''):
        return css_class.endswith(self.importance_designator)

    # Strip priority designator from the end of encoded_property_value.
    def strip_priority_designator(self, encoded_property_value=''):
        if self.is_important(css_class=encoded_property_value):
            return encoded_property_value[:-len(self.importance_designator)]
        else:
            return encoded_property_value

    def get_property_priority(self, css_class=''):
        return 'IMPORTANT' if self.is_important(css_class=css_class) else ''

    # Credit: Sergey Chikuyonok (serge.che@gmail.com)
    # https://code.google.com/p/zen-coding/source/browse/branches/serge.che/python/zencoding/zen_settings.py
    @staticmethod
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