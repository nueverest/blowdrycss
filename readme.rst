Read Me
=======

.. image:: https://img.shields.io/pypi/v/blowdrycss.svg?maxAge=2592000?style=plastic   :target: https://pypi.python.org/pypi/blowdrycss

.. image:: https://img.shields.io/travis/nueverest/blowdrycss.svg?maxAge=2592000   :target: https://travis-ci.org/nueverest/blowdrycss

.. image:: https://img.shields.io/coveralls/nueverest/blowdrycss.svg?maxAge=2592000   :target: https://coveralls.io/github/nueverest/blowdrycss

|

`blowdrycss` is a rapid styling tool that compiles DRY CSS from encoded class selectors in your web project files.


Getting Started
~~~~~~~~~~~~~~~

`Quick Start Docs <http://blowdrycss.readthedocs.io/en/latest/quickstart.html>`__

`Official site blowdrycss.org <http://blowdrycss.org>`__

`Full documentation <http://blowdrycss.readthedocs.io/en/latest/index.html>`__


Version Changelog
~~~~~~~~~~~~~~~~~

| See ``version.py`` for full changelog.
|
| **0.2.6** -- Created a filehandler.FileModificationComparator which runs under watchdog mode. This
  feature dramatically improves efficiency by only adding classes based on the files that changed
  before the last run of blowdrycss. The current CSS class selectors are now stored within the
  scope of the watchdog wrapper.

  A LimitTimer expires periodically (default is 30 minutes). The expiration triggers a parses
  of all files to delete unused classes.

  For those upgrading the package be sure to add ``time_limit = 1800`` to your current ``blowdrycss_settings.py``.

  Class selectors that were deleted by the user during file
  modification are temporarily ignored since all eligible files (including the ones
  not modified) would need to be parsed before deletion should be authorized. Deletion and full,
  comprehensive scans of all files now occurs every 1800 seconds (30 minutes). This value can be
  increased or decreased in the settings file by changing ``time_limit``.

  Added basic high-level design files.

  Force pypandoc==1.1.3 since pandoc doesn't properly install on Windows in version 1.2.

  Commented out pip and setuptools from requirements.txt.

  PEP8 and typo corrections.

| **0.2.7** -- Added a call to LimitTimer.reset() to fix a bug in which the LimitTimer never expired.
  Add two more color regexes which allow the case in which hex is be combined with a pseudo class.
  e.g. ``hffffff-hover`` or ``hfff-before``.


Why the name blowdrycss?
~~~~~~~~~~~~~~~~~~~~~~~~

Inspiration for the name came from the blow dryer. A blow dryer rapidly drys and styles hair.

Similarly, ``blowdrycss`` is used to rapidly style HTML and generate DRY CSS files using encoded class names.


Example Usage in HTML Tags:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use the CSS level 1, 2.1, and 3 syntax that you already know.**

.. code:: html

    <div class="text-align-center margin-top-30">
        <p class="font-size-25">
            The font-size is 25px. <span class="green">Green Text</span>
        </p>
    </div>

``blowdrycss`` decodes the class names ``text-align-center``,
``margin-top-30``, ``font-size-25``, and ``green``; and generates the
following atomic CSS in ``blowdry.css``:

::

    .text-align-center { text-align: center }
    .margin-top-30 { margin-top: 30px }
    .font-size-25 { font-size: 25px }
    .green { color: green }

Advantages of blowdrycss
~~~~~~~~~~~~~~~~~~~~~~~~

#. **Rapid Development:** Less time spent writing CSS, and cleaning up unused style rules.
#. **DRY (Don't Repeat Yourself):** Reduces CSS file size by only defining properties once.
#. **Symbiotic:**
    * Can be integrated with the current ecosystem of CSS compilers and frameworks.
      Compatible with SASS, SCSS, PostCSS, LESS, Foundation, Bootstrap.
    * Supports class selector discovery within HTML, JINJA, XHTML, .NET, Ruby ERB Templates, Javascript, and C#.
