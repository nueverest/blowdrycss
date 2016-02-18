Tutorial
========

.. index:: single: Tutorial

This guide teaches you how to:

- Setup the tutorial's virtual environment.
- Install :mod:`blowdrycss`.
- Walk through the ``/examplesite`` demo.
- Auto-generate DRY CSS with blowdrycss.
- Rapidly style HTML with encoded class syntax.
- Access more in-depth information.

.. note::

    | *No assumptions are made about your level of proficiency with python.*
    |
    | If this tutorial seems too slow, then go to the :doc:`quickstart`.

Part 1 - Setup virtualenv and install blowdrycss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python is required. Python 3.x is preferred. `It can be downloaded here <https://www.python.org/downloads/>`__.
- Check your python installation or version number. Open a command line interface (CLI), and enter the
  following command.  ::

    > python

  Something *like* the following should appear. ::

    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

  To exit type: ``exit()``.

- Create a virtual environment.
  (For the purposes of this tutorial the project folder should be initially empty.) ::

    > pip install virtualenv
    > mkdir blowdrycss_tutorial
    > cd blowdrycss_tutorial
    > virtualenv

- Activate the virtual environment. Verify initial state. ::

    > source bin/activate (linux, osx) or scripts\activate.bat (windows)
    > python
    >>> exit()
    > pip freeze

- Install ``blowdrycss``. ::

    > pip install blowdrycss
    > pip freeze

- Deactivate virtual environment. ::

    > deactivate



**Explanation:**

| ``pip install virtualenv`` Install virtual environment package from PyPi.
|
| ``mkdir blowdrycss_tutorial`` Create a folder for this tutorial.
|
| ``cd blowdrycss_tutorial`` Sets the current working directory to your web projects directory.
|
| ``virtualenv`` Setup your project up as a virtual environment.
|
| ``source bin/activate`` Activates the new virtual environment.
|
| ``python`` Confirm the version of python that is installed.
|
| ``exit()`` Exit python console.
|
| ``pip freeze`` Shows all of the python packages that are currently installed in the virtual environment.
|
| ``pip install blowdrycss`` Installs blowdrycss and related dependencies 'inside' of your virtual environment.
|
| ``pip freeze`` Shows blowdrycss and the related dependencies after the install.
|
| ``deactivate`` deactivates the virtual environment.

**Good References:**

- `Python Guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
- `The virtualenv docs <http://virtualenv.readthedocs.org/en/latest/userguide.html>`__
- `PyCharm virtualenv How To <https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html>`__


Part 2 - Setup examplesite and run a local webserver.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Download the zip version of ``blowdrycss`` from the `github repository <https://github.com/nueverest/blowdrycss>`__.

- Copy and paste the ``examplesite`` folder into the ``blowdrycss_tutorial`` folder created in Step 1.

- ``cd examplesite``

- Run ``python -m http.server 8080`` (Python 3.x) or
  ``python -m SimpleHTTPServer 8080`` (Python 2.x) depending on your version of python. On Windows the firewall
  might complain. Tell it to allow this server to run.

- Open a web browser and go to `localhost:8080 by clicking here <http://localhost:8080>`__.

- The page should contain lots of unstyled text and images. It should basically be a mess.

- Go back to the command line interface (CLI). The local webserver can be stopped by pressing ``Ctrl + C`` or
  closing the window. If you want to keep the webserver running then you will need to open
  a separate CLI.


Part 3 - Auto-generate CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Look at the files inside of the ``examplesite`` folder. There should be the following: ::

    blowdrycss_tutorial/
        examplesite/
            images/
            index.html
            test.aspx
            test.html
            test.jinja2

- Ensure that the current folder is ``blowdrycss_tutorial``. ::

    > cd ..

- Reactivate the virtualenv and run blowdrycss. ::

    > source bin/activate
    > blowdrycss

- Look at the files inside of the ``examplesite`` folder again. There should be a new subfolder called ``css``
  containing the files ``blowdry.css`` and ``blowdry.min.css``. ::

    blowdrycss_tutorial/
        examplesite/
            css/
                blowdry.css
                blowdry.min.css
            images/
            clashing_aliases.html
            index.html
            property_aliases.html
            test.aspx
            test.html
            test.jinja2
        blowdrycss_settings.py

