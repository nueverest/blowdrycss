"""
`blowdrycss` is a rapid styling tool that compiles DRY CSS from encoded class selectors in your web project files.

"""

# reference:
# http://stackoverflow.com/questions/23164482/created-a-pypi-package-and-it-installs-but-when-run-it-returns-an-import-error#23164865
# ``python setup.py test`` produces 1 failure and 19 errors.

# builtins
import sys
import os
# custom
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py

# Build blowdrycss_settings.py if it doesn't exist.
if not os.path.isfile('blowdrycss_settings.py'):
    write_blowdrycss_settings_dot_py()

# Allow blowdrycss_settings.py to be found in the users current working directory (cwd).
# The 0 in insert(0, cwd) enables blowdrycss_settings.py to override the blowdrycss module default settings.
cwd = os.getcwd()
sys.path.insert(0, cwd)

