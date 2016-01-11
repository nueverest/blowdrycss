Read Me
=======

.. index:: single: Read Me

`blowdrycss` is a rapid styling tool that compiles DRY CSS from encoded class selectors in your web project files.

**Why the name blowdrycss?**

Inspiration for the name came from the blow dryer. A blow dryer rapidly drys and styles hair.

Similarly, :mod:`blowdrycss` is used to rapidly style HTML and generate DRY CSS files using encoded class names.

Decomposition
~~~~~~~~~~~~~

-  **Blow** means to expel a current of air causing it to be in a state of motion. Resembles the dynamic nature of the development process.
-  **DRY** stands for `Don't Repeat Yourself <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__.
-  **CSS** stands for Cascading Style Sheets.

Example Usage in HTML Tags:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: html

    <div class="text-align-center margin-top-30">
        <p class="font-size-25">
            The font-size is 25px. <span class="green">Green Text</span>
        </p>
    </div>

:mod:`blowdrycss` decodes the class names ``text-align-center``,
``margin-top-30``, ``font-size-25``, and ``green``; and generates the
following CSS in ``blowdry.css``:

.. code:: css

    .text-align-center { text-align: center }
    .margin-top-30 { margin-top: 30px }
    .font-size-25 { font-size: 25px }
    .green { color: green }

Advantages of blowdrycss
~~~~~~~~~~~~~~~~~~~~~~~~

#. **Rapid Development:** Less time spent writing CSS, and cleaning up unused style rules.
#. **DRY (Don't Repeat Yourself):** Reduces CSS file size by only defining properties once.
#. **Symbiotic:** Can be integrated with the current ecosystem of CSS compliers and frameworks. Is compatible with SASS, SCSS, PostCSS, LESS, Foundation, Bootstrap.
#. **Documented:** Hands-on tutorial and sphinx documentation to get you up and running fast.
#. **Robust:** Built for the real world in which deadlines and division of labor is not always taken into account. Can be used across all phases of a products lifecycle from prototype to production.
#. **Customizable:** Features can be turned on and off inside of ``blowdry.py``. Examples include: minification, unit conversion, color parser, font parser, unit parser.
#. **Extensible:** Build your own plugins.
#. **Standardized:** HTML5 compatible, All `W3C CSS <http://www.w3.org/Style/CSS/Overview.en.html>`__ Level 2.1 and some Level 3 properties implemented, PEP8 Compliant
#. **Tested:** UnitTest Coverage
#. **Permissive:** MIT :doc:`license`

Requirements
~~~~~~~~~~~~

- `Python 2.7.x or 3.x <https://www.python.org/downloads/>`__ (required)
- `cssutils 1.0.1+ <https://bitbucket.org/cthedot/cssutils>`__ (required)
- `future 0.15.2+ <https://pypi.python.org/pypi/future>`__ (required - allows backward compatibility)

Optional
''''''''

- `watchdog 0.8.2+ <https://pypi.python.org/pypi/watchdog/0.8.3>`__ (recommended)
- unittest (run unit tests)
- coverage 4.0.2+ (check test coverage)

Pre-Requisite Knowledge
~~~~~~~~~~~~~~~~~~~~~~~

-  Basic HTML and CSS
-  Zero programming experience required.

Motivation
~~~~~~~~~~

This tool was created after seeing how many companies manage their CSS files. The following are a couple scenarios.

Scenario 1 - Inside a CSS file you find the following:
''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: css

    .header-1 { font-weight: bold; font-size: 12px; font-color: red; }
    .header-2 { font-weight: bold; font-size: 16px; font-color: blue; }
    .header-3 { font-weight: bold; font-size: 12px; font-color: green; }

The property ``font-weight: bold;`` appears three times, and
``font-size: 12px;`` appears twice. This is not DRY (Don't Repeat
Yourself).

Six months later the person who wrote this CSS is then asked to remove
header-2 and header-3 from the homepage. More often than not the
front-end developer will remove the CSS class from the HTML file, but
not from the CSS file.

Some reasons for this include:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Forgetting to delete the rule from the CSS file.
-  Fear that the class is used somewhere else and that it might break
   the site.
-  Being too busy to search all of the files in their project for other
   potential use cases.

The result is that multiple kilobytes worth of unused, dead CSS data
remain.

Scenario 2 - CSS Pre-compiler:
''''''''''''''''''''''''''''''

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
pre-compiler and a for-loop. Some might say, > Well we minified it to
save space.

Yes but,


    Why did you write the same property 500 times into your main CSS
    file?

CSS File size does matter. Large style files result in the following:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Longer download times increase user bounce rates especially on mobile
   devices.
-  Data pollution on the Internet.
-  Increase the likelihood of style bugs.
-  Increase the amount of time required to implement new changes and
   deprecate features.

What it is not
~~~~~~~~~~~~~~

This tool is not designed to replace the need to hand-craft complex CSS property or rule declarations.

* Multi-rule classes, Background images, url() values, multi-word fonts, and shorthand properties are not fully supported.

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

    `W3C Full CSS property table <http://www.w3.org/TR/CSS21/propidx.html>`__

    `Don't Repeat Yourself <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__

    `Python 3.4+ <https://www.python.org/downloads/>`__

    `cssutils 1.0.1+ <https://bitbucket.org/cthedot/cssutils>`__

    `watchdog 0.8.2+ <https://pypi.python.org/pypi/watchdog/0.8.3>`__

License
~~~~~~~

    The MIT :doc:`license` (MIT)

How to Contribute
~~~~~~~~~~~~~~~~~

-  Open an Issue first
-  Write Code
-  Write Unit Tests (All tests must pass. 100% coverage preferred.)
