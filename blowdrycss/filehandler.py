# python 2
from __future__ import absolute_import, print_function, unicode_literals, with_statement
from builtins import str
from io import open

# builtins
from os import path, walk, getcwd
from glob import glob
import logging

# plugins
from cssutils import parseString, ser

# custom
from blowdrycss.utilities import get_file_path, make_directory
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class FileFinder(object):
    """
    Designed to find all ``settings.files_types`` specified within a particular ``project_directory``.
    All folders within the ``project_directory`` are searched.

    | **Parameters:**

    | **recent** (*str*) -- Flag that indicates whether to gather the most recently modified files (True Case)
      or all eligible files (False Case).

    | **Members:**

    | **project_directory** (*str*) -- Set to settings.project_directory.

    | **files** (*str list*) -- List of all paths to all parsable files.

    | **file_dict** (*dict*) -- Dictionary of all paths to all parsable files where the file extension e.g. ``*.html``
      is the key and the full file path is the value.

    **Example:**

    >>> file_finder = FileFinder(recent=False)
    >>> files = file_finder.files

    """
    def __init__(self, recent=True):
        self.project_directory = settings.project_directory
        if path.isdir(self.project_directory):
            self.recent = recent

            self.files = []
            self.set_files()

            self.file_dict = {}
            if self.recent:
                self.set_recent_file_dict()
            else:
                self.set_file_dict()

            logging.debug(msg='File Types:' + ', '.join(settings.file_types))
            logging.debug(msg='Project Directory:' + str(self.project_directory))
            logging.debug('\nProject Files Found:')
            self.print_collection(self.files)
        else:
            raise OSError(
                self.project_directory +
                ' is not a directory. Check project_directory setting in blowdrycss_settings.py'
            )

    @staticmethod
    def print_collection(collection):
        """
        Takes a list or tuple as input and prints each item.

        :type collection: iterable

        :param collection: A list or tu of unicode strings to be printed.
        :return: None

        """
        for item in collection:
            logging.debug(str(item))        # Python 2 requires str().
        logging.debug(' ')                  # Add a blank line

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
            for file_type in settings.file_types:
                self.files.extend(glob(path.join(directory, file_type)))

    def set_file_dict(self):
        """ Filter and organize files by type in ``file_dict``.

        Dictionary Format: ::

            self.file_dict = {
                '.html': {'filepath_1.html', 'filepath_2.html', ..., 'filepath_n.html'},
                '.aspx': {'filepath_1.aspx', 'filepath_2.aspx', ..., 'filepath_n.aspx'},
                ...
                '.file_type': {'filepath_1.file_type', 'filepath_2.file_type', ..., 'filepath_n.file_type'},
            }

        Automatically removes the * wildcard from ``file_type``.

        :return: None

        """
        for file_type in settings.file_types:
            file_type = file_type.replace('*', '')  # Remove the * wildcard.
            self.file_dict[file_type] = {_file for _file in self.files if path.splitext(_file)[1] == file_type}

    def set_recent_file_dict(self):
        """ Filter and organize recent files by type in ``file_dict``. Meaning only files that are newer than
        the latest version of blowdry.css are added.

        Dictionary Format: ::

            self.file_dict = {
                '.html': {'filepath_1.html', 'filepath_2.html', ..., 'filepath_n.html'},
                '.aspx': {'filepath_1.aspx', 'filepath_2.aspx', ..., 'filepath_n.aspx'},
                ...
                '.file_type': {'filepath_1.file_type', 'filepath_2.file_type', ..., 'filepath_n.file_type'},
            }

        Automatically removes the * wildcard from ``file_type``.

        :return: None

        """
        comparator = FileModificationComparator()
        for file_type in settings.file_types:
            file_type = file_type.replace('*', '')  # Remove the * wildcard.
            self.file_dict[file_type] = {
                _file for _file in self.files if path.splitext(_file)[1] == file_type and comparator.is_newer(_file)
            }


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


class CSSFile(object):
    """ A tool for writing and minifying CSS to files.

    *Reference:*
    stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary#answer-14364249

    | **Parameters:**

    | **css_directory** (*str*) -- File directory where the .css and .min.css output files are stored.

    | **Members:**

    | **file_name** (*str*) -- Defined in blowdrycss_settings.py as ``output_file_name``. Default is 'blowdry'.

    | **extension** (*str*) -- Defined in blowdrycss_settings.py as ``output_extension``. Default is '.css'.

    | *Note:* The output file is named ``file_name + extension`` or ``file_name + .min + extension``.
      ex1: blowdry.css or blowdry.min.css
      ex2: _custom.scss or _custom.min.scss

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
    def __init__(self):
        self.file_directory = settings.css_directory
        self.file_name = settings.output_file_name
        self.extension = settings.output_extension
        make_directory(self.file_directory)

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
        file_path = get_file_path(
            file_directory=self.file_directory,
            file_name=self.file_name,
            extension=self.extension
        )
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
        ser.prefs.useMinified()                                     # Enable minification.
        file_path = get_file_path(
            file_directory=self.file_directory,
            file_name=self.file_name,
            extension=str('.min' + self.extension)                  # prepend '.min'
        )
        with open(file_path, 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))
        ser.prefs.useDefaults()                                     # Disable minification.


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
        make_directory(file_directory)

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


class FileModificationComparator(object):
    """ A Comparator that compares the last modified time of blowdry.css with the last modified time of another file.

    :return: None

    **Example**

    >>> import blowdrycss_settings as settings
    >>> from blowdrycss.filehandler import FileModificationComparator
    >>> file_age_comparator = FileModificationComparator()
    >>> print(file_age_comparator.is_newer(file_path=path.join(settings.project_directory, '/index.html'))

    """
    def __init__(self):
        self.blowdrycss_file = path.join(settings.css_directory, 'blowdry.css')
        self.blowdrymincss_file = path.join(settings.css_directory, 'blowdry.min.css')

    def is_newer(self, file_path):
        """ Detects if ``self.file_path`` was modified more recently than blowdry.css.  If ``self.file_path`` is
        newer than blowdry.css or blowdry.min.css it returns True otherwise it returns false.

        If blowdry.css or blowdry.min.css do not exist, then the file under comparison is newer.

        :type file_path: str
        :param file_path: The full path to a file.
        :return: (*bool*) Returns True if modification time of blowdry.css or blowdry.min.css do not exist, or are older
            i.e. less than the ``self.file_path`` under consideration.
        """
        if settings.human_readable:
            try:
                a = path.getmtime(self.blowdrycss_file)
            except OSError:                                                                     # file doesn't exist
                return True
        elif settings.minify:
            try:
                a = path.getmtime(self.blowdrymincss_file)
            except OSError:                                                                     # file doesn't exist
                return True
        else:
            raise SystemError(
                'Review blowdrycss_settings.py. Either settings.human_readable or settings.minify must be set to True.'
            )

        try:
            b = path.getmtime(file_path)
        except OSError:
            raise OSError('"' + file_path + '" does not exist.')

        return a <= b
