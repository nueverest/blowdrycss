# python 2 compatibility
from __future__ import print_function, unicode_literals
from io import open
# builtins
from os import path
from re import sub, findall
# custom
from blowdrycss.htmlparser import HTMLClassParser


class FileRegexMap(object):
    """ Given a file path including the file extension it maps the detected file extension to a regex pattern.

    **Supported jinja and django template extensions:** jinja, jinja2, jnj, ja, djt, djhtml

    **Jinja sub_regex regex explained:**

    | Remove {{...}} and {%...%} where '...' is any character.
    | ``{`` -- Substring must start with ``{``.
    | ``.*`` -- Matches any character.
    | ``?`` -- Do not be greedy.
    | ``}`` -- Match with an ending ``}``.
    | ``?}`` -- Optionally allow one more ``}``

    **Supported XHTML, asp.net, and ruby template extensions:** .aspx, .ascx, .master, .erb

    **XHTML sub_regex regex explained:**

    | Remove <%...%> patterns where '...' is any character
    | ``<%`` -- Substring must start with ``<%``.
    | ``.*`` -- Matches any character.
    | ``?`` -- Do not be greedy.
    | ``%>`` -- Substring must end with ``%>``.

    | **Raises OSError** if the ``_path`` does not exist.

    | **Parameters:**

    | **_path** (*str*) -- Relative or full path to the parsable file.

    **Examples:**

    >>> from blowdrycss.classparser import FileRegexMap
    >>> file_regex_map = FileRegexMap(path='Default.aspx')
    >>> file_regex_map.regex_dict
    {
        'sub_regex': r'<%.*?%>',
        'findall_regex': r'class="(.*?)"'
    }

    """
    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self._regex_dict = dict()
            self.file_path = file_path.strip()                              # Remove external whitespace.
            self.name, self.extension = path.splitext(self.file_path)

            html_sub = r''
            jinja_sub = r'{.*?}?}'
            django_sub = r'{.*?}?}'
            dotnet_sub = r'<%.*?%>'
            ruby_sub = r'<%.*?%>'

            findall_regex = r'class="(.*?)"'

            self.file_type_dict = {
                '.html': {
                    'sub_regex': html_sub,
                    'findall_regex': findall_regex,
                },
                '.jinja': {
                    'sub_regex': jinja_sub,
                    'findall_regex': findall_regex,
                },
                '.jinja2': {
                    'sub_regex': jinja_sub,
                    'findall_regex': findall_regex,
                },
                '.jnj': {
                    'sub_regex': jinja_sub,
                    'findall_regex': findall_regex,
                },
                '.ja': {
                    'sub_regex': jinja_sub,
                    'findall_regex': findall_regex,
                },
                '.djt': {
                    'sub_regex': django_sub,
                    'findall_regex': findall_regex,
                },
                '.djhtml': {
                    'sub_regex': django_sub,
                    'findall_regex': findall_regex,
                },
                '.aspx': {
                    'sub_regex': dotnet_sub,
                    'findall_regex': findall_regex,
                },
                '.ascx': {
                    'sub_regex': dotnet_sub,
                    'findall_regex': findall_regex,
                },
                '.master': {
                    'sub_regex': dotnet_sub,
                    'findall_regex': findall_regex,
                },
                '.erb': {
                    'sub_regex': ruby_sub,
                    'findall_regex': findall_regex,
                },
            }
        else:
            raise OSError(file_path + ' does not exist.')

    def is_valid_extension(self):
        """ Validates the extension. Returns whether True or False based on whether the extension is a key in
        ``file_type_dict``.

        :return: (*bool*) -- Returns True if the extension is a key in file_type_dict. Returns False otherwise.
        """
        return self.extension in self.file_type_dict

    @property
    def regex_dict(self):
        """ Validates ``self.extension`` and returns the associated regex dictionary for that extension.

        :return: Returns the regular expression dictionary associated with ``self.extension``.

        """
        self.is_valid_extension()
        return self.file_type_dict[self.extension]


