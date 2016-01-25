import blowdrycss_settings as settings
from os import getcwd, path


# Change settings directories for testing
def change_settings_for_testing():
    cwd = getcwd()
    settings.markdown_directory = path.join(cwd, 'test_markdown')
    settings.project_directory = path.join(cwd, 'test_examplesite')
    settings.css_directory = path.join(settings.project_directory, 'test_css')
    settings.docs_directory = path.join(cwd, 'test_docs')