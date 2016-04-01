Syntax -- Encoded Class Formatting Rules
========================================

.. index:: single: Syntax - Encoded Class Formatting Rules

Dissecting a CSS Statement
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: css

    .margin-10 { margin: 10px !important; }

+----------+-----------------+------------------+--------------+
| Format   | Property Name   | Property Value   | Priority     |
+==========+=================+==================+==============+
| CSS      | .margin-10      | margin: 10px     | !important   |
+----------+-----------------+------------------+--------------+

Dissecting Encoded CSS Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-----------------+--------------------------+------------------+-------------------------------------+
| Encoded Class   | Property Name or Alias   | Property Value   | CSS Rule Output                     |
+=================+==========================+==================+=====================================+
| font-size-25    | font-size-               | 25               | .font-size-25 { font-size: 25px }   |
+-----------------+--------------------------+------------------+-------------------------------------+
| green           | color-                   | green            | .green { color: green }             |
+-----------------+--------------------------+------------------+-------------------------------------+
| p-70-10         | p-                       | 70px 10px        | .p-70-10 { padding: 70px 10px }     |
+-----------------+--------------------------+------------------+-------------------------------------+

Dashes separate words in multi-word property names and aliases.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Property Names is a valid CSS property name in accordance with the `W3C Full CSS property table <http://www.w3.org/TR/CSS21/propidx.html>`__


``font-weight, border-bottom-color, border-bottom-style, border-bottom-width, border-collapse``

Dashes are placed at the end of aliases to indicate that it's an alias and not a css property name.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aliases for property names.


``f-weight-, bg-c-, bg-color-, t-align-``

Property names may be encoded as an alias.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider this dictionary key, value pair found in ``datalibrary.py``
dictionary ``DataLibrary.self.custom_property_alias_dict``.

``'font-weight': {'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'},``

It maps the alias set
``{'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'}``
to the property name ``font-weight``. Meaning that any of the values in
the set can be substituted for ``font-weight``.

The full property name can also be used directly in the encoded class
i.e. ``font-weight-``.

Dashes separate CSS property name/alias from property value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------+-------------------------------------------------+
| Encoded Class Format   | CSS Rule Output                                 |
+========================+=================================================+
| property-name-value    | .property-name-value { property-name: value }   |
+------------------------+-------------------------------------------------+
| alias-value            | .alias-value { property-name: value }           |
+------------------------+-------------------------------------------------+
| font-weight-700        | .font-weight-700 { font-weight: 700 }           |
+------------------------+-------------------------------------------------+
| fw-700                 | .fw-700 { font-weight: 700 }                    |
+------------------------+-------------------------------------------------+

Dashes separate multiple values for properties that take multiple values.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------+-----------------+
| Encoded Class Format   | CSS Rule Output |
+========================+=================+
| alias-value-value-valu | .alias-value-va |
| e-value                | lue-value-value |
|                        | {               |
|                        | property-name:  |
|                        | value value     |
|                        | value value }   |
+------------------------+-----------------+
| padding-10-20-10-10    | .padding-10-20- |
|                        | 10-10           |
|                        | { padding: 10px |
|                        | 20px 10px 10px  |
|                        | }               |
+------------------------+-----------------+
| p-10-20-10-10          | .p-10-20-10-10  |
|                        | { padding: 10px |
|                        | 20px 10px 10px  |
|                        | }               |
+------------------------+-----------------+

Dashes separate ``!important`` priority indicator ``'-i'`` (append to the end of the string)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------+---------------------+
| Encoded Class Format   | CSS Rule Output     |
+========================+=====================+
| alias-value-i          | .alias-value-i      |
|                        | {                   |
|                        | property-name:      |
|                        | value               |
|                        | !important }        |
+------------------------+---------------------+
| font-weight-bold-i     | .font-weight-bold-i |
|                        | { font-weight:      |
|                        | bold !important     |
|                        | }                   |
+------------------------+---------------------+

Shorthand can be used in cases where the alias is unambiguously the css property value.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Applicable properties include: ``color``, ``font-weight``,
``font-style``, ``text-decoration``, and ``text-transform``.

+------------------------+---------------------------------------------+
| Encoded Class Format   | CSS Rule Output                             |
+========================+=============================================+
| alias                  | .alias { property-name: alias }             |
+------------------------+---------------------------------------------+
| purple                 | .purple { color: purple }                   |
+------------------------+---------------------------------------------+
| bold                   | .bold { font-weight: bold }                 |
+------------------------+---------------------------------------------+
| lighter                | .lighter { font-weight: lighter }           |
+------------------------+---------------------------------------------+
| underline              | .underline { text-decoration: underline }   |
+------------------------+---------------------------------------------+
| italic                 | .italic { font-style: italic }              |
+------------------------+---------------------------------------------+
| lowercase              | .lowercase { text-transform: lowercase }    |
+------------------------+---------------------------------------------+

