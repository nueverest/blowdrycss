from html.parser import HTMLParser

# Custom Classes
from filehandler import FileConverter


class HTMLAttributeParser(HTMLParser):
    # attribute_name can be set to 'id', 'class', 'alt', etc.
    def __init__(self, attribute_name=''):
        super().__init__()
        self.attribute_name = attribute_name
        self.attribute_value_list = []

    def handle_starttag(self, tag, attrs):
        # self.print_class_value(tag=tag, attrs=attrs)
        self.set_attribute_value_list(attrs)

    def handle_startendtag(self, tag, attrs):
        # self.print_class_value(tag=tag, attrs=attrs)
        self.set_attribute_value_list(attrs)

    # Creates a set of all values in an HTML file with self.attribute_name.
    def set_attribute_value_list(self, attrs):
        for name, value in attrs:
            if name == self.attribute_name:
                self.attribute_value_list.append(value)

    # Used for debugging functions.
    # @staticmethod
    # def print_class_value(self, tag, attrs):
    #     for name, value in attrs:
    #         if name == self.attribute_name:
    #             print("tag:", tag, "\t\t", self.attribute_name, ":", value)


class HTMLClassParser(object):
    def __init__(self, files):
        for file in files:
            self.class_set = {}

            # Convert file to string.
            file_converter = FileConverter(file_path=file)
            file_string = file_converter.get_file_as_string()
            print(file_string)

            # Generate list of class strings
            class_parser = HTMLAttributeParser(attribute_name='class')
            class_parser.feed(file_string)

            # Convert list of class strings to set
            print("Class List:\t", class_parser.attribute_value_list)
            self.set_class_set(class_parser.attribute_value_list)
            print(" Class Set:\t", self.class_set)

    def set_class_set(self, attribute_value_list):
        for value in attribute_value_list:
            self.class_set = set.union(
                set(value.split()),         # Split space delimited string into set().
                self.class_set              # Unite the new set with class_set.
            )                               # Assign union() to self.class_set.

