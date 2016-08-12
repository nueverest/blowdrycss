# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
from os import getcwd, path, remove, chdir
from logging import DEBUG

# custom
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py


class TestWriteBlowdrycssSettingsDotPy(TestCase):
    def test_write_blowdrycss_settings_dot_py(self):
        settings_file = 'blowdrycss_settings.py'

        # Identical section of code from blowdrycss.py for test purposes.
        cwd = getcwd()

        # The if/else logic is required for unit testing
        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            if path.isfile(settings_file):                          # Remove it if it exists.
                remove(settings_file)

            write_blowdrycss_settings_dot_py()
            self.assertTrue(path.isfile('blowdrycss_settings.py'))  # test file existence
        else:                                                       # python setup.py test
            chdir(path.join('blowdrycss', 'unit_tests'))

            if path.isfile(settings_file):                          # Remove it if it exists.
                remove(settings_file)

            write_blowdrycss_settings_dot_py()
            self.assertTrue(path.isfile('blowdrycss_settings.py'))  # test file existence
            chdir(cwd)                                              # Reset current working directory.

        # Import from the current folder.
        import blowdrycss.unit_tests.blowdrycss_settings as test_settings    # python setup.py test

        # test directory settings
        cwd = getcwd()
        self.assertEqual(
            test_settings.markdown_directory, path.join(cwd, 'docs', 'markdown'),
            msg=test_settings.markdown_directory + '\t' + path.join(cwd, 'docs', 'markdown')
        )
        self.assertEqual(test_settings.project_directory, path.join(cwd, 'examplesite'))
        self.assertEqual(test_settings.css_directory, path.join(cwd, 'examplesite', 'css'))
        self.assertEqual(test_settings.docs_directory, path.join(cwd, 'docs'))

        # Logging
        self.assertEqual(test_settings.logging_enabled, False)
        self.assertEqual(test_settings.logging_level, DEBUG)
        self.assertEqual(test_settings.log_to_console, False)
        self.assertEqual(test_settings.log_to_file, False)
        self.assertEqual(test_settings.log_directory, path.join(cwd, 'log'))
        self.assertEqual(test_settings.log_file_name, 'blowdrycss.log')
        one_mega_byte = 1048576
        self.assertEqual(test_settings.log_file_size, 4 * one_mega_byte)
        self.assertEqual(test_settings.log_backup_count, 1)

        # test file_type settings
        self.assertTrue(test_settings.file_types == ('*.html', ))

        # test accessibility of true settings
        true_settings = [
            test_settings.html_docs, test_settings.timing_enabled, test_settings.human_readable,
            test_settings.minify, test_settings.media_queries_enabled, test_settings.use_em,
            test_settings.hide_css_errors,
        ]
        for true_setting in true_settings:
            self.assertTrue(true_setting)

        # test accessibility of false settings
        false_settings = [test_settings.markdown_docs, test_settings.rst_docs]
        for false_setting in false_settings:
            self.assertFalse(false_setting)

        # test base, px_to_em, and breakpoints
        self.assertTrue(test_settings.base == 16)

        self.assertTrue(test_settings.xxsmall == (test_settings.px_to_em(0), test_settings.px_to_em(120)))
        self.assertTrue(test_settings.xsmall == (test_settings.px_to_em(121), test_settings.px_to_em(240)))
        self.assertTrue(test_settings.small == (test_settings.px_to_em(241), test_settings.px_to_em(480)))
        self.assertTrue(test_settings.medium == (test_settings.px_to_em(481), test_settings.px_to_em(720)))
        self.assertTrue(test_settings.large == (test_settings.px_to_em(721), test_settings.px_to_em(1024)))
        self.assertTrue(test_settings.xlarge == (test_settings.px_to_em(1025), test_settings.px_to_em(1366)))
        self.assertTrue(test_settings.xxlarge == (test_settings.px_to_em(1367), test_settings.px_to_em(1920)))
        self.assertTrue(test_settings.giant == (test_settings.px_to_em(1921), test_settings.px_to_em(2560)))
        self.assertTrue(test_settings.xgiant == (test_settings.px_to_em(2561), test_settings.px_to_em(2800)))
        self.assertTrue(test_settings.xxgiant == (test_settings.px_to_em(2801), test_settings.px_to_em(10**6)))

        # custom_property_alias_dict
        self.assertEqual(
            test_settings.custom_property_alias_dict,
            {
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
        )

        # Clean up. Removed created file.
        if path.isfile(settings_file):                          # Remove it if it exists.
            remove(settings_file)

        if not cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            chdir(path.join('blowdrycss', 'unit_tests'))
            if path.isfile(settings_file):                          # Remove it if it exists.
                remove(settings_file)
            chdir(cwd)


if __name__ == '__main__':
    main()
