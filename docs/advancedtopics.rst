Advanced Topics
===============

- Use ```watchdog`` <https://pypi.python.org/pypi/watchdog/0.8.3>`__ to automate CSS compilation.
- Learn about clashing aliases and property aliases.
- How to change settings in blowdry.py.
- Customizing the alias dictionary.
- How to build a plugin.
- pro-tip: Want to share your site with a client, co-worker, or colleague. Use `ngrok <https://ngrok.com/>`__
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
