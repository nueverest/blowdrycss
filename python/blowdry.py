from os import chdir, getcwd, path

# Custom classes
from filehandler import FileFinder
from htmlattributeparser import HTMLClassParser
from classpropertyparser import ClassPropertyParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


# Set project_directory to the one containing the files you want to DRY out.
# In this case it is set to the "ExampleSite" by default for demonstration purposes.
chdir('..')                                                 # Navigate up one directory relative to this script.
project_directory = path.join(getcwd() + '\ExampleSite')    # Change to whatever you want.

# Define File all file types/extensions to search for in project_directory
file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

# Get all files associated with defined file_types in project_directory
file_finder = FileFinder(project_directory=project_directory, file_types=file_types)

# Get set of all defined classes
class_parser = HTMLClassParser(files=file_finder.files)

# Determine which class names match the format
class_property_parser = ClassPropertyParser(class_set=class_parser.class_set)
print('class_property_parser.class_set =', class_property_parser.class_set)

# Generate a DRY CSS file.


# Output the DRY CSS file. (user command option)


# Minify the DRY CSS file.


# Output the Minified DRY CSS file. (user command option)
