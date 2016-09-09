# python 2
from __future__ import absolute_import, print_function, unicode_literals

# builtins
import logging

# plugins
from cssutils.css import Property
from xml.dom import SyntaxErr

# custom
from blowdrycss.classpropertyparser import ClassPropertyParser
from blowdrycss.breakpointparser import BreakpointParser
from blowdrycss.scalingparser import ScalingParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class MediaQueryBuilder(object):
    """ Builds a set of CSS media queries from valid classes found in ``ClassPropertyParser.class_set``.

    | Takes a set of classes that may or may not contain media query flags.
    | Mixing breakpoint and scaling syntax is not allowed. Classes that contain mixed syntax like the following:
    | ``small-down-s`` or ``font-size-28-medium-only-s`` are invalidated.

    :type property_parser: ClassPropertyParser

    :param property_parser: ClassPropertyParser object containing ``class_set``.
    :return: None

    **Example Usage:**

    >>> import blowdrycss_settings as settings
    >>> from classpropertyparser import ClassPropertyParser
    >>> class_set = {'bold', 'large-down', 'font-size-25-s'}
    >>> # Filter class names. Only keep classes matching the defined class encoding.
    >>> property_parser = ClassPropertyParser(class_set=class_set)
    >>> class_set = property_parser.class_set.copy()
    >>> # Build Media Queries
    >>> if settings.media_queries_enabled:
    >>>     unassigned_class_set = class_set.difference(property_parser.class_set)
    >>>     # Only use unassigned classes
    >>>     property_parser.class_set = unassigned_class_set
    >>>     property_parser.removed_class_set = set()
    >>>     media_query_builder = MediaQueryBuilder(property_parser=property_parser)
    >>>     css_text = bytes(media_query_builder.get_css_text(), 'utf-8')
    >>>     print(media_query_builder.property_parser.class_set)
    {'large-down', 'font-size-25-s'}

    """

    def __init__(self, property_parser=ClassPropertyParser()):
        message = 'MediaQueryBuilder Running...'
        print(message)
        logging.debug(msg=message)
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
                    not_media_classes[css_class] = ' (Breakpoint and scaling media query syntax cannot be combined.)'
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
                except ValueError:  # Impossible to get here if get_property_name() is working properly.
                    not_media_classes[css_class] = ' property_name not found in property_alias_dict.'
                    continue
            else:
                value = 'none'      # Breakpoint Parser Case -> display: none;

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

    def get_css_text(self):
        """ Joins ``css_media_queries`` together with an empty separator string ``''``.

        :return: str -- Returns all media queries as CSS text.

        **Example**

        >>> from classpropertyparser import ClassPropertyParser
        >>> class_set = {'bold', 'large-down', 'font-size-24-s'}
        >>> # Filter class names. Only keep classes matching the defined class encoding.
        >>> property_parser = ClassPropertyParser(class_set=class_set)
        >>> media_query_builder = MediaQueryBuilder(property_parser=property_parser)
        >>> print(media_query_builder.get_css_text())
        @media only screen and (min-width: 64.0em) {
            .large-down {
                display: none;
            }
        }
        .font-size-24-s {
            font-size: 24px;
            @media only screen and (max-width: 45.0em) {
                font-size: 21.3px;
            }
            @media only screen and (max-width: 30.0em) {
                font-size: 19.2px;
            }
        }

        """
        return str.join(str(''), self.css_media_queries)

