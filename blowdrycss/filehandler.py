# python 2 compatibility
from __future__ import print_function, unicode_literals
from builtins import str
from io import open
# builtins
from os import path, walk, getcwd, makedirs
from glob import glob
from re import sub, findall
# plugins
from cssutils import parseString, ser
# custom
try:
    from utilities import get_file_path
except ImportError:
    from blowdrycss.utilities import get_file_path

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class FileFinder(object):
    """
    Designed to find all ``files_types`` specified within a particular ``project_directory``. All folders within the
    ``project_directory`` are searched.

    | **Parameters:**

    | **project_directory** (*str*) -- Full path to the project directory containing parsable files e.g.
      ``/home/usr/web_project``.

    | **file_types** (*str tuple*) -- A tuple containing file extensions of project files to be parsed. Extensions
      are in the wildcard form ``'*.<ext>'``.  Replace ``<ext>`` with the desired file extension.

    **Example:**

    >>> from os import getcwd, chdir, path
    >>> current_dir = getcwd()
    >>> chdir('..')
    >>> project_directory = path.join(current_dir, 'examplesite')
    >>> chdir(current_dir)    # Change it back.
    >>> file_types = ('*.html', )
    >>> file_finder = FileFinder(
    >>>     project_directory=project_directory,
    >>>     file_types=file_types
    >>> )
    >>> files = file_finder.files

    """
    file_types = ('*.html', )

    def __init__(self, project_directory='', file_types=file_types):
        if path.isdir(project_directory):
            self.project_directory = project_directory
            self.file_types = file_types
            self.files = []
            print(u'Project Directory:', str(project_directory))
            print(u'\nFile Types:', ', '.join(self.file_types))

            self.set_files()
            print(u'\nProject Files Found:')
            self.print_collection(self.files)
        else:
            raise OSError(project_directory + ' is not a directory.')
            # raise NotADirectoryError(project_directory + ' is not a directory.') # python 3 only

    @staticmethod
    def print_collection(collection):
        """
        Takes a list or tuple as input and prints each item.

        :type collection: list

        :param collection: A list of unicode strings to be printed.
        :return: None

        """
        for item in collection:
            print(str(item))        # Python 2 requires str().

    def set_files(self):
        """
        Get all files associated with defined ``file_types`` in ``project_directory``. For each ``file_type`` find
        the full path to each file in the project directory of the current ``file_type``.  Add the full path of each
        file found to the list ``self.files``.

        Reference:
        stackoverflow.com/questions/954504/how-to-get-files-in-a-directory-including-all-subdirectories#answer-954948

        :return: None

        """
        for directory, _, _ in walk(self.project_directory):
            for file_type in self.file_types:
                self.files.extend(glob(path.join(directory, file_type)))


class FileConverter(object):
    """ Converts text files to strings.

    On initialization checks the existence of ``file_path``.

    **Example:**

    >>> from os import getcwd, chdir, path
    >>> # Valid file_path
    >>> current_dir = getcwd()
    >>> chdir('..')
    >>> file_path = path.join(current_dir, 'examplesite', 'index.html')
    >>> chdir(current_dir)    # Change it back.
    >>> file_converter = FileConverter(file_path=file_path)
    >>> file_string = file_converter.get_file_as_string()
    >>> #
    >>> # Invalid file_path
    >>> file_converter = FileConverter(file_path='/not/valid/file.html')
    FileNotFoundError: file_path /not/valid/file.html does not exist.

    """
    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self.file_path = file_path
        else:
            raise OSError('file_path ' + file_path + ' does not exist.')
            # raise FileNotFoundError('file_path ' + file_path + ' does not exist.')       # python 3 only

    def get_file_as_string(self):
        """ Convert the _file to a string and return it.

        :return: (*str*) Return the _file as a string.

        **Example:**

        >>> from os import getcwd, chdir, path
        >>> current_dir = getcwd()
        >>> chdir('..')
        >>> file_path = path.join(current_dir, 'examplesite', 'index.html')
        >>> chdir(current_dir)    # Change it back.
        >>> file_converter = FileConverter(file_path=file_path)
        >>> file_string = file_converter.get_file_as_string()
        """
        with open(self.file_path, 'r') as _file:
            file_as_string = _file.read().replace('\n', '')
        return file_as_string


class FileRegexMap(object):
    """
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

    | **Parameters:**

    | **_path** (*str*) -- Relative or full path to the parsable file.

    **Examples:**

    >>> from filehandler import FileRegexMap
    >>> file_regex_map = FileRegexMap(path='Default.aspx')
    >>> file_regex_map.regex_dict
    {
        'sub_regex': r'<%.*?%>',
        'findall_regex': r'class="(.*?)"'
    }

    """
    def __init__(self, _path=''):
        if path.isfile(_path):
            self._regex_dict = dict()
            self._path = _path.strip()                              # Remove external whitespace.
            self.name, self.extension = path.splitext(self._path)

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
            raise OSError(_path + ' does not exist.')

    def is_valid_extension(self):
        """ Validates the extension. Returns whether True or False based on whether the extension is a key in
        ``file_type_dict``.

        :return: (*bool*) -- Returns True if the extension is a key in file_type_dict. Returns False otherwise.
        """
        return self.extension in self.file_type_dict

    @property
    def regex_dict(self):
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

    >>> from filehandler import ClassExtractor
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