#. **Documented:** Hands-on `tutorial <http://blowdrycss.readthedocs.io/en/latest/quickstart.html>`__ and sphinx `documentation <http://blowdrycss.readthedocs.io/en/latest/index.html>`__ to get you up and running fast.
#. **Robust:** Built for the real world in which deadlines and division of labor is not always taken into account. Can be used across all phases of a products lifecycle from prototype to production.
#. **Customizable:** Features can be turned on and off inside of `blowdrycss_settings.py <https://github.com/nueverest/blowdrycss/blob/master/blowdrycss/blowdrycss_settings.py>`__. Examples include:
    * Watchdog file monitoring
    * Logging
    * Unit parsing
    * Color parsing
    * Font parsing
    * CSS Minification
    * Media query parsing.
#. **Atomic:** Generates atomic CSS declarations.
#. **Standardized:** HTML5 compatible. All `W3C CSS <http://www.w3.org/Style/CSS/Overview.en.html>`__ Level 2.1, and Level 3 properties implemented. PEP8 Compliant.
#. **Tested:** UnitTest Coverage
#. **Permissive:** `MIT license <https://github.com/nueverest/blowdrycss/blob/master/LICENSE>`__

Requirements
~~~~~~~~~~~~

- `Python 2.7.x or 3.3+ <https://www.python.org/downloads/>`__ (required)
- `cssutils 1.0.1+ <https://bitbucket.org/cthedot/cssutils>`__ (required)
- `future 0.15.2+ <https://pypi.python.org/pypi/future>`__ (required - for Python 2.7)
- `pandoc <https://pypi.python.org/pypi/pypandoc/1.1.3#installing-pandoc>`__ (required - file type conversion)
- `pypandoc 1.1.2+ <pypi.python.org/pypi/pypandoc/1.1.3>`__ (required - file type conversion)
- `watchdog 0.8.2+ <https://pypi.python.org/pypi/watchdog/0.8.3>`__ (required - monitor directory and auto-generate CSS)

Optional
''''''''

- tox 2.3.1+ (Multi-environment testing)
- `tox-travis 0.4+ <https://pypi.python.org/pypi/tox-travis>`__ (Allows tox to be used on Travis CI.)
- coverage 4.0.2+ (Check test coverage)
- `coveralls 1.1+ <https://github.com/coagulant/coveralls-python>`__ (Used to report coverage when tox is run via Travis CI.)
- sphinx 1.3.3+ (docs)

Pre-Requisite Knowledge
~~~~~~~~~~~~~~~~~~~~~~~

-  Basic HTML and CSS
-  Zero programming experience required.

Motivation
~~~~~~~~~~

This tool was created after seeing how many companies manage their CSS files. The following are some scenarios:

