# python 2 compatibility
from __future__ import absolute_import, unicode_literals
from io import open
from builtins import str
# builtins
from os import path
from re import sub, findall, IGNORECASE
import logging
# custom


class FileRegexMap(object):
    """ Given a file path including the file extension it maps the detected file extension to a regex pattern.

    **Process:**

    - Comments, template variables, or javascript syntax patterns are removed/replaced first with re.sub().

    - Class selector sets are extracted using re.findall().

    **Supported Javascript, Typescript, VueJs vue-loader extensions:** .js, .ts, .vue

    Javascript has a number of cases where a special substitution is performed. These cases are stored in ``js_case``.
    A check is performed if the re.sub() should do a special substitution of text that begins with the ``js_substring``.
    The ``js_substring`` helps to uniquely designate the locations of class selector sets.

    Javascript can occur in a standalone file or embedded <script> tags inside a file of another type.

    **Supported HTML extension:** .html

    HTML comments are removed.

    **Supported jinja and django template extensions:** .jinja, .jinja2, .jnj, .ja, .djt, .djhtml

    **Jinja sub_regexes regex explained:**

    | Remove {{...}} and {%...%} where '...' is any character.
    | ``{`` -- Substring must start with ``{``.
    | ``.*`` -- Matches any character.
    | ``?`` -- Do not be greedy.
    | ``}`` -- Match with an ending ``}``.
    | ``?}`` -- Optionally allow one more ``}``

    **Supported XHTML, asp.net, c#, and ruby template extensions:** .aspx, .ascx, .master, .cs, .erb

    **XHTML sub_regexes regex explained:**

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
        'sub_regexes': r'<%.*?%>',
        'findall_regexes': r'class="(.*?)"'
    }

    """
    def __init__(self, file_path=''):
        self.file_path = file_path.strip()                                      # Remove external whitespace.
        self._regex_dict = dict()
        self.name = ''
        self.extension = ''
        self.js_replacement = r''
        self.js_case = ()
        self.file_type_dict = dict()

        if path.isfile(self.file_path):
            self.name, self.extension = path.splitext(self.file_path)

            sub_uri = (r'://', )                            # URIs (http://, ftp://) resemble inline JS comments (//)

            js_substring = r'extract__class__set'
            self.js_replacement = js_substring + r'("'

            self.js_case = (
                r'(domClass.add\(\s*.*?,\s*["\'])',                             # dojo
                r'(domClass.add\(\s*.*?,\s*["\'])',
                r'(dojo.addClass\(\s*.*?,\s*["\'])',
                r'(domClass.remove\(\s*.*?,\s*["\'])',
                r'(dojo.removeClass\(\s*.*?,\s*["\'])',
                r'(YAHOO.util.Dom.addClass\(\s*.*?,\s*["\'])',                  # yui
                r'(YAHOO.util.Dom.hasClass\(\s*.*?,\s*["\'])',
                r'(YAHOO.util.Dom.removeClass\(\s*.*?,\s*["\'])',
                r'(.addClass\(\s*["\'])',                                       # jquery
                r'(.removeClass\(\s*["\'])',
                r'(\$\(\s*["\']\.)',
            )

            sub_js = (
                r'//.*?\n',                                                     # Remove JS Comments.
                r'\n',                                                          # Remove new lines before block quotes.
                r'/\*.*?\*/',                                                   # Remove block quotes.
                r'(domClass.add\(\s*.*?,\s*["\'])',                             # dojo
                r'(domClass.add\(\s*.*?,\s*["\'])',
                r'(dojo.addClass\(\s*.*?,\s*["\'])',
                r'(domClass.remove\(\s*.*?,\s*["\'])',
                r'(dojo.removeClass\(\s*.*?,\s*["\'])',
                r'(YAHOO.util.Dom.addClass\(\s*.*?,\s*["\'])',                  # yui
                r'(YAHOO.util.Dom.hasClass\(\s*.*?,\s*["\'])',
                r'(YAHOO.util.Dom.removeClass\(\s*.*?,\s*["\'])',
                r'(.addClass\(\s*["\'])',                                       # jquery
                r'(.removeClass\(\s*["\'])',
                r'(\$\(\s*["\']\.)',
            )
            sub_html = sub_uri + sub_js + (r'<!--.*?-->', )
            sub_jinja = (r'{.*?}?}', ) + sub_html + (r'{#.*?#}', )
            sub_csharp = (r'//.*?\n', r'\n', r'/\*.*?\*/', )                    # Remove CS comments.
            sub_dotnet = sub_html + (r'<%--.*?--%>', r'<%.*?%>', )              # Remove XHTML comments before elements.
            sub_ruby = sub_html + (r'<%--.*?--%>', r'<%.*?%>', )                # Remove XHTML comments before elements.
            sub_php = sub_html                                                  # Treat PHP like HTML and JS.

            class_regex = (r'class=[\'"](.*?)["\']', )                          # general 'class' case

            findall_regex_js = (
                r'.classList.add\(\s*[\'"](.*?)["\']\s*\)',
                r'.classList.remove\(\s*[\'"](.*?)["\']\s*\)',
                r'.className\s*\+?=\s*.*?[\'"](.*?)["\']',
                r'.getElementsByClassName\(\s*[\'"](.*?)["\']\s*\)',
                r'.setAttribute\(\s*[\'"]class["\']\s*,\s*[\'"](.*?)["\']\s*\)',
                js_substring + r'\(\s*[\'"](.*?)["\']\s*\)',                    # Find cases designated by js_substring.
            )

            findall_regex_cs = class_regex + (
                r'.CssClass\s*\+?=\s*.*?[\'"](.*?)["\']',
                r'.Attributes.Add\(\s*[\'"]class["\'],\s*.*?[\'"](.*?)["\']\s*\)',
            )

            findall_regex = class_regex + findall_regex_js

            self.file_type_dict = {
                '.js': {
                    'sub_regexes': sub_js,
                    'findall_regexes': findall_regex,
                },
                '.ts': {                                                        # Typescript
                    'sub_regexes': sub_js,
                    'findall_regexes': findall_regex,
                },
                '.vue': {                                                       # VueJs modular vue-loader
                    'sub_regexes': sub_html,
                    'findall_regexes': findall_regex,
                },
                '.html': {
                    'sub_regexes': sub_html,
                    'findall_regexes': findall_regex,
                },
                '.jinja': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.jinja2': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.jnj': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.ja': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.djt': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.djhtml': {
                    'sub_regexes': sub_jinja,
                    'findall_regexes': findall_regex,
                },
                '.cs': {
                    'sub_regexes': sub_csharp,
                    'findall_regexes': findall_regex_cs,
                },
                '.aspx': {
                    'sub_regexes': sub_dotnet,
                    'findall_regexes': findall_regex,
                },
                '.ascx': {
                    'sub_regexes': sub_dotnet,
                    'findall_regexes': findall_regex,
                },
                '.master': {
                    'sub_regexes': sub_dotnet,
                    'findall_regexes': findall_regex,
                },
                '.erb': {
                    'sub_regexes': sub_ruby,
                    'findall_regexes': findall_regex,
                },
                '.php': {
                    'sub_regexes': sub_php,
                    'findall_regexes': findall_regex,
                }
            }
        else:
            raise OSError('"' + self.file_path + '" does not exist.')

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
    """ Given a file_regex_map of any type along with a substitution regex patterns and a findall regex patterns.
    Returns a minimum set of class selectors as ``class_set``.

    | **Parameters:**

    | **file_path** (*str*) -- Path to the file_regex_map to be parsed.

    | **sub_pattern** (*tuple of regexes*) -- Zero or more regex patterns to be removed from the file_regex_map text
      before further processing.

    | **findall_pattern** (*tuple of regexes*) -- Zero or more regex patterns used to find all class selectors
      in a given file.

    **Example Usage:**

    >>> from blowdrycss.classparser import ClassExtractor
    >>> # Assuming Default.aspx is located in the same directory
    >>> aspx_file = 'Default.aspx'
    >>> aspx_sub = r'<%.*?%>'
    >>> aspx_findall = r'class="(.*?)"'
    >>> class_extractor = ClassExtractor(file_path=aspx_file)
    >>> class_extractor.class_set
    {'row', 'padding-top-30', 'padding-bottom-30', 'bgc-green'}
    >>> jinja2_file = 'index.jinja2'
    >>> jinja2_sub = r'{.*?}?}'
    >>> jinja2_findall = r'class="(.*?)"'
    >>> class_extractor = ClassExtractor(file_path=jinja2_file, sub_regexes=jinja2_sub, findall_regexes=jinja2_findall)
    >>> class_extractor.class_set
    {'purple', 'padding-left-5', 'squirrel', 'text-align-center', 'large-up', 'border-1', 'row', 'text-align-center'}

    """
    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self.file_path = file_path
            self.file_regex_map = FileRegexMap(file_path=file_path)
            regex_dict = self.file_regex_map.regex_dict
            self.sub_regexes = regex_dict['sub_regexes']
            self.findall_regexes = regex_dict['findall_regexes']
        else:
            raise OSError('"' + file_path + '" does not exist.')

    @property
    def raw_class_list(self):
        """ Uses all sub_regexs and findall_regexes to extract space-delimited CSS class selector strings.
        Raw means space-delimited.

        Example: Look for the findall_regexes 'class="..."'. Extract the '...' part.

        sub_regexes() is used to remove template variables from quoted class selector strings in file text.
        findall_regexes() is used to find all class selector strings in a given files text.

        :return: (*list of strings*) -- Returns a list of raw class selector strings.

        """
        class_list = []
        with open(self.file_path, 'r', encoding='utf-8') as _file:
            text = _file.read()
            for sub_regex in self.sub_regexes:                                      # Remove everything first.
                if sub_regex in self.file_regex_map.js_case:
                    text = sub(sub_regex, self.file_regex_map.js_replacement, text)
                else:
                    text = sub(sub_regex, '', text)
            for findall_regex in self.findall_regexes:                              # Find everything second.
                class_list += findall(findall_regex, text, IGNORECASE)              # Allow CamelCase i.e. ClaSs="bold"
            logging.debug('classectractor.rawclasslist text: ' + text)
        return class_list

    @property
    def class_set(self):
        """ Reduce the list of quoted class selector strings to a minimum set of classes. Returns the ``class_set``.

        :return: (*set of strings*) -- Return the minimum set of individual class selector strings.

        """
        class_set = set()

        logging.debug(msg='classextractor.raw_class_list:\t' + str(self.raw_class_list))
        for classes in self.raw_class_list:
            class_set = set.union(
                set(classes.split()),               # Split space delimited string into set().
                class_set                           # Unite the new set with class_set.
            )                                       # Assign union() to class_set.
        logging.debug(msg='classextractor.class_set:\t' + str(class_set))
        return class_set


class ClassParser(object):
    """ Parses all project files provided by file_dict. All file types are sent to ``ClassExtractor`` as of v0.1.7.

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
        self.class_set = set()
        self.file_dict = file_dict
        self.file_path_list = []
        self.build_file_path_list()

        logging.debug(msg='classparser.html_class_parser.class_set:\t' + str(self.class_set))
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
            class_extractor = ClassExtractor(file_path=file_path)
            logging.debug(msg='classparser.class_extractor.class_set:\t' + str(class_extractor.class_set))
            self.class_set = self.class_set.union(class_extractor.class_set)
        logging.debug(msg='classparser final class_set:\t' + str(self.class_set))
