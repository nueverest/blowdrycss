Quick Start Guide
=================

.. index:: single: Quick Start Guide

This guide teaches you how to:

- Install :mod:`blowdrycss`
- Run the '/examplesite' demo.
- Auto-generate DRY CSS.
- Rapidly style your html with encoded classes.

Part 1 - Start the web browser to view the unstyled examplesite.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Download the :mod:`blowdrycss` `zip-file here <https://github.com/nueverest/blowdrycss/archive/master.zip>`_.
-  Navigate to ``../blowdrycss/examplesite``
-  Run ``python -m http.server 8080`` (Python 3.x) or
   ``python -m SimpleHTTPServer 8080`` (Python 2.x)
-  Open a web browser and go to
   `localhost:8080 <http://localhost:8080>`__ or click the link
-  The page should contain lots of un-styled text and images.

Part 2 - Auto-generate CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Navigate to ``../blowdrycss/python``
-  Run ``pip install -r requirements.txt`` If pip is not install `go
   here <https://pip.pypa.io/en/latest/installing/>`__.
-  Run ``python blowdry.py``
-  Navigate to ``../blowdrycss/examplesite/css`` and verify that
   ``blowdry.css`` and ``blowdry.min.css`` now exist.
-  Open a web browser and go to
   `localhost:8080 <http://localhost:8080>`__.
-  The page should now be styled better.

Notes about the auto-generated ``*.css`` files
''''''''''''''''''''''''''''''''''''''''''''''

| The CSS files ``blowdry.css`` and ``blowdry.min.css`` are not intended
  to be edited by humans.
| Any manual changes made to these two files are overwritten when
  ``python blowdry.py`` is run.

Part 3 - Apply new styles in ``index.html``
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

-  Navigate to ``../blowdrycss/examplesite``
-  Open ``index.html``
-  Find the line

   ``<h1 class="c-blue text-align-center">Blow Dry CSS</h1>``
-  From the class attribute delete ``c-blue`` and replace it with the
   word ``green``
-  Add the class ``font-size-148``
-  The line should now look like this

   ``<h1 class="green font-size-148 text-align-center">Blow Dry CSS</h1>``
-  Now refresh the web page running on
   `localhost:8080 <http://localhost:8080>`__.
-  What happened? Nothing happened because you need to run
   ``blowdry.py``
-  Navigate to ``../blowdrycss/python``
-  Run ``python blowdry.py``
-  Now refresh the web page running on
   `localhost:8080 <http://localhost:8080>`__.
-  The title at the top of the page should be large and green.

Let's make some more changes.
'''''''''''''''''''''''''''''
-  Center the image below the title with the class ``t-align-center`` in
   the ``<div>`` containing the image.
-  Find the ``+`` images and add the class ``padding-bottom-4p``
   directly to the ``img`` class attribute.
-  Run ``python blowdry.py``
-  Now refresh the web page running on
   `localhost:8080 <http://localhost:8080>`__.
-  Feel free to continue experimenting with different property names and
   values. More information about how to form write well-form encoded
   class names is found further down this page.

Part 4 - Experiment with these classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Apply these to an image: ``border-10px-solid-black``
   ``p-20-30-20-30`` ``w-50``
-  Apply this to a div: ``display-none``
-  Apply this to text: ``uppercase``
-  Run ``python blowdry.py``


Want to learn more head on over to :doc:`advancedtopics`.
