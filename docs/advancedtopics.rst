Advanced Topics
===============

.. index:: single: Advanced Topics


- Use `watchdog <https://pypi.python.org/pypi/watchdog/0.8.3>`__ to automate CSS compilation.
- Learn about :doc:`clashing_aliases` and :doc:`property_aliases`.
- How to change settings in ``blowdrycss_settings.py``.
- Customizing the alias dictionary.
- Where are the semicolons?
- How to build a plugin. [missing]
- Non-HTML files (jinja, .NET, and ruby templates). [missing]
- Pro-tip: Want to share your site with a client, co-worker, or colleague. Use `ngrok <https://ngrok.com/>`__.
- DRYness
- Syntax Guide


Automate CSS Compilation with Watchdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: single: Watchdog

- Having to run ``blowdrycss`` can annoying in a development environment.

- What if it were possible to auto-detect that ``index.html`` was saved and automatically run ``blowdrycss``?

- It is possible with `watchdog <https://pypi.python.org/pypi/watchdog/0.8.3>`__.

.. note::

    As of version ``0.1.3`` this is now much easier.


Enable watchdog
'''''''''''''''

- If the virtualenv is not already active, then activate the virtualenv with ``source/bin activate``.

- Navigate to ``<path>/blowdrycss_tutorial`` at the command line.

- Open ``blowdrycss_settings.py``.

- Set ``auto_generate = True``.

- Run ``blowdrycss``.

- Notice that what is printed differs from the default mode.

- Test it by saving a change to one of the project files e.g. change ``<path>/blowdryexample/examplesite/index.html``.


Setting Customization
~~~~~~~~~~~~~~~~~~~~~

The first time the ``blowdrycss`` command is run a file is auto-generated in the current directory named
``blowdrycss_settings.py``. This file provide the ability to override the default settings for a given project.

It is possible to change the directories, file types to discover, unit conversion, output file type, media query
breakpoints, and more.

Find Non-matching classes
~~~~~~~~~~~~~~~~~~~~~~~~~

If the encoded class name contains a typo or invalid value e.g. ``ppadding-5``, ``margin-A``,
``font-color-h000rem``, or ``squirrel-gray`` it will be placed in ``removed_class_set``. The
variable ``removed_class_set`` is found in ``ClassPropertyParser()`` inside of ``classpropertyparser.py``.

One day this may be placed an HTML file for easier discovery of typos or invalid syntax.

Customize Aliases:
~~~~~~~~~~~~~~~~~~

New custom aliases can be assigned as shorthand abbreviation for an official CSS property.

- Open the auto-generated settings file ``blowdrycss_settings.py``.

- Edit ``custom_property_alias_dict``.

**Custom Alias Syntax:**

| custom_property_alias_dict (*dict*) -- Contains customized shorthand encodings for a CSS property name.
  e.g. ``'c-'`` is an alias for ``'color'``. This saves on typing.

| These encoded class selectors can be used inside of Web project files matching ``file_type``.
  They can be customized to your liking.

**Custom Alias Rules:**

- The ``key`` is the official `W3C CSS property name <https://www.w3.org/TR/CSS21/propidx.html>`__.
  Also the ``key`` must exist in the set ``datalibrary.DataLibrary.property_names`` (shown here). ::

    {
        'azimuth', 'background', 'background-attachment', 'background-color', 'background-image',
        'background-position', 'background-repeat', 'border', 'border-bottom', 'border-bottom-color',
        'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-left',
        'border-left-color', 'border-left-style', 'border-left-width', 'border-right', 'border-right-color',
        'border-right-style', 'border-right-width', 'border-spacing', 'border-style', 'border-top',
        'border-radius', 'border-top-left-radius', 'border-top-right-radius', 'border-bottom-right-radius',
        'border-bottom-left-radius',
        'border-top-color', 'border-top-style', 'border-top-width', 'border-width', 'bottom',
        'caption-side', 'clear', 'clip', 'color', 'content', 'counter-increment', 'counter-reset', 'cue',
        'cue-after', 'cue-before', 'cursor', 'direction', 'display', 'elevation', 'empty-cells', 'float',
        'font', 'font-family', 'font-size', 'font-style', 'font-variant', 'font-weight', 'height', 'left',
        'letter-spacing', 'line-height', 'list-style', 'list-style-image', 'list-style-position',
        'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'max-height',
        'max-width', 'min-height', 'min-width', 'opacity', 'orphans', 'outline', 'outline-color', 'outline-style',
        'outline-width', 'overflow', 'padding', 'padding-bottom', 'padding-left', 'padding-right',
        'padding-top', 'page-break-after', 'page-break-before', 'page-break-inside', 'pause', 'pause-after',
        'pause-before', 'pitch', 'pitch-range', 'play-during', 'position', 'quotes', 'richness', 'right', 'speak',
        'speak-header', 'speak-numeral', 'speak-punctuation', 'speech-rate', 'stress', 'table-layout',
        'text-align', 'text-decoration', 'text-indent', 'text-shadow', 'text-transform', 'top', 'unicode-bidi',
        'vertical-align',
        'visibility', 'voice-family', 'volume', 'white-space', 'widows', 'width', 'word-spacing', 'z-index'
    }

.. note::

    If a new key is added to the standard, but not listed here feel free to raise an issue on github.


- The ``value`` is a ``set()`` of custom string aliases.  For example: ::

    {'bgc-', 'bg-c-', 'bg-color-', }

- When adding a new alias it must end with a ``'-'``. Specifically, ``'bgc-'`` is a valid custom alias format.
  If the ``'-'`` is removed, then blowdrycss assumes that ``'bgc'`` expects it to be a valid and
  unique CSS property value (*which it is not*). An example of a valid, unique CSS property value would be ``'bold'``.

- An alias must be unique across all defined aliases. Any alias that clashes with an alias in this dictionary
  or the dictionary auto-generated by ``initialize_property_alias_dict()`` is removed, and becomes unusable.

- Clashing aliases are:
    - Printed when ``get_clashing_aliases()`` is run.
    - Automatically added to the ``project_directory`` as ``clashing_alias.html``.
    - Automatically added to the sphinx docs and can be found under ``/docs/clashing_aliases.rst`` (*requires sphinx*).

**Custom Alias Examples:**

- To add a new alias ``'azi'`` for CSS property ``'azimuth'`` add the ``{key: value, }`` pair
  ``{'azimuth': {'azi-'}, }`` to custom_property_alias_dict. Defining ``'azi-'`` allows the following
  encoded class selector syntax:  ::

    'azi-left-side', 'azi-far-left', ..., 'azi-rightwards'

    <div class="azi-left-side">Azimuth applied to a DIV</div>

**Aliases already known to clash are:**  ::

    'background-color': {'bc-'},
    'border-color': {'bc-', 'border-c-'},
    'border-collapse': {'bc-', 'border-c-'},
    'border-style': {'border-s-', 'bs-'},
    'border-spacing': {'border-s-', 'bs-'},
    'border-right': {'br-'},
    'background-repeat': {'br-'},
    'font-style': {'fs-', 'font-s-'},
    'font-size': {'fs-', 'font-s-'},
    'list-style': {'ls-'},
    'letter-spacing': {'ls-'},
    'max-height': {'mh-'},
    'min-height': {'mh-'},
    'max-width': {'mw-'},
    'min-width': {'mw-'},
    'pause-before': {'pb-'},
    'padding-bottom': {'pb-'},
    'padding-right': {'pr-'},
    'pitch-range': {'pr-'},
    'white-space': {'ws-'},
    'word-spacing': {'ws-'},


Where are the semicolons?
~~~~~~~~~~~~~~~~~~~~~~~~~

After opening ``blowdry.css``, it becomes evident that semicolons are not used for most of the css rule declarations.

Why?
''''

