""" Cleans the project root directory before running tox tests.

Specifically, removes blowdrycss_settings.py from the project root before and after tox testing is finished.
The settings file is auto-generated as part of the integration testing.

If the settings file is in the root folder the py33+ could fail if the settings files changed. It is a strange
corner case that took a while to figure out since the python3 import system is different that py27.

Reproducing the error (scenario 1):
Go to project root where setup.py resides.
Activate virtual environment
Run: tox
If certain tests fail blowdrycss_settings.py could now be in the root directory.
Now subsequent py3x tests will fail.

Reproducing the error (scenario 2):
Go to project root where setup.py resides.
Activate virtual environment
Run: python setup.py install
blowdrycss_settings.py is now in the root directory.
Modify blowdrycss/blowdrycss/blowdrycss_settings.py
Run: tox
py3x tests will fail.

"""

# builtins
from os import path, getcwd, remove


def main():
    cwd = getcwd()
    print('The tox_cleanup started in', cwd)
    module_path = path.join(cwd, 'blowdrycss')            # Prevent removal of source settings file.

    if cwd.endswith('blowdrycss') and path.isdir(module_path):
        settings_file = path.join(cwd, 'blowdrycss_settings.py')

        if path.isfile(settings_file):
            remove(settings_file)
            print('Deleted', settings_file)
        else:
            print('The file', settings_file, 'was not found.')

        print('The tox_clean finished. Project root is clean.')


if __name__ == '__main__':
    main()