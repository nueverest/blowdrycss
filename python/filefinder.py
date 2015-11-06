from os import path, walk
from glob import glob


class FileFinder:
    project_directory = ''
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')
    files = []

    def __init__(self, project_directory='', file_types=file_types):
        self.project_directory = project_directory
        self.file_types = file_types
        print('Project Directory:')
        print(project_directory)

        print('\nValid File Types')
        print(self.file_types)

        self.set_files()
        print('\nFile List:')
        self.print_collection(self.files)

    # Takes a list or tuple as input and prints each item.
    @staticmethod
    def print_collection(collection):
        for item in collection:
            print(item)

    # Get all files associated with defined file_types in project directory
    def set_files(self):
        for directory,_,_ in walk(self.project_directory):
            for file_type in self.file_types:
                self.files.extend(glob(path.join(directory, file_type)))