- Navigate to ``<path>/blowdrycss_tutorial/examplesite/css``, and verify that ``blowdry.css`` and
  ``blowdry.min.css`` now exist.

- A file ``blowdrycss_settings.py`` appears. This file can be used to modify or override default settings.
  Use of this file is documented in the :doc:`advancedtopics` section.

- Two new HTML files ``property_aliases.html`` and ``clashing_aliases.html`` also appear. There is more about
  these files in the :doc:`advancedtopics`. In general, they document syntax that can (property_aliases) and
  cannot be used (clashing_aliases).

- Open a web browser and go to `localhost:8080 <http://localhost:8080>`__.

- The page should now be styled better. Keep in mind that some elements are intentionally left un-styled
  for tutorial purposes.

.. note::

    | The CSS files ``blowdry.css`` and ``blowdry.min.css`` are auto-generated and not intended to be edited by humans.

    | Any manual changes made to these two files are overwritten when ``blowdrycss`` is run.

    | To test this delete the ``css`` folder, and run ``blowdrycss``. The ``css`` will automatically appear
      under examplesite.

Part 4 - Apply new styles in ``index.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage of Encoded Classes in HTML Tags
'''''''''''''''''''''''''''''''''''''

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

Lets actually style something.
''''''''''''''''''''''''''''''

- Navigate to ``<path>/blowdrycss_tutorial/examplesite/``

- Open ``index.html``

- Go to line 12 and find: ::

    <h1 class="c-blue text-align-center display-medium-up font-size-48-s">

- From the class attribute delete ``c-blue`` and replace it with the word ``green``.

- Change ``font-size-48-s`` to ``font-size-148-s``.

- The line should now look like this: ::

    <h1 class="green text-align-center display-medium-up font-size-148-s">

- Save the changes.

- Now refresh the web page running on `localhost:8080 <http://localhost:8080>`__.

- What happened? Nothing happened because you need to run ``blowdrycss`` first.
  Sorry for the trick, but this is the most common reason why it doesn't seem to be working.

- Ensure that the current folder is ``<path>/blowdrycss_tutorial``.

- Run ``> blowdrycss``

- Now refresh the browser for the web page running on `localhost:8080 <http://localhost:8080>`__.

- The title at the top of the page should be large and green.


Part 5 - Exploring the auto-generated CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Navigate to ``<path>/blowdrycss_tutorial/examplesite/css``.

- List the items in the directory ``ls`` or ``dir``.

- The following files should appear: ::

    blowdry.css
    blowdry.min.css

- Both of these files contain the exact same style rules. The only difference is that the one with the ``*.min.css``
  extension in minified. This means that it is smaller and takes less time to upload and download over the Internet.
  However, minified files are not designed to be human-readable. The ``*.css`` is designed to be human-readable.

- Open each file and see the difference.  The ``blowdry.css`` contains line breaks and whitespace.
  Whereas, ``blowdry.min.css`` is written as a single line with whitespace removed.

