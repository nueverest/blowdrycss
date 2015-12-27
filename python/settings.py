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