class CSSFile(object):
    """ A tool for writing and minifying CSS files.

    *Reference:*
    stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary#answer-14364249

    | **Parameters:**

    | **css_directory** (*str*) -- File directory where the .css and .min.css output files are stored.

    | **file_name** (*str*) -- The name of the CSS output file. Default is 'blowdry'. The output file
      is named blowdry.css or blowdry.min.css.

    | *Note:* ``file_name`` does not include extension because ``write_css()`` and ``minify()`` append the extension.

    **Example:**

    >>> from os import getcwd, chdir, path
    >>> current_dir = getcwd()
    >>> chdir('..')
    >>> project_directory = path.join(current_dir, 'examplesite')
    >>> css_directory = path.join(project_directory, 'css')
    >>> chdir(current_dir)    # Change it back.
    >>> css_text = '.margin-top-50px { margin-top: 3.125em }'
    >>> css_file = CSSFile(
    >>>     file_directory=css_directory, file_name='blowdry'
    >>> )
    >>> css_file.write(css_text=css_text)
    >>> css_file.minify(css_text=css_text)

    """
    def __init__(self, file_directory=getcwd(), file_name='blowdry'):
        self.file_directory = file_directory
        self.file_name = file_name

        try:                                        # Python 2.7 Compliant
            makedirs(file_directory)                # Make 'css' directory
        except OSError:
            if not path.isdir(file_directory):      # Verify directory existences
                raise OSError(file_directory + ' is not a directory, and could not be created.')

    def write(self, css_text=''):
        """ Output a human readable version of the css file in utf-8 format.

        **Notes:**

        - The file is human readable. It is not intended to be human editable as the file is auto-generated.
        - Pre-existing files with the same name are overwritten.

        :type css_text: str

        :param css_text: Text containing the CSS to be written to the file.
        :return: None

        **Example:**

        >>> css_text = '.margin-top-50px { margin-top: 3.125em }'
        >>> css_file = CSSFile()
        >>> css_file.write(css_text=css_text)

        """
        parse_string = parseString(css_text)
        ser.prefs.useDefaults()                # Enables Default / Verbose Mode
        file_path = get_file_path(file_directory=self.file_directory, file_name=self.file_name, extension='.css')
        with open(file_path, 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))

    def minify(self, css_text=''):
        """ Output a minified version of the css file in utf-8 format.

        **Definition:**

        The term minify "in the context of CSS means removing all unnecessary characters,
        such as spaces, new lines, comments without affecting the functionality of the source code."

        *Source:* https://www.jetbrains.com/phpstorm/help/minifying-css.html

        **Purpose:**

        | The purpose of minification is to increase web page load speed.
        | Reducing the size of the CSS file reduces
          the time spent downloading the CSS file and waiting for the page to load.

        **Notes:**

        - The file is minified and not human readable.
        - Pre-existing files with the same name are overwritten.
        - Uses the cssutils minification tool.

        **Important:**

        - ``ser.prefs.useMinified()`` is a global setting. It must be reset to ``ser.prefs.useDefaults()``. Otherwise,
          minification will continue to occur. This can result in strange behavior especially during unit testing or
          in code called after this method is called.

        :type css_text: str

        :param css_text: Text containing the CSS to be written to the file.
        :return: None

        **Example:**

        >>> css_text = '.margin-top-50px { margin-top: 3.125em }'
        >>> css_file = CSSFile()
        >>> css_file.minify(css_text=css_text)

        """
        parse_string = parseString(css_text)
        ser.prefs.useMinified()                 # Enable minification.
        file_path = get_file_path(file_directory=self.file_directory, file_name=self.file_name, extension='.min.css')
        with open(file_path, 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))
        ser.prefs.useDefaults()                 # Disable minification.


class GenericFile(object):
    """ A tool for writing extension-independent files.

    **Reference:**
    stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary#answer-14364249

    | **Parameters:**

    | **file_directory** (*str*) -- File directory where the output files are saved / overwritten.

    | **file_name** (*str*) -- The name of the output file. Default is 'blowdry'.

    | **extension** (*str*) -- A file extension that begins with a ``.`` and only contains ``.``, ``0-9`` or ``a-z``.

    | *Notes:*

    - ``file_name`` does not include extension because ``write_file()`` normalizes and appends the extension.
    - ``extension`` is converted to lowercase.

    **Example:**

    >>> from os import getcwd, path
    >>> file_directory = path.join(getcwd())
    >>> css_text = '.margin-top-50px { margin-top: 3.125em }'
    >>> markdown_file = GenericFile(
    >>>     file_directory=file_directory,
    >>>     file_name='blowdry',
    >>>     extension='.md'
    >>> )
    >>> text = '# blowdrycss'
    >>> markdown_file.write(text=text)

    """
    def __init__(self, file_directory=getcwd(), file_name='', extension=''):
        self.file_directory = str(file_directory)
        self.file_name = str(file_name)
        self.file_path = get_file_path(
                file_directory=self.file_directory,
                file_name=self.file_name,
                extension=str(extension)
        )
        try:                                        # Python 2.7 Compliant
            makedirs(file_directory)                # Make 'html' directory
        except OSError:
            if not path.isdir(file_directory):      # Verify directory existences
                raise OSError(file_directory + ' is not a directory, and could not be created.')

    def write(self, text=''):
        """ Output a human readable version of the file in utf-8 format.

        Converts string to bytearray so that no new lines are added to the file.
        Note: Overwrites any pre-existing files with the same name.

        :raises TypeError: Raise a TypeError if ``text`` input is not of type ``str``.

        :type text: unicode or str
        :param text: The text to be written to the file.
        :return: None

        """
        if type(text) is str:
            with open(self.file_path, 'wb') as generic_file:
                generic_file.write(bytearray(text, 'utf-8'))
        else:
            raise TypeError('In GenericFile.write() "' + text + '" input must be a str type.')
