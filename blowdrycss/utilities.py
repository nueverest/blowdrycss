# python 2
from __future__ import absolute_import, print_function, division, unicode_literals
from builtins import str, round

# builtins
from re import search, findall
from inspect import currentframe
from os import path, stat, getcwd, makedirs, remove
import logging

# custom
import blowdrycss_settings as settings


__author__ = 'chad nelson'
__project__ = 'blowdrycss'


def contains_a_digit(string=''):
    """
    Check if string contains a digit ``[0-9]``.

    :type string: str

    :param string: The string to test.
    :return: (bool) -- Returns True if string contains at least 1 digit. Otherwise, returns False.

    **Examples:**

    >>> contains_a_digit('abc1')
    True
    >>> contains_a_digit('876')
    True
    >>> contains_a_digit('cat')
    False
    >>> contains_a_digit('')
    False
    >>> contains_a_digit('   ')
    False

    """
    return True if search(r"[0-9]", string) else False


def deny_empty_or_whitespace(string='', variable_name=''):
    """
    Prevent ``string`` or ``variable_name`` from being empty or only containing whitespace.

    :raises ValueError: Raises a ValueError if the string or the variable_name is empty or only contains whitespace.
        The ValueError contains the name of the calling function and the variable name used in the calling function.

    :type string: str
    :type variable_name: str

    :param string: The string to test.
    :param variable_name: The name of the variable used in the calling function.
    :return: None

    """
    if not variable_name:                                                                       # '' and None cases
        calling_function = currentframe().f_back.f_code.co_name
        raise ValueError(calling_function + ': variable_name input cannot be empty or None.')
    if not variable_name.strip():                                                               # whitespace case
        calling_function = currentframe().f_back.f_code.co_name
        raise ValueError(calling_function + ': variable_name input cannot only contain whitespace.')

    if not string:                                                                              # '' and None cases
        calling_function = currentframe().f_back.f_code.co_name
        raise ValueError(calling_function + ':', variable_name, 'cannot be empty or None.')
    if not string.strip():                                                                      # whitespace case
        calling_function = currentframe().f_back.f_code.co_name
        raise ValueError(calling_function + ':', variable_name, 'cannot only contain whitespace.')


def get_file_path(file_directory='', file_name='blowdry', extension=''):
        """ Joins the ``file_directory``, ``file_name``, and ``extension``. Returns the joined file path.

        **Rules:**

        - Do not allow ``''`` empty input for ``file_directory``, ``file_name``, or ``extension``.
        - Transform extension to lowercase.
        - Extensions must match this regex r"(^[.][.0-9a-z]*[0-9a-z]$)".

        **Findall regex Decoded:**

        - ``r"(^[.][.0-9a-z]*[0-9a-z]$)"``
        - ``^[.]`` -- ``extension`` must begin with a ``.`` dot.
        - ``[.0-9a-z]*`` -- ``extension`` may contain any of the character inside the brackets.
        - ``[0-9a-z]$`` -- ``extension`` may only end with the characters inside the brackets.

        :type file_directory: str
        :type file_name: str
        :type extension: str

        :param file_directory: Directory in which to place the file.
        :param file_name: Name of the file (excluding extension)
        :param extension: A file extension including the ``.``, for example, ``.css``, ``.min.css``, ``.md``,
            ``.html``, and ``.rst``
        :return: (*str*) -- Returns the joined file path.

        """
        deny_empty_or_whitespace(string=file_directory, variable_name='file_directory')
        deny_empty_or_whitespace(string=file_name, variable_name='file_name')

        extension = extension.lower()
        regex = r"(^[.][.0-9a-z]*[0-9a-z]$)"
        if len(findall(regex, extension)) == 1:
            return path.join(file_directory, file_name + extension)
        else:
            raise ValueError(
                'Extension: ' + extension + ' contains invalid characters. Only ".", "0-9", and "a-z" are allowed.'
            )


def validate_output_file_name_setting():
    """ Validates output_file_name from blowdrycss_settings.py. First thing that runs.

    :raises SyntaxError: If settings.output_file_name or settings.output_extension contain
        '\', '/', whitespace or ends with a dot.

    :return: None
    """
    output_file_name = settings.output_file_name

    if search(r"\s", output_file_name):             # Prevent whitespace
        raise SyntaxError(
            'The output_file_name "' + output_file_name + '" in blowdrycss_settings.py must not contain whitespace.'
        )

    invalid_chars = ['\\', '/']            # Prevent '\' and '/'
    for invalid_char in invalid_chars:
        if invalid_char in output_file_name:
            raise SyntaxError(
                'The output_file_name "' + output_file_name + '" in blowdrycss_settings.py must not contain / or \.'
            )

    if output_file_name.endswith('.'):              # Prevent final '.'
        raise SyntaxError(
            'The output_file_name "' + output_file_name + '" in blowdrycss_settings.py must not end with a dot.'
        )


