# python 2
from __future__ import absolute_import, print_function, unicode_literals
from builtins import bytes, str
# builtins
import logging
import cssutils
from os import path
# custom
from blowdrycss import log
from blowdrycss.filehandler import FileFinder, CSSFile, GenericFile
from blowdrycss.classparser import ClassParser
from blowdrycss.classpropertyparser import ClassPropertyParser
from blowdrycss.cssbuilder import CSSBuilder
from blowdrycss.datalibrary import clashing_alias_markdown, property_alias_markdown, clashing_alias_html, \
    property_alias_html, clashing_alias_rst, property_alias_rst
from blowdrycss.mediaquerybuilder import MediaQueryBuilder
from blowdrycss.utilities import print_minification_stats, validate_output_file_name_setting, validate_output_extension_setting
import blowdrycss_settings as settings

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


def boilerplate():
    """ Watchdog wrapper only calls this once to eliminate recurring performance impact.

    - Validate the output_file_name and output_extenion settings.
    - Generate Markdown documentation files.
    - Generate HTML documentation files. (This location is important since it allows encoded css to be included
      in the documentation files.)
    - Generate reStructuredText documentation files.

    :return: None

    """
    validate_output_file_name_setting()
    validate_output_extension_setting()

    if settings.logging_enabled:
        log.enable()

    if settings.hide_css_errors:
        cssutils.log.setLevel(logging.CRITICAL)

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
        print('\nDocumentation Directory:', str(settings.docs_directory))     # str() is required for Python2
        rst_file = GenericFile(file_directory=settings.docs_directory, file_name='clashing_aliases', extension='.rst')
        rst_file.write(str(clashing_alias_rst))
        rst_file = GenericFile(file_directory=settings.docs_directory, file_name='property_aliases', extension='.rst')
        rst_file.write(str(property_alias_rst))


def parse(recent=True, class_set=set(), css_text=b''):
    """ It parses every eligible file in the project i.e. file type matches an element of settings.file_types.
    This ensures that from time to time unused CSS class selectors are removed from blowdry.css.

    **Order of Operations:**

    - Initialize settings.
    - Start performance timer.
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
    ``project_directory`` -- Allows ``blowdrycss`` to know where the HTML project is located. It will only search
    the files in the directory specified here.

.. |sp| raw:: html

    &nbsp;

    :param css_text:
    :type recent: bool
    :param recent: Flag that indicates whether to parse the most recently modified files (True Case)
      or all eligible files (False Case).

    :type class_set: set
    :param class_set: The set of known css class selectors.

    :type css_text: bytes
    :param css_text: The current version of the CSS text.

    """
    if settings.timing_enabled:
        from blowdrycss.timing import Timer
        timer = Timer()

    print('\n~~~ blowdrycss started ~~~')

    # Get files to parse.
    file_finder = FileFinder(recent=recent)

    # Create set of all defined classes
    class_parser = ClassParser(file_dict=file_finder.file_dict)

    # Unite class sets during on_modified case.
    if recent:
        modified_class_set = class_parser.class_set
        use_this_set = modified_class_set.difference(class_set)
    else:
        use_this_set = class_parser.class_set

    # Filter class names. Only keep classes matching the defined class encoding.
    class_property_parser = ClassPropertyParser(class_set=use_this_set)
    logging.info(msg='blowdry.class_property_parser.class_set:\t' + str(class_property_parser.class_set))
    use_this_set = class_property_parser.class_set.copy()

    # Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    css_builder = CSSBuilder(property_parser=class_property_parser)
    css_text += bytes(css_builder.get_css_text())
    builder_class_set = css_builder.property_parser.class_set.copy()

    # Build Media Queries
    if settings.media_queries_enabled:
        unassigned_class_set = use_this_set.difference(css_builder.property_parser.class_set)
        css_builder.property_parser.class_set = unassigned_class_set.copy()             # Only use unassigned classes
        css_builder.property_parser.removed_class_set = set()                           # Clear set
        media_query_builder = MediaQueryBuilder(property_parser=class_property_parser)
        logging.debug(
            msg=(
                'blowdry.media_query_builder.property_parser.class_set:\t' +
                str(media_query_builder.property_parser.class_set)
            )
        )
        css_text += bytes(media_query_builder.get_css_text(), 'utf-8')

        media_class_set = unassigned_class_set.intersection(media_query_builder.property_parser.class_set)

        if recent:
            class_set = class_set.union(builder_class_set)
            class_set = class_set.union(media_class_set)
        else:
            class_set = builder_class_set.copy()
            class_set = class_set.union(media_class_set)
    else:
        if recent:
            class_set = class_set.union(builder_class_set)
        else:
            class_set = builder_class_set.copy()

    logging.debug('\nCSS Text:\n\n' + str(css_text))
    print('\nAuto-Generated CSS:')

    # Output the DRY CSS file. (user setting option)
    if settings.human_readable:
        css_file = CSSFile()
        css_file.write(css_text=css_text)
        print(path.join(css_file.file_directory, css_file.file_name) + css_file.extension)

    # Output the Minified DRY CSS file. (user setting option)
    if settings.minify:
        css_file = CSSFile()
        css_file.minify(css_text=css_text)
        print(path.join(css_file.file_directory, css_file.file_name) + '.min' + css_file.extension)

    if settings.timing_enabled:
        timer.report()

    if settings.minify:
        print_minification_stats(file_name=settings.output_file_name, extension=settings.output_extension)

    return class_set, css_text