CSS is Auto-Generated
'''''''''''''''''''''

- Look in ``blowdry.css`` for ``.green``. ::

    .green {
        color: green
        }

- This is the actual CSS that was generated as a result of adding the ``green`` CSS class selector to the
  ``<h1>`` tag.

- Change ``color: green`` to ``color: black``.

- Save ``blowdry.css``.

- Navigate back to ``<path>/blowdrycss_tutorial``

- Run ``blowdrycss``.

- Navigate to ``<path>/blowdrycss_tutorial/examplesite/css``.

- Look in ``blowdry.css`` for the ``.green`` class selector. The CSS is automatically changed
  from ``color: black`` back to ``color: green``. The reason is that ``blowdry.css`` and ``blowdry.min.css``
  are auto-generated. They are both completely overwritten every time ``blowdrycss`` is run.
  The auto-generated CSS files are not human-editable. ::

    .green {
        color: green
        }

  .. important::

    The auto-generated CSS files blowdry.css and blowdry.min.css are not human-editable.
    They are both overwritten each time blowdrycss is run.

Link Tag
''''''''

- Navigate back to ``<path>/examplesite``

- Open ``index.html``

- The following is on line 7: ::

    <link rel="stylesheet" type="text/css" href="css/blowdry.min.css" />

- This line tells the browser which CSS file to use. In this case, it is ``css/blowdry.min.css``. Though
  this could be replaced with ``css/blowdry.css`` and the page would still look the same.
  The minified version causes the web page to load faster since the file is smaller.

- Change line 7 of ``index.html`` to: ::

    <link rel="stylesheet" type="text/css" href="css/blowdry.css" />

- Save ``index.html``.

- Now refresh the web page running on `localhost:8080 <http://localhost:8080>`__.

- The page should still look the same.

- Change line 7 of ``index.html`` back to the way it was. ::

    <link rel="stylesheet" type="text/css" href="css/blowdry.min.css" />

- Save ``index.html``.


Part 6 - Experimentation
~~~~~~~~~~~~~~~~~~~~~~~~

- Center the image below the title with the class ``text-align-center`` in the ``<div>`` containing the image.

- Now (without running ``blowdrycss``) refresh the web page running on  `localhost:8080 <http://localhost:8080>`__.

- It worked. But why? The reason it worked is that ``text-align-center`` is already used in ``index.html``, and
  is already defined in ``blowdry.min.css``.


Padding Percentages and Decimals
''''''''''''''''''''''''''''''''

- Go back to ``index.html`` and find the '+ sign' images named ``images/plus.png``, and
  add the class ``padding-bottom-3p`` directly to the ``img`` class attribute to both of them. They are located
  at lines 19 and 21.

- Ensure that the current folder is ``blowdrycss_tutorial``.

- Run ``> blowdrycss``

- Now refresh the web page running on  `localhost:8080 <http://localhost:8080>`__.

- The '+ sign' images now appear closer to the vertical center, but not quite.

- Open ``index.html`` and change one of the '+ sign' image class selectors from ``padding-bottom-3p`` to
  ``padding-bottom-4_5p``.

- Ensure that the current folder is ``blowdrycss_tutorial``.

- Run ``> blowdrycss``

- Now refresh the web page running on  `localhost:8080 <http://localhost:8080>`__.

- The '+ sign' image with the ``padding-bottom-4_5p`` is now closer to the vertical center.

- What is going on here, and what do the ``p`` and the ``_`` do?

- To understand this better open up ``blowdry.css`` and search for ``padding-bottom-3p``. The following CSS
  is found: ::

    .padding-bottom-3p {
        padding-bottom: 3%
        }

  The ``3p`` property value is converted into ``3%``. So the letter ``p`` allows the percentage sign ``%`` to be
  encoded.

- Now search for ``padding-bottom-4_5p``. The following CSS is found: ::

    .padding-bottom-4_5p {
        padding-bottom: 4.5%
        }

  The ``4_5p`` property value is converted into ``4.5%``. Meaning that the underscore ``_`` represents the decimal
  point ``.`` character.

- Generally, these encodings are necessary because characters like ``.`` and ``%`` are not allowed in class selector
  names (`See here <http://stackoverflow.com/a/449000/1783439>`__).

    - On an advanced note, it is possible to escape the ``.`` and the ``%`` characters in the CSS file like so: ::

        .padding-bottom-4\.5\%

      However, this is hard to read and non-standard CSS. Though it is *valid*. Therefore, escape characters are
      ignored and unsupported by ``blowdrycss``. It is possible to learn more about escape characters
      `here <https://mothereff.in/css-escapes>`__.


Shortcut and Multi-value CSS Properties
'''''''''''''''''''''''''''''''''''''''

- Apply these encoded class selectors to an image: ::

    border-10px-solid-black p-20-30-20-30 w-50

  **Decomposition**

  | ``border-10px-solid-black`` Add a solid black border that is 10px thick.
  |
  | ``p-20-30-20-30`` Add 20px padding top and bottom. Add 30px padding left and right.
  |
  | ``w-50`` Make the image 50px wide.

- Ensure that the current folder is ``<path>/blowdrycss_tutorial``.

- Run ``> blowdrycss``


More Practice
'''''''''''''

- Change ``border-10px-solid-black`` to ``border-10px-dashed-cornflowerblue``.

- Apply ``display-none`` to a div.

- Apply ``uppercase`` to any paragraph tag.

- Feel free to continue experimenting with different property names and values.

  More information about how to write well-form encoded class names is found on the :doc:`syntax` page.

|

| **Want to learn more?**
|
| Head on over to :doc:`advancedtopics`.
