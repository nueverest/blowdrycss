from os import chdir, getcwd, path

# Custom classes
from filehandler import FileFinder, CSSFile
from htmlattributeparser import HTMLClassParser
from classpropertyparser import ClassPropertyParser
from cssstylebuilder import CSSStyleBuilder
__author__ = 'chad nelson'
__project__ = 'blow dry css'


def main():
    # Set project_directory to the one containing the files you want to DRY out.
    # In this case it is set to the "ExampleSite" by default for demonstration purposes.
    chdir('..')                                                 # Navigate up one directory relative to this script.
    project_directory = path.join(getcwd() + '\ExampleSite')    # Change to whatever you want.
    css_directory = path.join(project_directory + '\css')

    # Define File all file types/extensions to search for in project_directory
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

    # Get all files associated with defined file_types in project_directory
    file_finder = FileFinder(project_directory=project_directory, file_types=file_types)

    # Get set of all defined classes
    class_parser = HTMLClassParser(files=file_finder.files)

    # Filter class names only keeping classes that match the defined class encoding.
    class_property_parser = ClassPropertyParser(class_set=class_parser.class_set)
    print('class_property_parser.class_set: \n', class_property_parser.class_set)

    # Build a set() of valid css properties. Some classes may be removed during cssutils validation.
    style_builder = CSSStyleBuilder(property_parser=class_property_parser)
    print('CSS Text:')
    print(style_builder.css_style_declaration.cssText)

    # Output the DRY CSS file. (user command option)
    css_file = CSSFile(file_directory=css_directory, file_name='blowdry')
    css_file.write(css_text=style_builder.css_style_declaration.cssText)

    # Output the Minified DRY CSS file. (user command option)
    css_file.minify(css_text=style_builder.css_style_declaration.cssText)

if __name__ == '__main__':
    main()
