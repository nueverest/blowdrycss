# python 2
from __future__ import print_function
from builtins import bytes, str
# builtins
import logging
import cssutils
# custom
from blowdrycss.filehandler import FileFinder, CSSFile, GenericFile
from blowdrycss.htmlparser import HTMLClassParser
from blowdrycss.classpropertyparser import ClassPropertyParser
from blowdrycss.cssbuilder import CSSBuilder
from blowdrycss.datalibrary import clashing_alias_markdown, property_alias_markdown, clashing_alias_html, \
    property_alias_html, clashing_alias_rst, property_alias_rst
from blowdrycss.mediaquerybuilder import MediaQueryBuilder
import blowdrycss.blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


def main():
    """ This is the main script.

    **Order of Operations:**

    - Initialize settings.
    - Start performance timer.
    - Generate Markdown documentation files.
    - Generate HTML documentation files. (This location is important since it allows encoded css to be included
      in the documentation files.)
    - Generate reStructuredText documentation files.
    - Define File all file types/extensions to search for in project_directory
    - Get all files associated with defined file_types in project_directory
    - Get set of all defined classes
    - Filter class names only keeping classes that match the defined class encoding.
    - Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    - Output the DRY CSS file. (user command option)
    - Output the Minified DRY CSS file. (user command option)

    **Depending on the settings this script generates the following:**

    - DRY CSS files
        - blowdry.css |sp| |sp| |sp| |sp| |sp| **human readable**
        - blowdry.min.css |sp| **minified**

    - Clashing Alias files (Encoded class selector aliases that are invalid and cannot be used because they clash.)
        - Markdown |sp| |sp| |sp| |sp| |sp| |sp| **Github**
        - HTML |sp| |sp| |sp| |sp| |sp| |sp| |sp| |sp| |sp| **Browser**
        - reStructuredText |sp| **Sphinx**

    - Property Alias File (Encoded class selector aliases that are valid and can be used to construct class selectors.)
        - Markdown |sp| |sp| |sp| |sp| |sp| |sp| **Github**
        - HTML |sp| |sp| |sp| |sp| |sp| |sp| |sp| |sp| |sp| **Browser**
        - reStructuredText |sp| **Sphinx**

    - Temporal Statistics

    **Note:** The default locations of these files can be overridden to suit your needs.

    **Directory assignments**
    ``project_directory`` -- Allows ``blowdrycss`` to know where the HTML project is located. It will only search the files
    in the directory specified here.

.. |sp| raw:: html

    &nbsp;

    """

    # Import settings. Better to ask forgiveness both importing and writing the file.
    # The long name blowdrycss_settings is used since the django uses settings.py and using the same name would
    # cause a name conflict.

    # TODO: Overwrite settings

    if settings.hide_css_errors:
        cssutils.log.setLevel(logging.CRITICAL)

    # Performance timer
    if settings.timing_enabled:
        pass

    # Generate Markdown documentation files.
    if settings.markdown_docs:
        markdown_file = GenericFile(                                        # Document forbidden clashing aliases.
                file_directory=settings.markdown_directory,
                file_name='clashing_aliases',
                extension='.md'
        )
        markdown_file.write(str(clashing_alias_markdown))
        markdown_file = GenericFile(                                        # Document allowed property aliases.
                file_directory=settings.markdown_directory,
                file_name='property_aliases',
                extension='.md'
        )
        markdown_file.write(str(property_alias_markdown))

    # Generate HTML documentation files. (This location is important since it allows encoded css to be included
    # in the documentation files.)
    if settings.html_docs:
        html_file = GenericFile(                                            # Document forbidden clashing aliases.
                file_directory=settings.project_directory,
                file_name='clashing_aliases',
                extension='.html'
        )
        html_file.write(str(clashing_alias_html))
        html_file = GenericFile(                                            # Document allowed property aliases.
                file_directory=settings.project_directory,
                file_name='property_aliases',
                extension='.html'
        )
        html_file.write(str(property_alias_html))

    # Generate reStructuredText documentation files.
    if settings.rst_docs:
        print(str(settings.docs_directory))                                              # Python 2 requires str().
        rst_file = GenericFile(file_directory=settings.docs_directory, file_name='clashing_aliases', extension='.rst')
        rst_file.write(str(clashing_alias_rst))
        rst_file = GenericFile(file_directory=settings.docs_directory, file_name='property_aliases', extension='.rst')
        rst_file.write(str(property_alias_rst))

    # Get all files associated with defined file_types in project_directory
    file_finder = FileFinder(project_directory=settings.project_directory, file_types=settings.file_types)

    # Create set of all defined classes
    class_parser = HTMLClassParser(files=file_finder.files)

    # Filter class names. Only keep classes matching the defined class encoding.
    class_property_parser = ClassPropertyParser(class_set=class_parser.class_set)
    # print('\nclass_property_parser.class_set:', class_property_parser.class_set)
    class_set = class_property_parser.class_set.copy()

    # Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    css_builder = CSSBuilder(property_parser=class_property_parser)
    css_text = css_builder.get_css_text()

    # Build Media Queries
    if settings.media_queries_enabled:
        unassigned_class_set = class_set.difference(css_builder.property_parser.class_set)
        css_builder.property_parser.class_set = unassigned_class_set                # Only use unassigned classes
        css_builder.property_parser.removed_class_set = set()                       # Clear set
        media_query_builder = MediaQueryBuilder(property_parser=class_property_parser)
        # print(media_query_builder.property_parser.class_set)
        css_text += bytes(media_query_builder.get_css_text(), 'utf-8')

    # print('CSS Text:')
    # print(css_text)

    # Output the DRY CSS file. (user command option)
    if settings.human_readable:
        css_file = CSSFile(file_directory=settings.css_directory, file_name='blowdry')
        css_file.write(css_text=css_text)
        print(str(settings.css_directory + css_file.file_name) + '.css created.')

    # Output the Minified DRY CSS file. (user command option)
    if settings.minify:
        css_file = CSSFile(file_directory=settings.css_directory, file_name='blowdry')
        css_file.minify(css_text=css_text)
        print(str(settings.css_directory + css_file.file_name) + '.min.css created.')


if __name__ == '__main__':
    main()
