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

- Open ``python/datalibrary.py``

- In the ``DataLibrary`` class edit ``self.custom_property_alias_dict``


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