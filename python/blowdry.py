from os import chdir, getcwd, path

# Custom classes
from filehandler import FileFinder, FileConverter
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

for file in file_finder.files:
    file_converter = FileConverter(file_path=file)
    print(file_converter.get_file_as_string())

# Detect all defined classes


# Determine which class names match the format


# Generate a DRY CSS file.


# Output the DRY CSS file. (user command option)


# Minify the DRY CSS file.


# Output the Minified DRY CSS file. (user command option)