Built-in CSS Property Values containing '-' are now valid.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Implemented: 11/29/2015 version: 0.0.2

See ``custom_property_alias_dict`` in ``datalibrary.py`` for a
comprehensive list of usable aliases. Note that not every built-in CSS
property value `defined
here <http://www.w3.org/TR/CSS21/propidx.html>`__ is implemented. The
reason is that some values like 'right' and 'left' are used for more
than one property name. Also, in the case of ``font-weight`` numbers are
defined like '100', '200', and so on. Encoded CSS classes are not
permitted begin with a number and are therefore excluded.

+-------------------------+-----------------------------+
| Value Encoding Format   | CSS Property Value Output   |
+=========================+=============================+
| sans-serif              | font-family: sans-serif     |
+-------------------------+-----------------------------+
| x-large                 | font-size: x-large          |
+-------------------------+-----------------------------+

CSS Web Safe Font Fallbacks are now Auto-Generated for ``font-family``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Implemented: 11/29/2015 version: 0.0.2

Per
`w3schools.com <http://www.w3schools.com/cssref/css_websafe_fonts.asp>`__
> The font-family property should hold several font names as a
"fallback" system, to ensure maximum compatibility between
browsers/operating systems. If the browser does not support the first
font, it tries the next font.

+----------------------+----------------------------------------------+
| Font Name as Alias   | CSS Rule Output                              |
+======================+==============================================+
| arial                | .arial { font-family: arial, sans-serif }    |
+----------------------+----------------------------------------------+
| papyrus              | .papyrus { font-family: papyrus, fantasy }   |
+----------------------+----------------------------------------------+

Color Declarations
~~~~~~~~~~~~~~~~~~

