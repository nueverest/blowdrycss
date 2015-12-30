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
        print('\nMediaQueryBuilder Running:')
        self.property_parser = property_parser
        self.css_media_queries = set()
        self.media_query_text = ''

        invalid_css_classes = []
        reasons = []
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)

            try:
                breakpoint_parser = BreakpointParser(css_class=css_class, name=name, value='none')
                is_breakpoint = True
                css_class = breakpoint_parser.strip_breakpoint_limit()
            except ValueError:
                is_breakpoint = False

            scaling_parser = ScalingParser(css_class=css_class, name=name)
            is_scaling = scaling_parser.is_scaling()
            css_class = scaling_parser.strip_scaling_flag()

            if is_breakpoint and is_scaling:
                invalid_css_classes.append(css_class)
                reasons.append(' (breakpoint and scaling media query class syntax cannot be combined.)')
                continue

            # Handle case where css_class equals 'small-down', 'large-only', 'medium-up', etc.
            if css_class:
                # Can return an empty string '' if css_class does not match any patterns in the property_alias_dict.
                try:
                    encoded_property_value = self.property_parser.get_encoded_property_value(
                        property_name=name,
                        css_class=css_class
                    )
                except ValueError:
                    invalid_css_classes.append(css_class)
                    reasons.append(' (property_name not found in property_alias_dict.)')
                    continue

            priority = self.property_parser.get_property_priority(css_class=css_class)
            value = self.property_parser.get_property_value(
                property_name=name,
                encoded_property_value=encoded_property_value
            )
            # Build CSS Property AND Add to css_rules OR Remove invalid css_class from class_set.
            try:
                css_property = Property(name=name, value=value, priority=priority)
                if css_property.valid:
                    css_class = '.' + css_class                         # prepend dot selector to class name.
                    css_rule = CSSStyleRule(selectorText=css_class, style=css_property.cssText)
                    self.css_rules.add(css_rule)
                else:
                    invalid_css_classes.append(css_class)
                    reasons.append(' (cssutils invalid property value: ' + value + ')')
                    continue
            # This exception can't be tested as clean_class_set() and get_property_value() prevent it.(Triple Redundant)
            except SyntaxErr:   # Special Case - Not Tested
                invalid_css_classes.append(css_class)
                reasons.append(' (cssutils SyntaxErr invalid property value: ' + value + ')')
                continue

        # Clean out invalid CSS Classes.
        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.property_parser.class_set.remove(invalid_css_class)
            self.property_parser.removed_class_set.add(invalid_css_class + reasons[i])

        self.build_stylesheet()

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
        scaling_parser = ScalingParser(css_class=css_class, name=name)

        # Scaling but not Breakpoint case.
        if scaling_parser.is_scaling():
            try:
                BreakpointParser(css_class=css_class, name=name, value='none')
            except ValueError:
                return True

        # Breakpoint but not Scaling
        try:
            BreakpointParser(css_class=css_class, name=name, value='none')
            return not scaling_parser.is_scaling()
        except ValueError:
            return False

    def build_stylesheet(self):
        """ Builds the stylesheet by adding CSS rules to the CSS stylesheet.

        :return: None
        """
        for css_rule in self.css_rules:
            self.css_stylesheet.add(rule=css_rule)

    def get_css_text(self):
        """
        :return: str -- Returns CSS text.
        """
        return self.css_stylesheet.cssText

