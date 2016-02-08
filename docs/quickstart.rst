Quick Start Guide
=================

.. index:: single: Quick Start Guide

This guide teaches you how to:

- Install :mod:`blowdrycss`.
- Run the '/examplesite' demo.
- Auto-generate DRY CSS.
- Rapidly style your HTML with encoded class syntax.

*No assumptions are made about your level of proficiency with python.*

Part 1 - Setup virtualenv and install blowdrycss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python is required. Python 3.x is preferred. `Download it here <https://www.python.org/downloads/>`__.
- Check your python installation or version number. Open a command line interface (cli), and enter the
  following command.  ::

    python

  Something like the following should appear. ::

    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

  To exit enter: ``exit()`` or press ``Ctrl + q``.

- Create a virtual environment.
  (For the purposes of this tutorial the project folder should be initially empty.) ::

    pip install virtualenv
    cd name_of_project_folder
    virtualenv

- Activate the virtual environment. Verify initial state. ::

    source bin/activate
    python
    >>> exit()
    pip freeze

- Install ``blowdrycss``. ::

    pip install blowdrycss
    pip freeze

- Deactivate virtual environment. ::

    deactivate



**Explanation:**

| ``pip install virtualenv`` Install virtual environment package from PyPi.
|
| ``cd name_of_project_folder`` Sets the current working directory to your web projects directory.
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

**References:**

- `Python Guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
- `The virtualenv docs <http://virtualenv.readthedocs.org/en/latest/userguide.html>`__
- `PyCharm virtualenv How To <https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html>`__


Part 2 - Setup examplesite and run a local webserver.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Download ``blowdrycss`` from the `github repo <https://github.com/nueverest/blowdrycss>`__.

- Copy and paste the ``examplesite`` folder into the empty project folder.

- ``cd examplesite``

- Run ``python -m http.server 8080`` (Python 3.x) or
  ``python -m SimpleHTTPServer 8080`` (Python 2.x) depending on your version of python.

- Open a web browser and go to `localhost:8080 or click this link <http://localhost:8080>`__.

- The page should contain lots of unstyled text and images. It should basically be a mess.

- The local webserver can be stopped by pressing ``Ctrl + C`` or closing the window.
  If you want to keep the webserver running then you will need to open another command line interface (cli).


Part 3 - Auto-generate CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Look at the files inside of the ``examplesite`` folder. There should be the following: ::

    name_of_project_folder/
        examplesite/
            images/
            index.html
            test.aspx
            test.html
            test.jinja2

- Reactivate the virtualenv and run blowdrycss. ::

    source bin/activate
    blowdrycss

- Look at the files inside of the ``examplesite`` folder again. There should be a new subfolder called ``css``
  containing the files ``blowdry.css`` and ``blowdry.min.css``. ::

    name_of_project_folder/
        examplesite/
            css/
                blowdry.css
                blowdry.min.css
            ...

- Navigate to ``../name_of_project_folder/examplesite/css``, and verify that ``blowdry.css`` and ``blowdry.min.css`` now exist.

- Open a web browser and go to `localhost:8080 <http://localhost:8080>`__.

- The page should now be styled better (but not completely).

.. note::

    | The CSS files ``blowdry.css`` and ``blowdry.min.css`` are auto-generated and not intended to be edited by humans.

    | Any manual changes made to these two files are overwritten when ``blowdrycss`` is run.

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

Lets actually change something.
'''''''''''''''''''''''''''''''

-  Navigate to ``../name_of_project_folder/examplesite/``

-  Open ``index.html``

-  Find the line

   ``<h1 class="c-blue text-align-center">Blow Dry CSS</h1>``
-  From the class attribute delete ``c-blue`` and replace it with the word ``green``.

-  Add the class ``font-size-148``

-  The line should now look like this ::

    <h1 class="green font-size-148 text-align-center">Blow Dry CSS</h1>

-  Now refresh the web page running on `localhost:8080 <http://localhost:8080>`__.

-  What happened? Nothing happened because you need to run ``blowdrycss`` first.
   Sorry for the trick, but this is the most common reason why it doesn't seem to be working.

-  Run ``blowdrycss``

-  Now refresh the web page running on `localhost:8080 <http://localhost:8080>`__.

-  The title at the top of the page should be large and green.


Part 5 - Let's make some more changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Center the image below the title with the class ``text-align-center`` in the ``<div>`` containing the image.

- Find the ``+`` images named ``images/plus.png`` and add the class ``padding-bottom-4p``
  directly to the ``img`` class attribute.

- Run ``blowdrycss``

- Now refresh the web page running on  `localhost:8080 <http://localhost:8080>`__.

- Feel free to continue experimenting with different property names and values.
  More information about how to form write well-form encoded class names is found on the :doc:`syntax` page.

-  Apply these to an encoded class selectors to an image: ::

    border-10px-solid-black p-20-30-20-30 w-50

-  Apply this to any div: ``display-none``

-  Apply this to any paragraph tag: ``uppercase``

-  Run ``blowdrycss``

|


| **Want to learn more?**
|
| Head on over to :doc:`advancedtopics`.
