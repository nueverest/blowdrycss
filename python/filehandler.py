from os import path, walk, getcwd
from glob import glob
from cssutils import parseString, ser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class FileFinder(object):
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

    def __init__(self, project_directory=getcwd(), file_types=file_types):
        if path.isdir(project_directory):
            self.project_directory = project_directory
            self.file_types = file_types
            self.files = []
            print('Project Directory:')
            print(project_directory)
            print('\nFile Types')
            print(self.file_types)

            self.set_files()
            print('\nList of Files Found:')
            self.print_collection(self.files)
        else:
            raise NotADirectoryError(project_directory + ' is not a directory.')

    # Takes a list or tuple as input and prints each item.
    @staticmethod
    def print_collection(collection):
        for item in collection:
            print(item)

    # Get all files associated with defined file_types in project directory
    # Reference:
    # stackoverflow.com/questions/954504/how-to-get-files-in-a-directory-including-all-subdirectories#answer-954948
    def set_files(self):
        for directory, _, _ in walk(self.project_directory):
            for file_type in self.file_types:
                self.files.extend(glob(path.join(directory, file_type)))


class FileConverter(object):
    # Converts text files to strings.
    # Ensure the existence of the file_path.
    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self.file_path = file_path
        else:
            raise FileNotFoundError('No file found at: ' + file_path)

    # Convert the file to a string and return it.
    def get_file_as_string(self):
        with open(self.file_path, 'r') as file:
            file_as_string = file.read().replace('\n', '')
        return file_as_string


class CSSFile(object):
    # File name does not include extension.
    def __init__(self, file_directory=getcwd(), file_name='blowdry'):
        if path.isdir(file_directory):
            self.file_directory = file_directory
            self.file_name = file_name
        else:
            raise NotADirectoryError(file_directory + ' is not a directory.')

    def file_path(self, extension=''):
        return path.join(self.file_directory, self.file_name + extension)

    # Output a human readable version of the css file.
    # Note: Overwrites any pre-existing files with the same name.
    def write(self, css_text=''):
        with open(self.file_path(extension='.css'), 'w') as css_file:
            css_file.write(css_text)

    # Output a minified version of the css file.
    # Note: Overwrites any pre-existing files with the same name.
    def minify(self, css_text=''):
        parse_string = parseString(css_text)
        ser.prefs.useMinified()                 # Enables Minification
        with open(self.file_path(extension='.min.css'), 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))
