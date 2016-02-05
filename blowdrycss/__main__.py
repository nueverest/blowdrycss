"""
reference:
http://stackoverflow.com/questions/23164482/created-a-pypi-package-and-it-installs-but-when-run-it-returns-an-import-error#23164865

``python setup.py test`` produces 0 failures and 19 errors.

"""
import sys
import os.path
sys.path.insert(1, os.path.dirname(sys.path[0]))