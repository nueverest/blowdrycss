# builtins
from unittest import TestCase, main
from os import path, remove
# custom
from settingsbuilder import write_blowdrycss_settings_dot_py


class TestWrite_blowdrycss_settings_dot_py(TestCase):
    """
    IMPORTANT: This particular test can only be run in isolation. The other tests import the settings file from the
    actual module as opposed along with all of the other tests.

    Uncomment ``test directory and file_type settings`` section and run this test.
    """
    def test_write_blowdrycss_settings_dot_py(self):
        settings_file = 'blowdrycss_settings.py'

        # Remove it if it exists.
        if path.isfile(settings_file):
            remove(settings_file)

        # Identical section of code from blowdrycss.py for test purposes.
        write_blowdrycss_settings_dot_py()
        import blowdrycss_settings as settings

        # test file existence
        self.assertTrue(path.isfile('blowdrycss_settings.py'))

        # test directory and file_type settings
        # IMPORTANT: When running this test in isolation uncomment these lines.
        # cwd = getcwd()
        # self.assertTrue(
        #     settings.markdown_directory == path.join(cwd, 'docs', 'markdown'),
        #     msg=settings.markdown_directory + '\t' + path.join(cwd, 'docs', 'markdown')
        # )
        # self.assertTrue(settings.project_directory == cwd)
        # self.assertTrue(settings.css_directory == path.join(cwd, 'css'))
        # self.assertTrue(settings.docs_directory == path.join(cwd, 'docs'))

        self.assertTrue(settings.file_types == ('*.html', ))

        # test accessibility of true settings
        true_settings = [
            settings.timing_enabled, settings.human_readable, settings.minify, settings.media_queries_enabled,
            settings.use_em
        ]
        for true_setting in true_settings:
            self.assertTrue(true_setting)

        # test accessibility of false settings
        false_settings = [settings.markdown_docs, settings.html_docs, settings.rst_docs]
        for false_setting in false_settings:
            self.assertFalse(false_setting)

        # test base, px_to_em, and breakpoints
        self.assertTrue(settings.base == 16)

        self.assertTrue(settings.xxsmall == (settings.px_to_em(0), settings.px_to_em(120)))
        self.assertTrue(settings.xsmall == (settings.px_to_em(121), settings.px_to_em(240)))
        self.assertTrue(settings.small == (settings.px_to_em(241), settings.px_to_em(480)))
        self.assertTrue(settings.medium == (settings.px_to_em(481), settings.px_to_em(720)))
        self.assertTrue(settings.large == (settings.px_to_em(721), settings.px_to_em(1024)))
        self.assertTrue(settings.xlarge == (settings.px_to_em(1025), settings.px_to_em(1366)))
        self.assertTrue(settings.xxlarge == (settings.px_to_em(1367), settings.px_to_em(1920)))
        self.assertTrue(settings.giant == (settings.px_to_em(1921), settings.px_to_em(2560)))
        self.assertTrue(settings.xgiant == (settings.px_to_em(2561), settings.px_to_em(2800)))
        self.assertTrue(settings.xxgiant == (settings.px_to_em(2801), settings.px_to_em(10**6)))


if __name__ == '__main__':
    main()
