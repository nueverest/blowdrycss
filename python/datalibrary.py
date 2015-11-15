from collections import OrderedDict
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class DataLibrary(object):
    def __init__(self, custom_property_alias_dict=None):
        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        # Extracted all properties containing Values of <angle>, <percentage>, <length>, <time>, <frequency>
        # IDEA: Build webscraper that auto-extracts these.\
        self.default_property_units_dict = {       # Possible Occurrences:
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

        # TODO: create functions that validates dictionarien ensuring that no aliases clash.
        # TODO: move this to a CSV file and autogenerate this dictionary from CSV.
        # Dictionary contains:
        #   css property name as 'keys'
        #   list of aliases as 'values' - An alias can be shorthand for the property name.
        self.custom_property_alias_dict = {
            'background': {'bg-', },
            'background-color': {'bgc-', 'bg-c-', 'bg-color-', },
            'color': {'c-', },
            'font-size': {'fsize-', 'f-size-', },
            'font-weight': {'bold', 'bolder', 'lighter', 'fweight-', 'f-weight-', },
            'height': {'h-', },
            'margin': {'m-', },
            'margin-top': {'m-top-', },
            'margin-bottom': {'m-bot-', },
            'padding': {'p-', 'pad-', },
            'padding-top': {'p-top-', },
            'text-align': {'talign-', 't-align-', },
            'vertical-align': {'valign-', 'v-align-', },
            'width': {'w-', },
        }
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

        # Merge with user-defined custom_property_dict
        # self.merge_dicts(custom_property_alias_dict=custom_property_alias_dict)

        # Sort property_alias_dict with the longest items first as the most verbose match is preferred.
        # i.e. If css_class == 'margin-top' Then we want it to match the property_alias_dict key 'margin-top' not 'margin'
        # TODO: Combine these 5 into 1.
        self.property_alias_dict = self.create_property_alias_dict(property_names=self.property_names)
        self.property_alias_dict = self.add_custom_aliases(
            property_dict=self.property_alias_dict, custom_dict=custom_property_alias_dict
        )
        self.clashing_aliases = self.remove_clashing_aliases(property_dict=self.property_alias_dict)

        self.ordered_property_dict = OrderedDict(
            sorted(self.property_alias_dict.items(), key=lambda t: len(t[0]), reverse=True)
        )

    # Return abbreviation patterns.
    # No dash: [First three letters]
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
    @staticmethod
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

    # Accepts a set of property names.
    # Returns an alias dictionary with
    # Key   = Property Name
    # Value = Alias abbreviation set
    def create_property_alias_dict(self, property_names=set()):
        alias_dict = {}
        for property_name in property_names:
            abbreviations = self.get_abbreviated_property_names(property_name=property_name)
            value = abbreviations
            alias_dict[property_name] = value
        return alias_dict

    # Remove duplicate/clashing aliases from property_alias_dict
    @staticmethod
    def remove_clashing_aliases(property_dict=None):
        clone_dict = property_dict
        _clashing_aliases = set()
        for key1, alias_set1 in property_dict.items():
            for key2, alias_set2 in clone_dict.items():
                intersection = alias_set1.intersection(alias_set2)
                if len(intersection) > 0 and key1 != key2:                  # prevent direct comparison of the same key.
                    _clashing_aliases = _clashing_aliases.union(intersection)
        return _clashing_aliases

    @staticmethod
    def add_custom_aliases(property_dict=None, custom_dict=None):
        if custom_dict is not None:
            for property_name, alias_set in custom_dict.items():
                property_dict[property_name] = property_dict[property_name].union(alias_set)
        return property_dict
