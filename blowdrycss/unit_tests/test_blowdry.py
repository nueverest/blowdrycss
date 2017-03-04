# python 2
from __future__ import absolute_import, unicode_literals
from builtins import bytes
# builtins
from unittest import TestCase, main
import sys
from io import StringIO
import os

# custom
from blowdrycss.utilities import unittest_file_path, delete_file_paths
import blowdrycss.blowdry as blowdry
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestMain(TestCase):
    def test_boilerplate_markdown_docs(self):
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

    def test_boilerplate_rst_docs(self):
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

    def test_parse(self):
        expected_class_set = {
            u'medium-up', u'border-1px-solid-gray', u'padding-5', u'margin-top-10', u'display-none',
            u'width-50', u'height-150px', u'color-hfff', u'font-size-25-s', u't-align-center',
            u'display-inline', u'margin-top-50px', u'talign-center', u'width-150',
            u'display-960-up-i', u'font-size-48', u'bold', u'margin-20', u'bgc-h000', u'c-red-i-hover',
            u'hfff-hover-i', u'padding-10', u'bgc-hf8f8f8', u'text-align-center',
            u'c-blue', u'height-200',
            u'padding-10-s', u'height-50px', u'padding-top-10',
            # Invalid though they exist in the HTML
            # u'addclass3', u'addclass6', u'addclass1', u'addclass4', u'addclass5', u'hide', u'alex-grey-125', u'b',
        }
        substrings = [
            '~~~ blowdrycss started ~~~',
            'CSSBuilder Running...',
            '.css',
        ]

        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            class_set, css_text = blowdry.parse(recent=False, class_set=set(), css_text=b'')
            self.assertTrue(expected_class_set == class_set, msg=class_set)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output + '\tsubstring: ' + substring)
        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory

    def test_parse_on_modify_class_set(self):
        expected_class_set = {
            'green', 'purple-medium-up', 'bgc-h454545',                                     # Pre-existing
            'pink-hover',                                                                   # Modify.html
            # Exists in HTML but should not be returned
            # 'not-valid',
        }
        substrings = [
            '~~~ blowdrycss started ~~~',
            'CSSBuilder Running...',
            '.css',
        ]

        project_directory = settings.project_directory
        css_directory = settings.css_directory

        settings.project_directory = unittest_file_path()
        settings.css_directory = unittest_file_path()

        current_set = {'green', 'purple-medium-up', 'bgc-h454545', }

        css_file = unittest_file_path(filename='blowdry.css')                                       # CSS file
        css_min_file = unittest_file_path(filename='blowdry.min.css')                               # CSS.min file
        with open(css_file, 'w') as generic_file:
            generic_file.write('test test test')

        modify_file = unittest_file_path(filename='modify.html')                                    # Modify file
        with open(modify_file, 'w') as generic_file:
            generic_file.write('<html><div class="pink-hover not-valid">Modified</div></html>')

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            class_set, css_text = blowdry.parse(recent=True, class_set=current_set)
            self.assertTrue(expected_class_set == class_set, msg=class_set)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output + '\tsubstring: ' + substring)
        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory
            settings.css_directory = css_directory
            delete_file_paths((css_file, css_min_file, modify_file, ))

    def test_parse_on_modify_css_text_PREXISTING(self):
        # WARNING Indentation must be preserved.
        expected_css_text = b""".green {
            color: green
            }
        .pink-hover:hover {
    color: pink
    }"""
        substrings = [
            '~~~ blowdrycss started ~~~',
            'CSSBuilder Running...',
            settings.output_file_name,
            settings.output_extension,
        ]

        project_directory = settings.project_directory
        css_directory = settings.css_directory

        settings.project_directory = unittest_file_path()
        settings.css_directory = unittest_file_path()

        current_set = {'green', }

        current_css_text = b""".green {
            color: green
            }
        """

        css_file = unittest_file_path(filename='blowdry.css')                                       # CSS file
        css_min_file = unittest_file_path(filename='blowdry.min.css')                               # CSS.min file
        with open(css_file, 'w') as generic_file:
            generic_file.write('test test test')

        modify_file = unittest_file_path(filename='modify.html')                                    # Modify file
        with open(modify_file, 'w') as generic_file:
            generic_file.write('<html><div class="pink-hover not-valid">Modified</div></html>')

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            class_set, css_text = blowdry.parse(recent=True, class_set=current_set, css_text=current_css_text)
            self.assertTrue(expected_css_text == css_text, msg=css_text)

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue(substring in output, msg=output + '\tsubstring: ' + substring)
        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory
            settings.css_directory = css_directory
            delete_file_paths((css_file, css_min_file, modify_file, ))

if __name__ == '__main__':
    main()

