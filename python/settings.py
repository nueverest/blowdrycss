from utilities import px_to_em

""" Settings

:type use_em: bool

:param use_em: A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion.
    False disables unit conversions meaning any pixel value remains unchanged.
"""

# TODO: Consider converting these to properties, so that, they cannot be modified anywhere but here.

# Boolean Settings
timing_enabled = True       # Run performance timer
markdown_docs = True        # Generate a markdown files that provide a quick syntax and clashing alias reference.
html_docs = True            # Generate a html file that provide a quick syntax and clashing alias reference.
rst_docs = True             # Generate a sphinx rst file that provide a quick syntax and clashing alias reference.
human_readable = True       # Generate a standard human readable css file
minify = True               # Generate a minified version of the css file

# Plugin Defaults
use_em = True
base = 16
# ...Not Implemented Yet...
# hex_to_rgb = True
# color_parser = False
# extra_dry = False

# breakpoints = False
# scaling = False

# TODO: Implement these in a fashion similar to the performance timer.
# auto_generate = False       # Automatically generates blowdry.css file when a project HTML file is saved.
# http_server = False         # Auto-Start a simple webserver on localhost:8080.
# condense_classes = False    # Edits HTML Files after discovering common patterns (Not DRY).

# Default Screen Breakpoints / Transition Triggers
# Tuple Format (Lower Limit, Upper Limit) in pixels.
# Note: These values change if unit conversion is enabled i.e. ``use_em`` is ``True``.
# Common Screen Resolutions: https://en.wikipedia.org/wiki/List_of_common_resolutions
xxsmall = (px_to_em(0), px_to_em(120))          # 0.0 - 7.5em
xsmall = (px_to_em(121), px_to_em(240))         # 7.5625 - 15.0em
small = (px_to_em(241), px_to_em(480))          # 15.0625 - 30.0em
medium = (px_to_em(481), px_to_em(720))         # 30.0625 - 45.0em: Typical mobile device break point @ 720px.
large = (px_to_em(721), px_to_em(1024))         # 45.0625 - 64.0em
xlarge = (px_to_em(1025), px_to_em(1366))       # 64.0625 - 85.375em
xxlarge = (px_to_em(1367), px_to_em(1920))      # 85.4375 - 120.0em
giant = (px_to_em(1921), px_to_em(2560))        # 120.0625 - 160.0em
xgiant = (px_to_em(2561), px_to_em(2800))       # 160.0625 - 175.0em
xxgiant = (px_to_em(2801), px_to_em(10**6))     # 175.0625 - float("inf")) # Python 2.x representation of Infinity.