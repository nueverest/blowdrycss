from re import search
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# Checks if string contains at least 1 digit.
def contains_a_digit(value=''):
    return True if search(r"[0-9]", value) else False