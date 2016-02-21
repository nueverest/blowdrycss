# builtins
from unittest import TestCase, main
from os import path, getcwd, chdir
# custom
import tox_cleanup
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


def create_settings(cwd=''):
    """ Build blowdrycss_settings.py if it doesn't exist and the user is not inside the sphinx docs directory.

    """
    if not path.isfile('blowdrycss_settings.py') and not cwd.endswith('docs'):
        write_blowdrycss_settings_dot_py()


class TestTiming(TestCase):
    def test_tox_cleanup_file_exists(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)

        cwd = original_dir
        module_path = path.join(cwd, 'blowdrycss')            # Prevent removal of source settings file.

        if not cwd.endswith('blowdrycss') and not path.isdir(module_path):
            up2 = path.join('..', '..')
            chdir(up2)
            cwd = getcwd()

        self.assertFalse(path.isfile('blowdrycss_settings.py'))
        create_settings(cwd=cwd)
        self.assertTrue(path.isfile('blowdrycss_settings.py'))
        tox_cleanup.main()
        self.assertFalse(path.isfile('blowdrycss_settings.py'))

        chdir(original_dir)     # Reset directory

    def test_tox_cleanup_file_does_not_exist(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)

        cwd = original_dir
        module_path = path.join(cwd, 'blowdrycss')            # Prevent removal of source settings file.

        if not cwd.endswith('blowdrycss') and not path.isdir(module_path):
            up2 = path.join('..', '..')
            chdir(up2)
            cwd = getcwd()

        self.assertFalse(path.isfile('blowdrycss_settings.py'))
        tox_cleanup.main()
        self.assertFalse(path.isfile('blowdrycss_settings.py'))

        chdir(original_dir)     # Reset directory


if __name__ == '__main__':
    main()
