from os import chdir, getcwd, path
# custom classes
from filehandler import FileFinder, CSSFile, GenericFile
from htmlattributeparser import HTMLClassParser
from classpropertyparser import ClassPropertyParser
from cssbuilder import CSSBuilder
from datalibrary import clashing_alias_markdown, property_alias_markdown, clashing_alias_html, property_alias_html
import timing
__author__ = 'chad nelson'
__project__ = 'blow dry css'


def main():
    # Boolean Settings
    markdown_docs = True        # Generate a markdown files that provide a quick syntax and clashing alias reference.
    html_docs = True            # Generate a html file that provide a quick syntax and clashing alias reference.
    human_readable = True       # Generate a standard human readable css file
    minify = True               # Generate a minified version of the css file


    # Set project_directory to the one containing the files you want to DRY out.
    # In this case it is set to the "examplesite" by default for demonstration purposes.
    chdir('..')                                                 # Navigate up one directory relative to this script.
    project_directory = path.join(getcwd() + '\\examplesite')    # Change to whatever you want.
    css_directory = path.join(project_directory + '\\css')
    
    # Generate Markdown documentation files.
    if markdown_docs:
        markdown_file = GenericFile(file_directory=getcwd(), file_name='clashing_aliases')
        markdown_file.write_file(clashing_alias_markdown, extension='.md')
        markdown_file.file_name = 'property_aliases'                        # Changes file name.
        markdown_file.write_file(property_alias_markdown, extension='.md')

    # Generate HTML documentation files. (This location is important since it allows encoded css to be included.)
    if html_docs:
        html_file = GenericFile(file_directory=project_directory, file_name='clashing_aliases')
        html_file.write_file(clashing_alias_html, extension='.html')
        html_file.file_name = 'property_aliases'                            # Change file name.
        html_file.write_file(property_alias_html, extension='.html')

    # Define File all file types/extensions to search for in project_directory
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

    # Get all files associated with defined file_types in project_directory
    file_finder = FileFinder(project_directory=project_directory, file_types=file_types)

    # Get set of all defined classes
    class_parser = HTMLClassParser(files=file_finder.files)

    # Filter class names only keeping classes that match the defined class encoding.
    class_property_parser = ClassPropertyParser(class_set=class_parser.class_set)
    # print('\nclass_property_parser.class_set:', class_property_parser.class_set)

    # Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    css_builder = CSSBuilder(property_parser=class_property_parser)
    css_text = css_builder.get_css_text()
    # print('CSS Text:')
    # print(css_text)

    # Output the DRY CSS file. (user command option)
    if human_readable:
        css_file = CSSFile(file_directory=css_directory, file_name='blowdry')
        css_file.write_css(css_text=css_text)
        print(css_directory + css_file.file_name + '.css', "created.")

    # Output the Minified DRY CSS file. (user command option)
    if minify:
        css_file = CSSFile(file_directory=css_directory, file_name='blowdry')
        css_file.minify(css_text=css_text)
        print(css_directory + css_file.file_name + '.min.css', "created.")


if __name__ == '__main__':
    main()
