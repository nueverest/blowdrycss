"""
**Parameters:**

| markdown_directory (*string*) -- Generally used for development purposes only.

| project_directory (*string) -- Path to your project directory

| css_directory (*string*) -- Path to your projects CSS directory

| docs_directory (*string*) -- Path to Sphinx docs.

| file_types = (*tuple of strings*) -- All file types/extensions to search for in the defined project_directory
  that contain encoded class selectors.

| timing_enabled (*bool*) -- Run performance timer

| markdown_docs (*bool*) -- Generate a markdown files that provides a quick syntax and clashing alias reference.

| html_docs (*bool*) -- Generate a html file that provides a quick syntax and clashing alias reference.

| rst_docs (*bool*) -- Generate a sphinx rst file that provides a quick syntax and clashing alias reference.

| human_readable (*bool*) -- Generate a standard human readable css file.

| minify (*bool*) -- Generate a minified version of the css file.

| media_queries_enabled (*bool*) -- Generate breakpoint and scaling media queries.

| use_em (*bool*) -- A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion.
  False disables unit conversions meaning any pixel value remains unchanged.

| base (*int*) -- Base used for unit conversion (typically set to 16). The pixel value will be divided by
  ``base`` during unit conversion.

| xxsmall (*tuple of floats*) -- (0px, upper limit in pixels)

| xsmall (*tuple of floats*) -- (xxsmall upper limit + 1px, upper limit in pixels)

| small (*tuple of floats*) -- (xsmall upper limit + 1px, upper limit in pixels)

| medium (*tuple of floats*) -- (small upper limit + 1px, upper limit in pixels)

| large (*tuple of floats*) -- (medium upper limit + 1px, upper limit in pixels)

| xlarge (*tuple of floats*) -- (large upper limit + 1px, upper limit in pixels)

| xxlarge (*tuple of floats*) -- (xlarge upper limit + 1px, upper limit in pixels)

| giant (*tuple of floats*) -- (xxlarge upper limit + 1px, upper limit in pixels)

| xgiant (*tuple of floats*) -- (giant upper limit + 1px, upper limit in pixels)

| xxgiant (*tuple of floats*) -- (xgiant upper limit + 1px, 1E+6) [Technically the upper limit is infinity,
  but CSS does not permit it.]

**cssutils Patch:**

``cssutils`` does not currently support CSS 3 Units.  The patch in this file allows length units of
``q``, ``ch``, ``rem``, ``vw``, ``vh``, ``vmin``, and ``vmax``. It also allows angle units of ``turn``.

"""

# python 2
from __future__ import absolute_import, division, unicode_literals
from builtins import round

# builtins
from os import getcwd, path
from string import digits
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# plugins
from cssutils import profile

__project__ = 'blowdrycss'


# Set project_directory to the one containing the files you want to DRY out.
# Change it to whatever you want.
cwd = getcwd()

if cwd.endswith('unit_tests'):                                              # Allows running of pycharm unittest.
    markdown_directory = path.join(cwd, 'test_markdown')
    project_directory = path.join(cwd, 'test_examplesite')
    css_directory = path.join(project_directory, 'test_css')
    docs_directory = path.join(cwd, 'test_docs')
else:                                                       # Run unittest cmd from the root directory.
    markdown_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_markdown')
    project_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite')
    css_directory = path.join(project_directory, 'test_css')
    docs_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_docs')

# Logging
logging_enabled = False
logging_level = DEBUG                                       # Allowed: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_to_console = True
log_to_file = True
log_directory = path.join(cwd, 'log')
log_file_name = 'blowdrycss.log'
one_mega_byte = 1048576
log_file_size = 4 * one_mega_byte                           # Max log file size
log_backup_count = 1                                        # Maximum number of log files.

# All file types/extensions to search for in the defined project_directory that contain encoded class selectors.
# Example format: ('*.html', )
file_types = ('*.html', )

