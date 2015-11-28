"""
blowdrycss setup module.

See:
https://github.com/nueverest/blowdrycss
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
# from codecs import open
from os import path, pardir


# Optional way to manually generate reStructuredText
# From the project directory run this command.
# pandoc --from markdown --to rst README.md -o python/long_description.rst

# Convert README.md to reStructuredText and assign to long_description.
# Reference: https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules (do not like adding another
# dependency).
try:
    from pypandoc import convert
    here = path.abspath(path.dirname(__file__))
    readme_path = path.join(here, pardir, 'README.md')           # Go up one directory.
    with open(readme_path, encoding='utf-8') as f:
        markdown = f.read()
        long_description = convert(source=markdown, to='rst', format='md')
except (IOError, ImportError):
    # default description
    long_description = u'Rapid styling tool used to quickly auto-generate DRY CSS files from encoded classes found in ' \
                       u'*.html files.'

setup(
    name='blowdrycss',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description=u'Rapid styling tool used to quickly auto-generate DRY CSS files from encoded classes found in ' \
                u'*.html files.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/nueverest/blowdrycss',

    # Author details
    author='chad nelson',
    author_email='nu.everest@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',                  # 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: OS Independent',

        # Topics
        'Topic :: Artistic Software',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',

        # License
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='css compiler pre-compiler pre-processor generator dry cascading style sheets html encoded class parser',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['cssutils>=1.0.1'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install blowdrycss -e .[describe, auto_save, test]
    extras_require={
        'describe': ['pypandoc>=1.1.2'],
        'auto_save': ['watchdog>=0.8.3'],
        'test': ['unittest', 'coverage>=4.0.2'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'blowdrycss': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'blowdry=blowdry:main',
    #     ],
    # },
)