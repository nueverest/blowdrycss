from collections import OrderedDict
from copy import deepcopy
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# DataLibrary is not intended for use outside of this file as each time its' called it rebuilds the dictionaries.
class DataLibrary(object):
    def __init__(self):
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

        self.property_alias_dict = self.build_property_alias_dict()

        # TODO: Review whether this is still necessary
        # Sort property_alias_dict with the longest items first as the most verbose match is preferred.
        # i.e. If css_class == 'margin-top' Then match the property_alias_dict key 'margin-top' not 'margin'
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
                    print('KeyError: property_name "', property_name, '" not found in property_dict.')
        return property_dict

    # Remove duplicate/clashing aliases from property_alias_dict.
    @staticmethod
    def get_clashing_aliases(property_dict=None):
        clone_dict = property_dict
        clashing_alias_dict = {}
        for key1, alias_set1 in property_dict.items():
            for key2, alias_set2 in clone_dict.items():
                intersection = alias_set1.intersection(alias_set2)
                if len(intersection) > 0 and key1 != key2:                  # prevent direct comparison of the same key.
                    try:
                        clashing_alias_dict[key1] = clashing_alias_dict[key1].union(intersection)
                    except KeyError:
                        clashing_alias_dict[key1] = intersection
        print('clashing aliases', clashing_alias_dict)
        return clashing_alias_dict

    @staticmethod
    def remove_clashing_aliases(property_dict=None, clashing_alias_dict=None):
        clean_dict = deepcopy(property_dict)
        for property_name in property_dict:
            try:
                clashing_aliases = clashing_alias_dict[property_name]
                for clashing_alias in clashing_aliases:
                    if clashing_alias in property_dict[property_name]:                                      # If Exists
                        clean_dict[property_name] = property_dict[property_name].remove(clashing_alias)     # Remove it.
                        if clean_dict[property_name] is None:
                            clean_dict[property_name] = set()   # Replace None with set()
            except KeyError:
                pass
        print('clashing aliases removed', clean_dict)
        return clean_dict

    # Builds a property_alias_dict using the following steps:
    # Initialize,
    # Merge with custom_property_alias_dict to allow integration of user defined aliases.
    # Get Clashing Aliases.
    # Remove Clashing Aliases.
    def build_property_alias_dict(self):
        _dict = self.initialize_property_alias_dict(property_names=self.property_names)                     # Initialize
        _dict = self.merge_dicts(property_dict=_dict, custom_dict=self.custom_property_alias_dict)          # Merge
        clashing_alias_dict = self.get_clashing_aliases(property_dict=_dict)                                # Get Clash
        _dict = self.remove_clashing_aliases(property_dict=_dict, clashing_alias_dict=clashing_alias_dict)  # Fix Clash
        return _dict


# DataLibrary is not intended for use outside of this file as each time its' called it rebuilds the dictionaries.
__data_library = DataLibrary()

# Only Variables intended for outside use.
default_property_units_dict = __data_library.default_property_units_dict
property_alias_dict = __data_library.property_alias_dict
ordered_property_dict = __data_library.ordered_property_dict
