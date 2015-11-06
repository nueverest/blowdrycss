from os import path, walk
from glob import glob
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class FileFinder:
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

    def __init__(self, project_directory='', file_types=file_types):
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
