# python 2
from __future__ import print_function
# general
from cssutils.css import Property
from xml.dom import SyntaxErr
# custom
from classpropertyparser import ClassPropertyParser
from breakpointparser import BreakpointParser
from scalingparser import ScalingParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class MediaQueryBuilder(object):
    def __init__(self, property_parser=ClassPropertyParser()):
        # Takes a set of classes that contain media query flags
        # Invalidates classes that contain mixed syntax ``small-down-s`` or ``font-size-28-medium-only-s``
        # i.e. mixing breakpoint and scaling syntax is not allowed.
        print(u'\nMediaQueryBuilder Running...\n')
        self.property_parser = property_parser
        self.css_media_queries = set()
        self.media_query_text = ''

        not_media_classes = dict()
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)
            priority = self.property_parser.get_property_priority(css_class=css_class)
            clean_css_class = ''    # Prevents css_class from being modified.

            if name:
                # value='inherit' since we do not know if the class is valid yet.
                inherit_property = Property(name=name, value='inherit', priority=priority)

                scaling_parser = ScalingParser(css_class=css_class, css_property=inherit_property)
                is_scaling = scaling_parser.is_scaling
                if is_scaling:
                    clean_css_class = scaling_parser.strip_scaling_flag()

                breakpoint_parser = BreakpointParser(css_class=css_class, css_property=inherit_property)
                is_breakpoint = breakpoint_parser.is_breakpoint
                if is_breakpoint:
                    clean_css_class = breakpoint_parser.strip_breakpoint_limit()

                if is_breakpoint and is_scaling:                                                    # Mixed syntax
                    not_media_classes[css_class] = ' (breakpoint and scaling media query syntax cannot be combined.)'
                    continue

                if not is_breakpoint and not is_scaling:                                            # Missing syntax
                    not_media_classes[css_class] = ' is not a media query css_class selector.'
                    continue
            else:
                not_media_classes[css_class] = ' is not a media query css_class selector.'
                continue

            if clean_css_class and property_parser.is_important(css_class=clean_css_class):
                clean_css_class = property_parser.strip_priority_designator(css_class=clean_css_class)

            # Set property value.
            # Handles case where css_class equals 'small-down', 'large-only', 'medium-up', etc.
            # Specifically handle the 'display' case.
            if clean_css_class and clean_css_class != 'display':
                # Can return an empty string '' if css_class does not match any patterns in the property_alias_dict.
                try:
                    encoded_property_value = self.property_parser.get_encoded_property_value(
                        property_name=name,
                        css_class=clean_css_class
                    )
                    value = self.property_parser.get_property_value(
                        property_name=name,
                        encoded_property_value=encoded_property_value
                    )
                except ValueError:
                    not_media_classes[css_class] = ' (property_name not found in property_alias_dict.)'
                    continue
            else:
                value = 'none'     # Breakpoint Parser -> display: none;

            # Build CSS Property AND Add to css_media_queries OR Remove invalid css_class from class_set.
            try:
                css_property = Property(name=name, value=value, priority=priority)

                if css_property.valid:
                    if is_breakpoint and breakpoint_parser:
                        breakpoint_parser.css_property = css_property
                        media_query = breakpoint_parser.build_media_query()
                        self.css_media_queries.add(media_query)
                    if is_scaling:
                        scaling_parser.css_property = css_property
                        media_query = scaling_parser.build_media_query()
                        self.css_media_queries.add(media_query)
                else:
                    not_media_classes[css_class] = ' (cssutils invalid property value: ' + value + ')'
                    continue
            # This exception can't be tested as clean_class_set() and get_property_value() prevent it.(Triple Redundant)
            except SyntaxErr:   # Special Case - Not Tested
                not_media_classes[css_class] = ' (cssutils SyntaxErr invalid property value: ' + value + ')'
                continue

        # Clean out invalid CSS Classes.
        for invalid_css_class, reason in not_media_classes.items():
            self.property_parser.class_set.remove(invalid_css_class)
            self.property_parser.removed_class_set.add(invalid_css_class + reason)

    @staticmethod
    def class_is_parsable(css_class, name):
        """ Returns True if breakpoint and scaling syntax are not combined.  Otherwise returns False.

        **Rule:**

        Breakpoint and scaling syntax cannot be mixed or combined.

        | Allowed: ``display-medium-down``, ``large-up``, and ``font-size-24-s``
        | Not Allowed: ``display-medium-down-s``, ``large-up-s``, and ``font-size-24-small-only-s``

        :type css_class: str
        :type name: str

        :param css_class: An encoded css class.
        :param name: A CSS property name.
        :return: (*str*) -- Returns True if breakpoint and scaling syntax are not combined.  Otherwise returns False.

        """
        scaling_parser = ScalingParser(css_class=css_class, css_property=name)

        # Scaling but not Breakpoint case.
        if scaling_parser.is_scaling:
            try:
                BreakpointParser(css_class=css_class)
            except ValueError:
                return True

        # Breakpoint but not Scaling
        try:
            BreakpointParser(css_class=css_class)
            return not scaling_parser.is_scaling
        except ValueError:
            return False

    def get_css_text(self):
        """ Joins ``css_media_queries`` together with an empty separator string ``''``.

        :return: str -- Returns all media queries as CSS text.

        """
        return str.join('', self.css_media_queries)

