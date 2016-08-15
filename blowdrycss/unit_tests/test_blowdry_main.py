# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main
import sys
from io import StringIO
import os

# custom
from blowdrycss.utilities import unittest_file_path
import blowdrycss.blowdry as blowdry
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestMain(TestCase):
    def test_main(self):
        substrings = [
            '~~~ blowdrycss started ~~~',
            'CSSBuilder Running...',
            '.css',
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            blowdry.parse(recent=False)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output + '\tsubstring: ' + substring)
        finally:
            sys.stdout = saved_stdout

    def test_main_markdown_docs(self):
        # Save original values.
        project_directory = settings.project_directory
        markdown_directory = settings.markdown_directory
        markdown_docs = settings.markdown_docs

        # Change settings
        settings.project_directory = unittest_file_path(folder='test_examplesite')  # Prevent 'examplesite' creation.
        settings.markdown_directory = unittest_file_path(folder='test_markdown')
        settings.markdown_docs = True

        expected_files = (
            os.path.join(settings.markdown_directory, 'clashing_aliases.md'),
            os.path.join(settings.markdown_directory, 'property_aliases.md'),
        )

        for expected_file in expected_files:                                        # Ensure the files do not exist.
            if os.path.isfile(expected_file):
                os.remove(expected_file)

        blowdry.boilerplate()                                                       # Run It

        for expected_file in expected_files:
            self.assertTrue(os.path.isfile(expected_file), msg=expected_file)
            os.remove(expected_file)                                                # Delete

        # Reset settings values.
        settings.project_directory = project_directory
        settings.markdown_directory = markdown_directory
        settings.markdown_docs = markdown_docs

    def test_rst_docs(self):
        # Save original values.
        project_directory = settings.project_directory
        docs_directory = settings.docs_directory
        rst_docs = settings.rst_docs

        # Change settings
        settings.project_directory = unittest_file_path(folder='test_examplesite')  # Prevent 'examplesite' creation.
        settings.docs_directory = unittest_file_path(folder='test_docs')
        settings.rst_docs = True

        expected_files = (
            os.path.join(settings.docs_directory, 'clashing_aliases.rst'),
            os.path.join(settings.docs_directory, 'property_aliases.rst'),
        )

        for expected_file in expected_files:                                        # Ensure the files do not exist.
            if os.path.isfile(expected_file):
                os.remove(expected_file)

        blowdry.boilerplate()

        for expected_file in expected_files:
            self.assertTrue(os.path.isfile(expected_file), msg=expected_file)
            os.remove(expected_file)                                                # Delete

        # Reset settings values.
        settings.project_directory = project_directory
        settings.docs_directory = docs_directory
        settings.rst_docs = rst_docs


if __name__ == '__main__':
    main()