class ClassExtractor(object):
    """ Given a file_regex_map of any type along with a substitution regex pattern and a findall_regex regex pattern. Return
    a minimum set of classes.

    | **Parameters:**

    | **file_path** (*str*) -- Path to the file_regex_map to be parsed.

    | **sub_pattern** (*regex*) -- Regex pattern to be removed from the file_regex_map text before further processing.

    | **findall_pattern** (*regex*) -- Regex pattern used to find all class selector assignments in a given file.

    **Example Usage:**

    >>> from blowdrycss.classparser import ClassExtractor
    >>> # Assuming Default.aspx is located in the same directory
    >>> aspx_file = 'Default.aspx'
    >>> aspx_sub = r'<%.*?%>'
    >>> aspx_findall = r'class="(.*?)"'
    >>> class_extractor = ClassExtractor(file_path=aspx_file, sub_regex=aspx_sub, findall_regex=aspx_findall)
    >>> class_extractor.class_set
    {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
    >>> jinja2_file = 'index.jinja2'
    >>> jinja2_sub = r'{.*?}?}'
    >>> jinja2_findall = r'class="(.*?)"'
    >>> class_extractor = ClassExtractor(file_path=jinja2_file, sub_regex=jinja2_sub, findall_regex=jinja2_findall)
    >>> class_extractor.class_set
    {'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row', 'text-align-center'}

    """
    def __init__(self, file_path='', sub_regex=r'', findall_regex=r''):
        if path.isfile(file_path):
            self.file_path = file_path
            self.sub_regex = sub_regex
            self.findall_regex = findall_regex
        else:
            raise OSError(file_path + ' does not exist.')

    @property
    def raw_class_list(self):
        """ Look for the findall_regex 'class="..."'. Extract the '...' part.

        sub_regex() is used to remove template variables from quoted class selector strings from file text.
        findall_regex() is used to find all class selector strings in a given files text.

        :return: (*list of strings*) -- Returns a list of raw class selector strings.

        """
        with open(self.file_path, 'r', encoding='utf-8') as _file:
            text = _file.read()
            text = sub(self.sub_regex, '', text)
            return findall(self.findall_regex, text)

    @property
    def class_set(self):
        """ Reduce the list of quoted class selector strings to a minimum set of classes. Returns the ``class_set``.

        :return: (*set of strings*) -- Return the minimum set of individual class selector strings.

        """
        class_set = set()

        print(self.raw_class_list)
        for classes in self.raw_class_list:
            class_set = set.union(
                set(classes.split()),               # Split space delimited string into set().
                class_set                           # Unite the new set with class_set.
            )                                       # Assign union() to class_set.
        return class_set


class ClassParser(object):
    """ Parses all project files provided by file_dict. HTML files are sent to ``HTMLClassParser``, and all other
    file types are sent to ``ClassExtractor``.

    **Parameters**

    **file_dict** (*dict*) -- Expecting FileFinder.file_dict as input.

    **Returns** None

    **Example**

    >>> from os import getcwd, chdir, path
    >>> from blowdrycss.filehandler import FileFinder
    >>> from blowdrycss.classparser import ClassParser
    >>> current_dir = getcwd()
    >>> chdir('..')
    >>> project_directory = path.join(current_dir, 'examplesite')
    >>> chdir(current_dir)    # Change it back.
    >>> file_finder = FileFinder(project_directory=project_directory)
    >>> file_dict = file_finder.file_dict
    >>> general_class_parser = ClassParser(file_dict=file_dict)
    >>> general_class_parser.class_set
    { Returns a complete set of all the classes discovered after looking in at all file paths. }

    """
    def __init__(self, file_dict):
        self.html_class_parser = HTMLClassParser(files=file_dict['.html'])

        # Exclude 'html' files. They are already handled on the line above.
        if '.html' in file_dict:
            del file_dict['.html']

        self.file_dict = file_dict

        self.file_path_list = []
        self.build_file_path_list()

        self.class_set = self.html_class_parser.class_set
        self.build_class_set()

    def build_file_path_list(self):
        """ Builds a list of all of the file paths regardless of type.

        :return: None

        """
        keys = list(self.file_dict)
        for key in keys:
            self.file_path_list += self.file_dict[key]

    def build_class_set(self):
        """ Builds a complete set of all the classes discovered after looking in at all file paths.

        :return: None

        """
        for file_path in self.file_path_list:
            file_regex_map = FileRegexMap(file_path=file_path)
            regex_dict = file_regex_map.regex_dict
            sub_regex = regex_dict['sub_regex']
            findall_regex = regex_dict['findall_regex']
            class_extractor = ClassExtractor(file_path=file_path, sub_regex=sub_regex, findall_regex=findall_regex)
            self.class_set = self.class_set.union(class_extractor.class_set)
