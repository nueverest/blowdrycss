Quick Start Guide
=================

.. index:: single: Quick Start Guide

This guide teaches you how to:

- Setup the tutorial's virtual environment.
- Install :mod:`blowdrycss`.
- Walk through the ``/examplesite`` demo.
- Auto-generate DRY CSS with blowdrycss.
- Rapidly style HTML with encoded class syntax.

.. note::

    *No assumptions are made about your level of proficiency with python.*

Part 1 - Setup virtualenv and install blowdrycss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python is required. Python 3.x is preferred. `Download it here <https://www.python.org/downloads/>`__.
- Check your python installation or version number. Open a command line interface (CLI), and enter the
  following command.  ::

    > python

  Something like the following should appear. ::

    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

  To exit enter: ``exit()`` or press ``Ctrl + q``.

- Create a virtual environment.
  (For the purposes of this tutorial the project folder should be initially empty.) ::

    > pip install virtualenv
    > mkdir blowdrycss_tutorial
    > cd blowdrycss_tutorial
    > virtualenv

- Activate the virtual environment. Verify initial state. ::

    > source bin/activate
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
            blowdrycss_settings.py
            clashing_aliases.html
            index.html
            property_aliases.html
            test.aspx
            test.html
            test.jinja2

- Navigate to ``../blowdrycss_tutorial/examplesite/css``, and verify that ``blowdry.css`` and
  ``blowdry.min.css`` now exist.

- A file ``blowdrycss_settings.py`` appears. This file can be used to modify or override default settings.
  Use of this file is documented in the advanced topics section.

- Two new HTML files ``property_aliases.html`` and ``clashing_aliases.html`` also appear. There is more about
  these files in the advanced topics. In general, they document syntax that can (property_aliases) and
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

Lets actually change something.
'''''''''''''''''''''''''''''''

-  Navigate to ``../blowdrycss_tutorial/examplesite/``

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

-  Ensure that the current folder is ``blowdrycss_tutorial``.

-  Run ``> blowdrycss``

-  Now refresh the web page running on `localhost:8080 <http://localhost:8080>`__.

-  The title at the top of the page should be large and green.


Part 5 - Let's make some more changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Center the image below the title with the class ``text-align-center`` in the ``<div>`` containing the image.

- Find the ``+`` images named ``images/plus.png`` and add the class ``padding-bottom-4p``
  directly to the ``img`` class attribute.

- Ensure that the current folder is ``blowdrycss_tutorial``.

- Run ``> blowdrycss``

- Now refresh the web page running on  `localhost:8080 <http://localhost:8080>`__.

- Feel free to continue experimenting with different property names and values.
  More information about how to form write well-form encoded class names is found on the :doc:`syntax` page.

-  Apply these to an encoded class selectors to an image: ::

    border-10px-solid-black p-20-30-20-30 w-50

   **Decomposition**

   | ``border-10px-solid-black`` Add a solid black border that is 10px thick.
   |
   | ``p-20-30-20-30`` Add 20px padding top and bottom. Add 30px padding left and right.
   |
   | ``w-50`` Make the image 50px wide.


-  Apply this to any div: ``display-none``

-  Apply this to any paragraph tag: ``uppercase``

-  Ensure that the current folder is ``blowdrycss_tutorial``.

-  Run ``> blowdrycss``

|


| **Want to learn more?**
|
| Head on over to :doc:`advancedtopics`.
