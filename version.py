""" Defines the version of the project. Use ``method 3`` described in this reference for single sourcing the version.
    Reference: https://packaging.python.org/en/latest/single_source_version/#single-sourcing-the-version

    Only set the __version__ global variable in this module.

    How to access __version__ externally from settings.py, conf.py, and so on.

    >>> current_version = {}
    >>> with open('version.py') as file:
    >>>     exec(file.read(), current_version)
    >>> current_version['__version__']
    'x.x.x'

    | Uses a modified version of the pre-release version format defined in PEP 440.
    | Reference: https://www.python.org/dev/peps/pep-0440/#pre-releases

    **__version__ format:**

    ``X.Y.Z``

    **__release__ formats:**

    +--------------+-------------------+
    | ``0.0.Za1``  | Alpha release     |
    +--------------+-------------------+
    | ``0.Y.Zb1``  | Beta release      |
    +--------------+-------------------+
    | ``X.Y.Zrc1`` | Release Candidate |
    +--------------+-------------------+
    | ``X.Y.Z``    | Final release     |
    +--------------+-------------------+

    **Incrementing Rules:**

    - When X and Y are both 0 the project is Alpha
    - When only X is 0 the project is Beta

    - The numbers are only incremented never decremented.

    - Z may not be greater than 9
    - Y may not be greater than 9
    - X may grow into infinity.

    - When Z increments beyond 9 Y is incremented by 1. Z is reset to 0.
    - When Y increments beyond 9 X is incremented by 1. Both Y and Z are reset to 0.
    - When X increments both Y and Z are reset to 0.

    **Version Changelog:**

    | **0.0.1** -- Initial Release with basic functions working.
    |
    | **0.0.2** -- Extended functionality to allow for a subset of shorthand properties to be decoded correctly
    |
    | **0.0.3** -- Modularized the color, font, and unit parsers.
    |
    | **0.0.4** -- Sphinx integration started.
    |
    | **0.0.5** -- All docstrings added. Many modules refactored and improved during the documentation process. New
      unit tests added.
    |
    | **0.0.6** -- Advanced media query syntax added. Modules ``breakpointparser`` and ``scalingparser`` added to
      allow for the dynamic creation of media queries. (1/2/2016)
    |
    | **0.0.7** -- ALPHA release: Implemented backward compatibility with Python version 2.7.x.
    |
    | **0.0.8** -- Major refactoring of directory structure, and preparation of new settings file.
    |
    | **0.0.9** -- This version auto-builds blowdrycss_settings.py inside of the users web project making the settings
      easier to find and edit.
    |
    | **0.1.0** -- BETA release: Fixed ImportErrors when running blowdrycss after
      ``pip install blowdrycss`` or ``python setup.py install``. Entered BETA.
    |
    | **0.1.1** -- Corrected more errors in the import infrastructure. Fixed ``blowdrycss_settings.py`` so that
      settings can be customized.
    |
    | **0.1.2** -- ``HTML, JINJA, .NET, and RUBY Template`` file types are now supported. Meaning that classes can be
      discovered in them. To use open ``blowdrycss_settings.py`` and set ``file_types = ('*.html', '.<extension>')``.
      See ``blowdrycss.classparser`` for more details about available extensions.
    |
    | **Supported jinja and django template extensions:** ::

        .jinja, .jinja2, .jnj, .ja, .djt, .djhtml

    | **Supported XHTML, asp.net, and ruby template extensions:** ::

        .aspx, .ascx, .master, .erb

    | **0.1.3** -- Implemented support for auto-generated CSS via Watchdog. Watchdog can now monitor all files
      associated with the ``file_types`` defined in ``blowdrycss_settings.py``. If a file is modified or deleted,
      Watchdog will trigger blowdrycss and auto-generate the CSS files. Watchdog is now a required dependency.
      The setting ``auto-generate`` is currently ``False`` by default.
    |
    | *To enable it* open ``blowdrycss_settings.py``, and set ``auto_generate = True``.
    | *To test it* change one of the project files, and see what happens at the console.
    |
    | ``Timing.py`` was completely re-written and now contains a ``Timer`` class. These changes were needed to
      accommodate watchdog feature.
    |
    | CSS file size reduction statistics are now printed.
    |
    | An ASCII blow dryer is now printed on program exit.

"""
__author__ = 'chad nelson'

__project__ = 'blowdrycss'

__version__ = '0.1.3'

__release__ = __version__ + 'b1'