Scenario 1 - WET (Write Everything Twice) CSS
'''''''''''''''''''''''''''''''''''''''''''''

Inside a CSS file you find the following:

.. code:: css

    .header-1 { font-weight: bold; font-size: 12px; font-color: red; }
    .header-2 { font-weight: bold; font-size: 16px; font-color: blue; }
    .header-3 { font-weight: bold; font-size: 12px; font-color: green; }

The property ``font-weight: bold;`` appears three times, and
``font-size: 12px;`` appears twice. This is not DRY (Don't Repeat
Yourself).

Scenario 2 - Stale or Unused CSS
''''''''''''''''''''''''''''''''

Inside a CSS file you find the following:

.. code:: css

    .banner-video {
        position: absolute;
        top: 48%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        /*width: auto;*/
        /*max-height: 30.5em;*/
        z-index: -100;
        transform: translateX(-50%) translateY(-50%);
        background-color: rgba(0,0,0,1);
        background-size: contain;
        transition: 1s opacity;
    }

Six months later the person who wrote this CSS is then asked to remove
banner-video from the homepage. More often than not the
front-end developer will remove the CSS class from the HTML file, but
not from the CSS file. This leaves unused CSS lurking in the project.

Reasons include:
^^^^^^^^^^^^^^^^

-  Forgetting to delete the rule from the CSS file.
-  Fear that the class is used somewhere else and that it might break
   the site.
-  Being too busy to search all of the files in their project for other
   potential use cases.

Now 326 bytes worth of stale CSS data lurks in the style files.

Scenario 3 - Modern CSS Pre-compiler:
'''''''''''''''''''''''''''''''''''''

CSS compilation with SASS/SCSS, PostCSS, or LESS is awesome, and makes
writing lots of CSS rules easy. Tools like these allow auto-generation
of hundreds of header rules like the ones above. If care is not taken
this leverage can rapidly grow the CSS file.

SCSS Mixin example from a recent project:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: css

    @mixin text($font-color, $font-size, $font-family:"Open Sans", $line-height:inherit) {
        color: $font-color;
        font-size: $font-size;
        font-family: $font-family, $default-font-family;
        line-height: $line-height;
    }

This mixin is called using ``@include`` as follows:

.. code:: css

    @include text($color-blue, rem-calc(14px), $default-font-family);

It turns out that ``@include text(...)`` is called 627 times in our
SCSS. Most of these ``@include`` statements include at least one
matching input parameter resulting in thousands of duplicate CSS
properties.

Auto-generating ``font-size: 1rem;`` 500 times is now super easy with a
pre-compiler and a for-loop. Some might say, ::

    Well we minified it to save space.

Yes but, ::

    Why did you write the same property 500 times in your main CSS file?

CSS File size does matter. For consideration:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Longer download times increase user bounce rates especially on mobile
   devices.
-  Data pollution on the Internet.
-  Increased likelihood of style bugs.
-  Increased time required to implement new changes and
   deprecate features.

What it is not
~~~~~~~~~~~~~~

This tool is not designed to replace the need to hand-craft complex CSS property or rule declarations.

* Custom CSS would need to be written for Multi-rule classes, Background images, url() values, multi-word fonts, and some shorthand properties.

The following is an example of something this tool in not intended to
generate, and something that still needs to be written by hand.

.. code:: css

    .home-banner {
        background: url("https://somewhere.net/images/banner/home-mainbanner-bg.jpg") no-repeat;
        font-family: "Open Sans","Source Sans Pro",Arial;
        background-repeat: no-repeat;
        background-size: cover;
        min-height: 7rem;
        font-weight: bold;
        font-size: 3.5625rem;
        color: white;
        line-height: 3.6875rem;
        text-align: center;
        text-shadow: -2px 2px 4px rgba(0,0,0,0.5);
    }

Valuable References
~~~~~~~~~~~~~~~~~~~

    `Blowdrycss Documentation <http://blowdrycss.readthedocs.io/en/latest/index.html>`__

    `Github Repo <https://github.com/nueverest/blowdrycss>`__

    `Slides presented at DessertPy <https://docs.google.com/presentation/d/1wjkbvQUorD9rzdPWjwPXaJcYPOBnrjE1qUJY2M4xwuY/edit#slide=id.gc6f8badac_0_0>`__

    `W3C Full CSS property table <http://www.w3.org/TR/CSS21/propidx.html>`__

    `Don't Repeat Yourself <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__

    `Download Python <https://www.python.org/downloads/>`__

    `cssutils 1.0.1+ <https://bitbucket.org/cthedot/cssutils>`__

    `watchdog 0.8.2+ <https://pypi.python.org/pypi/watchdog/0.8.3>`__

License
~~~~~~~

    The `MIT license <https://github.com/nueverest/blowdrycss/blob/master/LICENSE>`__

How to Contribute
~~~~~~~~~~~~~~~~~

-  Open an Issue first and get community buy-in.
-  Write Code
-  Write Unit Tests (All tests must pass. 100% coverage preferred.)