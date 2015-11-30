Advanced Topics
===============

- Use ```watchdog`` <https://pypi.python.org/pypi/watchdog/0.8.3>`__ to automate CSS compilation.
- Learn about clashing aliases and property aliases.
- How to change settings in blowdry.py.
- Customizing the alias dictionary.
- How to build a plugin.
- pro-tip: Want to share your site with a client, co-worker, or colleague. Use `ngrok <https://ngrok.com/>`__
- DRYness
- Syntax

Automate CSS Compilation with Watchdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Having to run ``python blowdry.py`` can annoying in a development environment.
-  What if it were possible to auto-detect that ``index.html`` was saved and automatically
   run ``python blowdry.py``?

   -  This is possible with
      ```watchdog`` <https://pypi.python.org/pypi/watchdog/0.8.3>`__.

-  To setup watchdog run ``pip install watchdog``
-  Navigate to ``/examplesite`` at the command line.
-  From the command line run:

   ``watchmedo shell-command --patterns="*.html;" --ignore-directories --recursive --command="python ../python/blowdry.py"``
-  Now add the class ``margin-150`` to one of the ``<div>`` tags, and
   save ``index.html``
-  Refresh `localhost:8080 <http://localhost:8080>`__ in the browser,
   and the change should appear without manually re-running
   ``blowdry.py``.

What if refreshing the browser doesn't work?
''''''''''''''''''''''''''''''''''''''''''''

-  Ensure ``watchdog`` is running.
-  Check the shell or command prompt where ``watchog`` is running to see
   if there are any error messages.
-  Double check that the command is running in the correct directory,
   and that the python command ``python ../python/blowdry.py`` will run from the directory without
   ``watchdog``.

Watchdog Parameter Modification
'''''''''''''''''''''''''''''''

``--patterns`` can be set to any file type that should trigger
``blowdry.py``. For example: ``--patterns="*.html;*.aspx;*.js"``

``--recursive`` causes the ``watchdog`` to monitor all of the files
matching ``--patterns`` in all subdirectories of the current folder.

``--ignore-directories`` ignores all directory related events, and only
focuses on file changes.

``--command`` contains the path to ``blowdry.py``. Make sure that this
is the correct directory otherwise it will not run.

Find Non-matching classes
~~~~~~~~~~~~~~~~~~~~~~~~~

If the encoded class name contains a typo or invalid value e.g.
``ppadding-5``, ``margin-A``, ``font-color-h000rem``, or
``squirrel-gray`` it will be placed in ``removed_class_set``. The
variable ``removed_class_set`` is found in ``ClassPropertyParser()``
inside of ``classpropertyparser.py``.

Customize Aliases:
~~~~~~~~~~~~~~~~~~

:one: Open ``python/datalibrary.py``

:two: In the ``DataLibrary`` class edit ``self.custom_property_alias_dict``

Change the CSS File Name and Location:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Document how easy it is to edit blowdry.py

DRY-ness must be balanced against other factors.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first three properties are not currently supported by
``blowdrycss``. Eight out of the eleven style lines or 72% of the lines
could be written by hand as encoded classes. However, it would result in
the following really long class attribute:

.. code:: html

    <div class="background-size-cover min-h-7rem bold font-size-3_5625rem white line-height-3_6875rem talign-center
                t-shadow-n2px-2px-4px-rgba-0-0-0-0_5">
        <!-- div contents -->
    </div>

This is a case were the DRY principle is subsumed by the value of
readability, brevity, and encapsulation. Also, just because this tool
can decode the class ``t-shadow-n2px-2px-4px-rgba-0-0-0-0_5`` that
doesn't mean it is intended to be used in this manner.

My CSS is DRY, but my HTML is not.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copying and pasting something like
``p-10-20-11-22 h-50 w-50 talign-center orange font-size-16`` twenty times in an
HTML file is not that DRY either. If this is happening, then it might be
valuable to pause and hand-craft a CSS class for this repeating class selector
pattern.
