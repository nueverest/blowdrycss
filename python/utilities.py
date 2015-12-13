from re import search
from inspect import currentframe
__author__ = 'chad nelson'
__project__ = 'blow dry css'


def contains_a_digit(string=''):
    """
    Check if string contains a digit `[0-9]`.

    :type string: str

    :param string: The string to test.
    :return: (bool) -- Returns True if string contains at least 1 digit. Otherwise, returns False.

    """
    return True if search(r"[0-9]", string) else False


def deny_empty_or_whitespace(string='', variable_name=''):
    """
    Raises a ValueError if the string or the variable_name is empty or only contains whitespace.

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