- The only or last css rule { property: value } is not required to end with a semicolon.
  `See section 4.1.8 of the current CSS Standard. <http://www.w3.org/TR/CSS2/syndata.html#declaration>`__

- The auto--generated file ``blowdry.css`` is not intended to be human-editable. Any manual edits are
  over--written when ``blowdrycss`` is run. Generally, when building a CSS file by hand it is considered
  best practise to always include the final semicolon. The reason being that human--error is reduced the
  next time a person adds a rule to the CSS block. However, this does not apply for a file that is only
  machine--edited.

- It is compatible with all browsers.

- It results in faster page loads due to smaller ``*.css`` file size.


DRY-ness must be balanced against other factors.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider the following:

.. code:: html

    <div class="background-size-cover min-h-7rem bold font-size-3_5625rem white line-height-3_6875rem
                talign-center t-shadow-n2px-2px-4px-rgba-0-0-0-0_5">
        <!-- div contents -->
    </div>

This is a case were the DRY principle is subsumed by the value of readability, brevity, and encapsulation.
Creating a custom CSS class selector in this case might be warranted.

Also, just because this tool can decode the class

.. code-block:: html

    t-shadow-n2px-2px-4px-rgba-0-0-0-0_5

that doesn't mean it is intended to be frequently used in this manner.

My CSS is DRY, but my HTML is not.
''''''''''''''''''''''''''''''''''

Copying and pasting something like

.. code-block:: html

    p-10-20-11-22 h-50 w-50 talign-center orange font-size-16 margin-top-30

twenty times in an HTML file is not that DRY from an HTML perspective. If this is happening, then it might be
valuable to pause and hand-craft a CSS class for this repeating class selector pattern.

Syntax Guide
~~~~~~~~~~~~

Continue to :doc:`syntax`.