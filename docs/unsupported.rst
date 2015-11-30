Unsupported Features
====================

.. index:: single: Unsupported Features

Shorthand properties
''''''''''''''''''''

Use shorthand properties at your own risk. Currently no support is
guaranteed for shorthand properties.

No encoding is defined for '/', comma, dash, double quote, '@'.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

+----------------------------------------+-----------------------------+
| CSS Property Value                     | Encodings Not Implemented   |
+========================================+=============================+
| font: 12px/14px sans-serif             | '/' and '-'                 |
+----------------------------------------+-----------------------------+
| font: 16rem "New Century Schoolbook"   | double quote                |
+----------------------------------------+-----------------------------+
| font-family: Palatino, serif, arial    | comma                       |
+----------------------------------------+-----------------------------+

Properties Values that contain 'url()' are not supported as they are too bulky and verbose. These sorts of
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

``url()`` declarations belong in your custom CSS class definitions.

+---------------------+---------------------------+
| CSS Property Value  | Encodings Not Implemented |
+=====================+===========================+
| background-image:   | '/', '(', and double      |
| url("/home/images/s | quote                     |
| ample/image.png")   |                           |
+---------------------+---------------------------+
