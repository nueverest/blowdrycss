# builtins
from unittest import TestCase, main
from os import getcwd, path, remove
# custom
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py


class TestWrite_blowdrycss_settings_dot_py(TestCase):
    def test_write_blowdrycss_settings_dot_py(self):
        settings_file = 'blowdrycss_settings.py'

        # Remove it if it exists.
        if path.isfile(settings_file):
            remove(settings_file)

        # Identical section of code from blowdrycss.py for test purposes.
        write_blowdrycss_settings_dot_py()

        # test file existence
        self.assertTrue(path.isfile('blowdrycss_settings.py'))

        # Import from the current folder.
        import blowdrycss_settings as test_settings    # python setup.py test

        # test directory settings
        cwd = getcwd()
        self.assertEqual(
            test_settings.markdown_directory, path.join(cwd, 'docs', 'markdown'),
            msg=test_settings.markdown_directory + '\t' + path.join(cwd, 'docs', 'markdown')
        )
        self.assertEqual(test_settings.project_directory, cwd)
        self.assertEqual(test_settings.css_directory, path.join(cwd, 'css'))
        self.assertEqual(test_settings.docs_directory, path.join(cwd, 'docs'))

        # test file_type settings
        self.assertTrue(test_settings.file_types == ('*.html', ))

        # test accessibility of true settings
        true_settings = [
            test_settings.timing_enabled, test_settings.human_readable, test_settings.minify, test_settings.media_queries_enabled,
            test_settings.use_em
        ]
        for true_setting in true_settings:
            self.assertTrue(true_setting)

        # test accessibility of false settings
        false_settings = [test_settings.markdown_docs, test_settings.html_docs, test_settings.rst_docs]
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

        # Clean up by deleting test settings file.  Can be commented to see what the generated file looks like.
        # Remove it if it exists.
        if path.isfile(settings_file):
            remove(settings_file)


if __name__ == '__main__':
    main()
