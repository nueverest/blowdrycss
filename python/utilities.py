# python 2
from __future__ import division
from builtins import round
# builtins
import settings
from re import search, findall
from inspect import currentframe
from os import path
from string import digits

__author__ = 'chad nelson'
__project__ = 'blow dry css'


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

        **Findall ``regex`` Decoded:**

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


def px_to_em(pixels):
    """ Convert a numeric value from px to em using ``settings.base`` as the unit conversion factor.

    **Rules:**

    - ``pixels`` shall only contain [0-9.-].
    - Inputs that contain any other value are simply passed through unchanged.
    - Default ``base`` is 16 meaning ``16px = 1rem``

    **Note:** Does not check the ``property_name`` or ``use_em`` values.  Rather, it blindly converts
    whatever input is provided.  The calling method is expected to know what it is doing.

    Rounds float to a maximum of 4 decimal places.

    :type pixels: str, int, float
    :param pixels: A numeric value with the units stripped.
    :return: (str)

        - If the input is convertible return the converted number as a string with the units ``em``
          appended to the end.
        - If the input is not convertible return the unprocessed input.

    >>> from utilities import px_to_em
    >>> # settings.use_em = True
    >>> px_to_em(pixels='-16.0')
    -1em
    >>> # settings.use_em = False
    >>> px_to_em(pixels='42px')
    42px
    >>> # Invalid input passes through.
    >>> px_to_em(pixels='invalid')
    invalid

    """
    if set(str(pixels)) <= set(digits + '-.'):
        em = float(pixels) / float(settings.base)
        em = round(em, 4)
        em = str(em) + 'em'                             # Add 'em'.
        return em
    return pixels
