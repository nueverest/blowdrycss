# python 2
from __future__ import absolute_import, print_function, unicode_literals
# builtins
import logging
# plugins
from cssutils.css import Property, CSSStyleRule, CSSStyleSheet
from xml.dom import SyntaxErr
# custom
from blowdrycss.classpropertyparser import ClassPropertyParser

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class CSSBuilder(object):
    """ Builds CSS text with the ``cssutils.css`` module.

    **Note:** Removes invalid classes. A class is invalid for one of the following reasons:

    - It is not valid CSS.
    - It does not contain a valid ``blowdrycss`` encoding.

    **Object initialization process:**

    - Build CSS property rules
    - Add to css_rules, OR remove invalid css_class from class_set.
    - Build a CSS stylesheet based on the CSS ``css_rules`` set.

    | **Parameters: property_parser** (*ClassPropertyParser object*) -- Contains a class property parser with a
      populated class_set.
    | **Returns:** None

    """
    def __init__(self, property_parser=ClassPropertyParser()):
        message = 'CSSBuilder Running...'
        print(message)
        logging.debug(msg=message)
        self.property_parser = property_parser
        self.css_rules = set()
        self.css_stylesheet = CSSStyleSheet()

        invalid_css_classes = []
        reasons = []
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)

            # 'name' can return an empty string '' if css_class does not match any patterns in the property_alias_dict.
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