def validate_output_extension_setting():
    """ Validates output_extension from blowdrycss_settings.py. First thing that runs.

    :raises SyntaxError: If settings.output_extension does not begin with a dot or contains '\', '/', whitespace
        or ends with a dot.

    :return: None
    """
    output_extension = settings.output_extension

    if not output_extension.startswith('.'):
        raise SyntaxError(
            'The output_extension "' + output_extension + '" in blowdrycss_settings.py must begin with a dot.'
        )

    if search(r"\s", output_extension):             # Prevent whitespace
        raise SyntaxError(
            'The output_extension "' + output_extension + '" in blowdrycss_settings.py must not contain whitespace.'
        )

    invalid_chars = ['\\', '/']                     # Prevent '\' and '/'
    for invalid_char in invalid_chars:
        if invalid_char in output_extension:
            raise SyntaxError(
                'The output_extension "' + output_extension + '" in blowdrycss_settings.py must not contain / or \.'
            )

    if output_extension.endswith('.'):              # Prevent final '.'
        raise SyntaxError(
            'The output_extension "' + output_extension + '" in blowdrycss_settings.py must not end with a dot.'
        )


def change_settings_for_testing():
    """ Change settings directories for testing.

    .. warning::

        This method should only be used by the unit_test framework.

    :return: None

    """
    cwd = getcwd()

    # The if/else logic is required for unit testing.
    if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
        settings.markdown_directory = path.join(cwd, 'test_markdown')
        settings.project_directory = path.join(cwd, 'test_examplesite')
        settings.css_directory = path.join(settings.project_directory, 'test_css')
        settings.docs_directory = path.join(cwd, 'test_docs')
    else:                                                       # Run unittest cmd from the root directory.
        settings.markdown_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_markdown')
        settings.project_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite')
        settings.css_directory = path.join(settings.project_directory, 'test_css')
        settings.docs_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_docs')


def unittest_file_path(folder='', filename=''):
    """ Determines the path of assigned to the folder and file based on the directory in which the unittest command
    is executed.

    :type folder: str
    :type filename: str

    :param folder: Name of the folder where the file is located.
    :param filename: Name of the file including extension e.g. test_aspx.aspx

    :return: (*str*) -- Return the path of the file to test.

    """
    cwd = getcwd()

    if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
        the_path = path.join(cwd, folder, filename)
    else:                                                       # Run unittest cmd from the root directory.
        the_path = path.join(cwd, 'blowdrycss', 'unit_tests', folder, filename)

    return the_path


def print_minification_stats(file_name='', extension=''):
    """ Print before and after minification file size reduction statistics.

    :type file_name: str
    :param file_name: The file name excluding extension e.g. 'blowdry' or 'site'.
    :type extension: str
    :param extension: Appended to the file_name and begins with a dot e.g. '.css', '.scss', etc.
    :return: None

    """
    original_file = file_name + extension
    min_file = file_name + '.min' + extension

    original_path = path.join(settings.css_directory, original_file)                      # Get full file path.
    min_path = path.join(settings.css_directory, min_file)

    original_size = stat(original_path).st_size                                                # Get file size in Bytes.
    min_size = stat(min_path).st_size

    try:
        percent_reduced = round(                                                    # Calculate percentage size reduced.
            float(100) - float(min_size) / float(original_size) * float(100),
            1                                                                       # Precision
        )
    except ZeroDivisionError:
        percent_reduced = round(0.0, 1)

    original_kb = round(float(original_size) / float(1000), 1)                                # Convert to kiloBytes.
    min_kb = round(float(min_size) / float(1000), 1)

    minification_stats = (
        '\n' + str(original_file) + ':\t ' + str(original_kb) + 'kB\n' +
        str(min_file) + ': ' + str(min_kb) + 'kB\n' +
        'File size reduced by ' + str(percent_reduced) + '%.'
    )
    logging.debug(minification_stats)
    print(minification_stats)


def print_blow_dryer():
    """ Prints an image of a blow dryer using ASCII.

    `A nice png to ascii converter <http://picascii.com>`__

    :return: None

    """
    blow_dryer_ascii = """
                     .-'-.
                  ;@@@@@@@@@'
    ~~~~ ;@@@@@@@@@@@@@@@@@@@+`
    ~~~~ ;@@@@@@@@@@@@@``@@@@@@
                +@@@@@`  `@@@@@'
                   @@@@``@@@@@
                     .-@@@@@@@+
                          @@@@@
                           .@@@.
                            `@@@.
    """
    print(str(blow_dryer_ascii))


def make_directory(directory=''):
    """ Try to make a directory or verify its' existence. Raises an error if neither of these are possible.

    :raise OSError: Raises an OSError if the directory cannot be made or found.

    :type directory: str

    :param directory: A directory path in the file system.

    :return: None

    """
    try:                                            # Python 2.7 Compliant
        makedirs(directory)                         # Make 'log' directory
        logging.debug('%s created.', directory)
    except OSError:
        if not path.isdir(directory):               # Verify directory existence
            raise OSError(directory + ' is not a directory, and could not be created.')


def delete_file_paths(file_paths):
    """ Delete all file_paths. Use Caution.

    Note::

        Ignores files that do not exist.

    :type file_paths: iterable of strings

    :param file_paths: An iterable containing file path strings.
    :return: None

    """
    for file_path in file_paths:
        try:
            remove(file_path)
        except:
            pass
