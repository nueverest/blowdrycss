# python 2.7
from __future__ import absolute_import, unicode_literals, with_statement
from io import open

# builtins
from unittest import TestCase, main
from os import path, getcwd, chdir, remove

# custom
import tox_cleanup

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


def create_file(file_path=''):
    """ Build create a file at the defined file_path, and write the word 'test' inside it.

    :type file_path: str
    :param file_path: Path to the file to be created.

    """
    with open(file_path, 'w', encoding='utf-8') as _file:
        _file.write('test')


class TestToxCleanup(TestCase):
    def test_tox_cleanup_file_exists(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)

        cwd = original_dir
        module_path = path.join(cwd, 'blowdrycss')                      # Prevent removal of source settings file.

        if cwd.endswith('unit_tests') and not path.isdir(module_path):
            up2 = path.join('..', '..')
            chdir(up2)
            cwd = getcwd()

        settings_path = path.join(cwd, 'blowdrycss_settings.py')

        if not path.isfile(settings_path):
            create_file(file_path=settings_path)

        self.assertTrue(path.isfile(settings_path), msg=settings_path)
        tox_cleanup.main()
        self.assertFalse(path.isfile(settings_path), msg=settings_path)

        chdir(original_dir)                                             # Reset directory

    def test_tox_cleanup_file_does_not_exist(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)

        cwd = original_dir

        if cwd.endswith('unit_tests'):
            up2 = path.join('..', '..')
            chdir(up2)
            cwd = getcwd()

        settings_path = path.join(cwd, 'blowdrycss_settings.py')

        if path.isfile(settings_path):
            remove(settings_path)                                       # Delete blowdrycss_settings.py if it exists.

        self.assertFalse(path.isfile(settings_path), msg=settings_path)
        tox_cleanup.main()
        self.assertFalse(path.isfile(settings_path), msg=settings_path)

        chdir(original_dir)                                             # Reset directory


if __name__ == '__main__':
    main()
