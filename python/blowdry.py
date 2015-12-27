from os import chdir, getcwd, path
# custom classes
from filehandler import FileFinder, CSSFile, GenericFile
from htmlparser import HTMLClassParser
from classpropertyparser import ClassPropertyParser
from cssbuilder import CSSBuilder
from datalibrary import clashing_alias_markdown, property_alias_markdown, clashing_alias_html, property_alias_html, \
    clashing_alias_rst, property_alias_rst
__author__ = 'chad nelson'
__project__ = 'blow dry css'


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

    **Settings**
    ``project_directory`` -- Allows ``blowdrycss`` to know where the HTML project is located. It will only search the files
    in the directory specified here.

.. |sp| raw:: html

    &nbsp;

    """

    # Boolean Settings
    timing_enabled = True       # Run performance timer
    markdown_docs = True        # Generate a markdown files that provide a quick syntax and clashing alias reference.
    html_docs = True            # Generate a html file that provide a quick syntax and clashing alias reference.
    rst_docs = True             # Generate a sphinx rst file that provide a quick syntax and clashing alias reference.
    human_readable = True       # Generate a standard human readable css file
    minify = True               # Generate a minified version of the css file

    # Plugin Defaults
    use_em = True
    # ...Not Implemented Yet...
    # hex_to_rgb = True
    # color_parser = False
    # extra_dry = False

    # media_queries = False
    # responsive = False

    # TODO: Implement these in a fashion similar to the performance timer.
    # auto_generate = False       # Automatically generates blowdry.css file when a project HTML file is saved.
    # http_server = False         # Auto-Start a simple webserver on localhost:8080.
    # condense_classes = False    # Edits HTML Files after discovering common patterns (Not DRY).

    # Performance timer
    if timing_enabled:
        import timing

    # Set project_directory to the one containing the files you want to DRY out.
    # In this case it is set to the "examplesite" by default for demonstration purposes.
    # Change to whatever you want.
    chdir('..')                                                 # Navigate up one directory relative to this script.
    project_directory = path.join(getcwd() + '\\examplesite')
    css_directory = path.join(project_directory + '\\css')
    
    # Generate Markdown documentation files.
    if markdown_docs:
        markdown_file = GenericFile(file_directory=getcwd(), file_name='clashing_aliases', extension='.md')
        markdown_file.write(clashing_alias_markdown)
        markdown_file.file_name = 'property_aliases'                        # Changes file name.
        markdown_file.write(property_alias_markdown)

    # Generate HTML documentation files. (This location is important since it allows encoded css to be included
    # in the documentation files.)
    if html_docs:
        html_file = GenericFile(file_directory=project_directory, file_name='clashing_aliases', extension='.html')
        html_file.write(clashing_alias_html)
        html_file.file_name = 'property_aliases'                            # Change file name.
        html_file.write(property_alias_html)

    # Generate reStructuredText documentation files.
    if rst_docs:
        docs_directory = path.join(getcwd() + '\\docs')
        print(docs_directory)
        rst_file = GenericFile(file_directory=docs_directory, file_name='clashing_aliases', extension='.rst')
        rst_file.write(clashing_alias_rst)
        rst_file.file_name = 'property_aliases'                        # Changes file name.
        rst_file.write(property_alias_rst)

    # Define File all file types/extensions to search for in project_directory
    file_types = ('*.html', )

    # Get all files associated with defined file_types in project_directory
    file_finder = FileFinder(project_directory=project_directory, file_types=file_types)

    # Create set of all defined classes
    class_parser = HTMLClassParser(files=file_finder.files)

    # Filter class names only keeping classes that match the defined class encoding.
    class_property_parser = ClassPropertyParser(class_set=class_parser.class_set, px_to_em=use_em)
    # print('\nclass_property_parser.class_set:', class_property_parser.class_set)

    # Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    css_builder = CSSBuilder(property_parser=class_property_parser)
    css_text = css_builder.get_css_text()
    # print('CSS Text:')
    # print(css_text)

    # Output the DRY CSS file. (user command option)
    if human_readable:
        css_file = CSSFile(file_directory=css_directory, file_name='blowdry')
        css_file.write(css_text=css_text)
        print(css_directory + css_file.file_name + '.css', "created.")

    # Output the Minified DRY CSS file. (user command option)
    if minify:
        css_file = CSSFile(file_directory=css_directory, file_name='blowdry')
        css_file.minify(css_text=css_text)
        print(css_directory + css_file.file_name + '.min.css', "created.")


if __name__ == '__main__':
    main()
