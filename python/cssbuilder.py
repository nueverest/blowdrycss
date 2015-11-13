from cssutils.css import Property, CSSStyleRule, CSSStyleSheet
from xml.dom import SyntaxErr
# Custom
from classpropertyparser import ClassPropertyParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class CSSBuilder(object):
    def __init__(self, property_parser=ClassPropertyParser()):
        print('\nCSSBuilder Running:')
        self.property_parser = property_parser
        self.css_rules = set()
        self.css_stylesheet = CSSStyleSheet()

        invalid_css_classes = []
        reasons = []
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)

            # 'name' can return an empty string '' if css_class does not match any patterns in the property_dict.
            try:
                encoded_property_value = self.property_parser.get_encoded_property_value(
                    property_name=name,
                    css_class=css_class
                )
            except ValueError:
                invalid_css_classes.append(css_class)
                reasons.append(' (property_name not found in self.property_dict.)')
                continue

            priority = self.property_parser.get_property_priority(css_class=css_class)
            value = self.property_parser.get_property_value(
                property_name=name,
                encoded_property_value=encoded_property_value,
                property_priority=priority      # TODO: Why is priority required???? Validation does not occur anymore.
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
            except SyntaxErr:
                invalid_css_classes.append(css_class)
                reasons.append(' (cssutils SyntaxErr invalid property value: ' + value + ')')
                continue

        # Clean out invalid CSS Classes.
        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.property_parser.class_set.remove(invalid_css_class)
            self.property_parser.removed_class_set.add(invalid_css_class + reasons[i])

        self.build_stylesheet()

    def build_stylesheet(self):
        for css_rule in self.css_rules:
            self.css_stylesheet.add(rule=css_rule)

    def get_css_text(self):
        return self.css_stylesheet.cssText