# Boolean Flags
timing_enabled = True           # Run performance timer
markdown_docs = True            # Generate a markdown files that provides a quick syntax and clashing alias reference.
html_docs = True                # Generate a html file that provides a quick syntax and clashing alias reference.
rst_docs = True                 # Generate a sphinx rst file that provides a quick syntax and clashing alias reference.
human_readable = True           # Generate a standard human readable css file.
minify = True                   # Generate a minified version of the css file.
media_queries_enabled = True    # Generate breakpoint and scaling media queries.
# ...Not Implemented Yet...
# use_rgb = True
# extra_dry = False             # Combine identical CSS discovered under different class selector names.

# TODO: Implement these in a fashion similar to the performance timer.
# auto_generate = False         # Automatically generates blowdry.css file when a project HTML file is saved.
# http_server = False           # Auto-Start a simple webserver on localhost:8080.
# public_url = False            # Uses ngrok to generate a temporary public url for testings and demo purposes.
# condense_classes = False      # Edits HTML Files after discovering common patterns (Not DRY do not implement).

# Unit Conversion Defaults
use_em = True
base = 16


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

    >>> from settings.blowdrycss_settings import px_to_em
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
        em = float(pixels) / float(base)
        em = round(em, 4)
        em = str(em) + 'em'                             # Add 'em'.
        return em
    return pixels


# Default Screen Breakpoints / Transition Triggers
# Tuple Format (Lower Limit, Upper Limit) in pixels.
# Note: These values change if unit conversion is enabled i.e. ``use_em`` is ``True``.
# Common Screen Resolutions: https://en.wikipedia.org/wiki/List_of_common_resolutions
xxsmall = (px_to_em(0), px_to_em(120))          # 0.0 - 7.5em
xsmall = (px_to_em(121), px_to_em(240))         # 7.5625 - 15.0em
small = (px_to_em(241), px_to_em(480))          # 15.0625 - 30.0em
medium = (px_to_em(481), px_to_em(720))         # 30.0625 - 45.0em  # Typical mobile device break point @ 720px.
large = (px_to_em(721), px_to_em(1024))         # 45.0625 - 64.0em
xlarge = (px_to_em(1025), px_to_em(1366))       # 64.0625 - 85.375em
xxlarge = (px_to_em(1367), px_to_em(1920))      # 85.4375 - 120.0em
giant = (px_to_em(1921), px_to_em(2560))        # 120.0625 - 160.0em
xgiant = (px_to_em(2561), px_to_em(2800))       # 160.0625 - 175.0em
xxgiant = (px_to_em(2801), px_to_em(10**6))     # 175.0625 - float("inf")) # Python 2.x representation of Infinity.

# Custom CSS Property Syntax
# When adding a new alias it must end with a '-'.
# To add a new alias 'bgc-' for 'background-color' add the (key: value) pair 'background-color': {'bgc-'},
# to custom_property_alias_dict.
#
#  key = A valid CSS property name (consult the W3C standard and datalibrary.DataLibrary.property_names).
# value = An alias set().
#
# If 'bgc' is used without the '-', then blowdrycss assumes that 'bgc' is a valid CSS property (which it is not).
# This will result in 'bgc' being discarded later on as an invalid css class selector.
#
# Defining 'bgc-' allows the following encoded class selector syntax:
# 'bgc-blue', 'bgc-h000', ..., 'bgc-red'
#
# These encoded class selectors can be used inside of Web project files matching 'file_type' defined above.
custom_property_alias_dict = {
    'background': {'bg-', },
    'background-color': {'bgc-', 'bg-c-', 'bg-color-', },
    'color': {'c-', },
    'font-size': {'fsize-', 'f-size-', },
    'font-weight': {'fweight-', 'f-weight-', },
    'height': {'h-', },
    'margin': {'m-', },
    'margin-top': {'m-top-', },
    'margin-bottom': {'m-bot-', },
    'padding': {'p-', 'pad-', },
    'padding-top': {'p-top-', },
    'position': {'pos-', },
    'text-align': {'talign-', 't-align-', },
    'vertical-align': {'valign-', 'v-align-', },
    'width': {'w-', },
}

# Patches cssutils
profile._MACROS['length'] = r'0|{num}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['positivelength'] = r'0|{positivenum}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['angle'] = r'0|{num}(deg|grad|rad|turn)'
profile._resetProperties()