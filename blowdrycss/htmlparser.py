# builtins
from html.parser import HTMLParser                  # Allowed after pip install future
# custom
from blowdrycss.filehandler import FileConverter

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class HTMLAttributeParser(HTMLParser):
    """ Inherits from HTMLParser. Overrides ``handle_starttag`` and ``handle_startendtag``.

    Parses attributes with the ``attribute_name`` provided.

    | HTML generally tags may contain attributes.
    | ``<div id="ex5" class="margin-10">Example Text</div>``

    In the case above ``id`` and ``class`` are attributes of the ``div``.

    | **Parameters:**
    | **attribute_name** (*str*) -- A valid html attribute can be set to ``id``, ``class``, ``alt``, etc.
      It is also possible to define a custom attribute.

    **Example:**

    >>> from os import getcwd, chdir, path
    >>> current_dir = getcwd()
    >>> chdir('..')
    >>> file_string = path.join(current_dir, 'examplesite', 'index.html')
    >>> chdir(current_dir)    # Change it back.
    >>> class_parser = HTMLAttributeParser(attribute_name='class')
    >>> class_parser.feed(file_string)
    >>> # Get attribute value list for html ``class`` attributes.
    >>> attribute_value_list = class_parser.attribute_value_list

    """
    def __init__(self, attribute_name=''):
        HTMLParser.__init__(self)               # Python 2 and 3 compatible: http://amyboyle.ninja/Python-Inheritance/
        self.attribute_name = attribute_name
        self.attribute_value_list = []

    def handle_starttag(self, tag, attrs):
        """
        | **Overrides HTMLParser method.**
        | https://docs.python.org/3.5/library/html.parser.html#html.parser.HTMLParser.handle_starttag

        | **What is a start tag?**
        | A tag that starts a section of HTML, for instance, ``<div>``.  This tag requires an end tag. A pair of
          start and end tags generally contain content between them.

        - Gathers every attribute for every start tag in a given HTML file.
        - Filters the attribute for the ``attribute_name`` declared in ``__init__``.
        - If attribute names match, then it adds all of attribute values to ``attribute_value_list``.

        :type tag: str
        :type attrs: list

        :param tag: The name of the HTML tag converted to lower case.
        :param attrs: List of tuple (name, value) pairs containing the attributes found inside the tag's ``<>``
            brackets.
        :return: None

        """
        # self.print_class_value(tag=tag, attrs=attrs)
        self.set_attribute_value_list(attrs)

    def handle_startendtag(self, tag, attrs):
        """
        | **Overrides HTMLParser method.**
        | https://docs.python.org/3.5/library/html.parser.html#html.parser.HTMLParser.handle_startendtag

        | **What is a startend tag?**
        | Tags like ``<img src="/image1.jpg" />`` or ``<br />`` that stand alone. They start and end themselves.

        - Gathers every attribute for every start--end tag in a given HTML file.
        - Filters the attribute for the ``attribute_name`` declared in ``__init__``.
        - If attribute names match, then it adds all of attribute values to ``attribute_value_list``.

        :type tag: str
        :type attrs: list

        :param tag: The name of the HTML tag converted to lower case.
        :param attrs: List of tuple (name, value) pairs containing the attributes found inside the tag's ``<>``
            brackets.
        :return: None

        """
        # self.print_class_value(tag=tag, attrs=attrs)
        self.set_attribute_value_list(attrs)

    def set_attribute_value_list(self, attrs):
        """
        Creates a ``list()`` of all string values in a HTML file with a ``name`` that matches ``self.attribute_name``.

        :param attrs: List of tuple (name, value) pairs containing the attributes found inside the tag's ``<>``
            brackets.
        :return: None

        """
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
    """
    Wraps ``HTMLAttributeParser()``, and uses it to get all of the values associated with HTML ``class`` attributes.

    Converts the list of space-delimited strings returned into a minimum ``set()`` of space-split strings, and assigns
    the value to ``self.class_set``.

    | **Parameters:**
    | **files** (*str*) -- A collection of strings containing the full path to each HTML file in the project.

    **Example:**

    >>> from os import getcwd
    >>> # Intended to be used in conjunction with the FileFinder
    >>> from filehandler import FileFinder
    >>> #
    >>> # Set project_directory to the one containing the files you
    >>> # want to DRY out.
    >>> project_directory = getcwd()
    >>> #
    >>> # Define File all file types/extensions to search for
    >>> # in project_directory
    >>> file_types = ('*.html', )
    >>> #
    >>> # Get all files associated with defined file_types
    >>> # in project_directory
    >>> file_finder = FileFinder(
    >>>     project_directory=project_directory, file_types=file_types
    >>> )
    >>> #
    >>> # Create set of all defined css class selectors.
    >>> class_parser = HTMLClassParser(files=file_finder.files)
    >>> #
    >>> # Get set of all defined css class selectors.
    >>> class_set = class_parser.class_set

    """
    def __init__(self, files):
        self.class_set = set()

        for _file in files:
            # Convert file to string.
            file_converter = FileConverter(file_path=_file)
            file_string = file_converter.get_file_as_string()
            # print(file_string)

            # Generate list of class strings
            class_parser = HTMLAttributeParser(attribute_name='class')
            class_parser.feed(file_string)

            # Convert list of class strings to set
            self.__set_class_set(class_parser.attribute_value_list)
            # print("Class List:\t", class_parser.attribute_value_list)
            # print(" Class Set:\t", self.class_set)

    def __set_class_set(self, attribute_value_list):
        """ Private Method

        Sets the value of ``self.class_set`` via the following steps:

        - Split space delimited string into set().
        - Unite the new set with class_set.
        - Assign union() to self.class_set.

        Using a ``set()`` allows for duplicate class names to be discarded.

        :param attribute_value_list: A ``list()`` of all string values in a HTML file with an attribute name
            of ``class``.
        :return: None

        """
        for value in attribute_value_list:
            self.class_set = set.union(
                set(value.split()),         # Split space delimited string into set().
                self.class_set              # Unite the new set with class_set.
            )                               # Assign union() to self.class_set.