+--------------+------------------------+-----------------+
| Color Format | Encoded Class Format   | CSS Rule Output |
+==============+========================+=================+
| keyword      | color-silver           | .color-silver { |
|              |                        | color: silver } |
+--------------+------------------------+-----------------+
| rgb          | color-rgb-0-255-0      | .color-rgb-0-25 |
|              |                        | 5-0             |
|              |                        | { color: rgb(0, |
|              |                        | 255, 0) }       |
+--------------+------------------------+-----------------+
| rgba         | color-rgba-255-0-0-0\_ | .color-rgba-255 |
|              | 5                      | -0-0-0\_5       |
|              |                        | { color:        |
|              |                        | rgba(255, 0, 0, |
|              |                        | 0.5) }          |
+--------------+------------------------+-----------------+
| hex6         | color-h0ff23f (prepend | .color-h0ff23f  |
|              | 'h')                   | { color:        |
|              |                        | #0ff23f }       |
+--------------+------------------------+-----------------+
| hex6         | h0ff23f                | .h0ff23f {      |
|              |                        | color: C#0ff23f |
|              |                        | }               |
+--------------+------------------------+-----------------+
| hex3         | color-h03f (prepend    | .color-h03f {   |
|              | 'h')                   | color: #03f }   |
+--------------+------------------------+-----------------+
| hex3         | hfd4                   | .hfd4 { color:  |
|              |                        | C#fd4 }         |
+--------------+------------------------+-----------------+
| hsl          | color-hsl-120-60p-70p  | .color-hsl-120- |
|              |                        | 60p-70p         |
|              |                        | { color:        |
|              |                        | hsl(120, 60%,   |
|              |                        | 70%) }          |
+--------------+------------------------+-----------------+
| hsla         | color-hsla-120-60p-70p | .color-hsla-120 |
|              | -0\_3                  | -60p-70p-0\_3   |
|              |                        | { color:        |
|              |                        | hsl(120, 60%,   |
|              |                        | 70%, 0.3) }     |
+--------------+------------------------+-----------------+

Negative Values
~~~~~~~~~~~~~~~

'n' :point\_right: '-'

Value Encoding Format \| CSS Property Value Output ---------------------
\| ------------------------- 'n48' \| '-48' 'n5cm n6cm' \| '-5cm -6cm'
'n9in' \| '-9in' ###### Note that the 'n' at the end of ``-9in`` is not
affected.

Use underscores to indicate Decimal point.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'1\_25' :point\_right: '1.25'

+-------------------------+-----------------------------+
| Value Encoding Format   | CSS Property Value Output   |
+=========================+=============================+
| '1\_32rem'              | '1.32rem'                   |
+-------------------------+-----------------------------+

Special Note: Underscores can 'only' be used as decimal points.


Other usage of underscores will invalidate the class. e.g. 'padding\_1',
'*padding-1', or 'padding-1*' are considered invalid and will not be
decoded. Classes may still be defined with these names, but CSS would
not be generated by this tool.

Using Percentages 'p' becomes '%'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'p' :point\_right: '%'

+-------------------------+-----------------------------+
| Value Encoding Format   | CSS Property Value Output   |
+=========================+=============================+
| '1p-10p-3p-1p'          | '1% 10% 3% 1%'              |
+-------------------------+-----------------------------+
| '32p'                   | '32%'                       |
+-------------------------+-----------------------------+

Default Units:
~~~~~~~~~~~~~~

If units are not provided in the class name, then default units were
applicable. The default units are defined in
``UnitParser.default_property_units_dict`` inside ``unitparser.py``.
This makes it possible to easily change the default units for a
particular property name.

+-------------------------+-----------------------------+
| Value Encoding Format   | CSS Property Value Output   |
+=========================+=============================+
| padding-50              | padding: 50px               |
+-------------------------+-----------------------------+
| elevation-20            | elevation: 20deg            |
+-------------------------+-----------------------------+

Optional Unit Conversion
~~~~~~~~~~~~~~~~~~~~~~~~

- Implemented: 11/28/2015 in version: 0.0.2

To enable 'px' to 'em' unit conversion open ``blowdrycss.py`` and set
``use_em = True``

Explicitly Encoding Units in Class Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------+-----------------------------+
| Value Encoding Format   | CSS Property Value Output   |
+=========================+=============================+
| padding-50cm            | padding: 50cm               |
+-------------------------+-----------------------------+
| width-120vmin           | width: 120vmin              |
+-------------------------+-----------------------------+

Media Queries using Breakpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Implemented: 1/2/2016 in version: 0.0.6

- Valid Formats ::

    # General case
    'property name/alias' + 'breakpoint_key' + 'limit_key'

    # Special case -- Implied property_name is 'display'.
    # Allows elements to be visible or hidden.
    'breakpoint_key' + 'limit_key'

- Breakpoint keys -- See ``blowdrycss_settings.py`` if you want to customize these. ::

    'xxsmall-', 'xsmall-', 'small-', 'medium-', 'large-',
    'xlarge-', 'xxlarge-', 'giant-', 'xgiant-', 'xxgiant-'

- Limit keys ::

   'only', 'down', 'up'

- Breakpoints and limits combined. CSS property name defaults to ``display``. ::

    xxsmall-up
    medium-only
    xxlarge-down

- Custom CSS Property with breakpoint and limit suffix. ::

    bold-small-only
    color-hfff-giant-down
    text-align-center-large-up

- Set Custom Breakpoints 4/1/2016 as of version 0.1.8.
  Breakpoints can now be set by specifying a screen width as a custom breakpoint before the limit key
  ``-up`` or ``-down``.  The limit key ``-only`` is excluded since it would only apply when the width is an exact
  match. Units default to pixels if not specified.  Unit conversion still applies if ``use_em = True`` in
  blowdrycss_settings.py. ::

    padding-25-820-up
    display-480-down
    margin-5-2-5-2-1000-up
    display-960-up-i
    display-3_2rem-down

----------------------

**Value Encoding Format**

``display-medium-up``

**CSS Media Query Output** ::

    @media only screen and (max-width: 30.0625em) {
        .display-medium-up { display: none }
    }

----------------------

**Value Encoding Format**

``large-up`` -- Property name ``'display-'`` is optional.

**CSS Media Query Output** ::

    @media only screen and (max-width: 45.0625em) {
        .large-up { display: none }
    }

----------------------

**Value Encoding Format**

``giant-down`` -- Property name ``'display-'`` is optional.

**CSS Media Query Output** ::

    @media only screen and (min-width: 160.0em) {
        .giant-down { display: none }
    }

----------------------

**Value Encoding Format**

``padding-100-large-only``

**CSS Media Query Output** ::

    @media only screen and (min-width: 45.0625em) and (max-width: 64em) {
        .padding-100-large-only { padding: 6.25em }
    }

----------------------

Media Queries using Scaling Flag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Implemented: 1/2/2016 in version: 0.0.6

- Allows scaling of ``'font-size'`` or other pixel--based CSS property as the screen width is reduced.

- Just add ``'-s'`` or ``'-s-i'`` to the end of your encoded class selector.

----------------------

**Value Encoding Format**

``font-size-48-s``

**CSS Media Query Output** ::

    .font-size-48-s { font-size: 3em }

    @media only screen and (max-width: 45em) {
        .font-size-48-s { font-size: 2.6667em }
    }
    @media only screen and (max-width: 30em) {
        .font-size-48-s { font-size: 2.4em }
    }

----------------------

**Value Encoding Format**

``font-size-16-s-i`` -- !important global override case

**CSS Media Query Output** ::

    .font-size-16-s-i { font-size: 1em !important }

    @media only screen and (max-width: 45em) {
        .font-size-16-s-i { font-size: 0.8889em !important }
    }
    @media only screen and (max-width: 30em) {
        .font-size-16-s-i { font-size: 0.8em !important }
    }
