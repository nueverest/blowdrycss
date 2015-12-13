""" Defines the version of the project. Use ``method 3`` described in this reference for single sourcing the version.
    Reference: https://packaging.python.org/en/latest/single_source_version/#single-sourcing-the-version

    Set the value to a __version__ global variable in a dedicated module in your project (e.g. version.py), then have setup.py read and exec the value into a variable.

    How to access the version externally from settings.py, conf.py, and so on.

    >>> version = {}
    >>> with open('version.py') as file:
    >>>     exec(file.read(), version)
    >>> version['__version__']
    'x.x.x'

    Uses a modified version of the pre-release version format defined in PEP 440:
    https://www.python.org/dev/peps/pep-0440/#pre-releases

    __version__ follows the form:

    ``X.Y.Z``

    __release__ follows the form:

    ``0.0.Za``   # Alpha release
    ``0.Y.Zb``   # Beta release
    ``X.Y.Zrc``  # Release Candidate
    ``X.Y.Z``    # Final release

    Incrementing Rules:

    When X and Y are both 0 the project is Alpha
    When only X is 0 the project is Beta

    The numbers are only incremented never decremented.

    Z may not be greater than 9
    Y may not be greater than 9
    X may grow into infinity.

    When Z increments beyond 9 Y is incremented by 1 and Z is reset to 0.
    When Y increments beyond 9 X is incremented by 1 and both Y and Z is reset to 0.
    When X increments both Y and Z is reset to 0.

"""
__author__ = 'chad nelson'

__project__ = 'blow dry css'

__version__ = '0.0.4'

__release__ = __version__ + 'a'
