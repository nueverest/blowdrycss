Quick Start Guide
=================

.. index:: single: Quick Start Guide

This guide rapidly shows you how to:

- Setup a virtual environment.
- Install :mod:`blowdrycss`.
- Walk through the ``/examplesite`` demo.
- Auto-generate DRY CSS with blowdrycss.
- Rapidly style HTML with encoded class syntax.
- Access more in-depth information.

.. note::

    If this guide seems too quick, then head over to the :doc:`tutorial` instead.

::

    > pip install virtualenv
    > mkdir blowdrycss_tutorial
    > cd blowdrycss_tutorial
    > virtualenv
    > source bin/activate
    > pip install blowdrycss

- Download the zip version of ``blowdrycss`` from the `github repository <https://github.com/nueverest/blowdrycss>`__.

- Copy and paste the entire ``examplesite`` folder from the downloaded zip file to the new ``blowdrycss_tutorial`` folder.

- Look at the files inside of the ``examplesite`` folder. There should be the following: ::

    blowdrycss_tutorial/
        examplesite/
            images/
            index.html
            test.aspx
            test.html
            test.jinja2

- Open a new Command Line Interface (CLI). ::

    > cd <path to>/blowdrycss_tutorial/examplesite
    > python -m http.server 8080            # (Python 3.x)
    > python -m SimpleHTTPServer 8080       # (Python 2.x)

- Open a web browser and go to `localhost:8080 by clicking here <http://localhost:8080>`__.

- The page should contain lots of unstyled text and images. It should basically be a mess.

- Leave the web server running, and go back to the original CLI.

- Ensure that the current folder is ``blowdrycss_tutorial``. Run blowdrycss. ::

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
  these files in the :doc:`advancedtopics`.

- Open ``<path>/blowdrycss_tutorial/examplesite/index.html``

- Go to line 12 and find: ::

    <h1 class="c-blue text-align-center display-medium-up font-size-48-s">

- From the class attribute delete ``c-blue`` and replace it with the word ``green``.

- Change ``font-size-48-s`` to ``font-size-148-s``.

- The line should now look like this: ::

    <h1 class="green text-align-center display-medium-up font-size-148-s">

- Save the changes.

- Ensure that the current folder is ``<path>/blowdrycss_tutorial``.

- Run ``> blowdrycss``

- Now refresh the browser for the web page running on `localhost:8080 <http://localhost:8080>`__.

- The title at the top of the page should be large and green.


| **Syntax**
|
| More information about how to write well-form encoded class names is found on the :doc:`syntax` page.
|
|
| **Want to learn more?**
|
| Go to Part 5 of the :doc:`tutorial`.
|
| Head on over to :doc:`advancedtopics`.
