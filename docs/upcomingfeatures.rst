Upcoming Features
=================

.. index:: single: Upcoming Features

Make DRYer:
~~~~~~~~~~~

TODO: Implement this essential feature. TODO: Document Currently two
classes are being created with the same properties. The preferred
solution would be to assign both classes to the same property.

Scenario 1:


+-------------------------+-------------------------------------------+
| Value Encoding Format   | CSS Property Value Output                 |
+=========================+===========================================+
| bold                    | .bold { font-weight: bold }               |
+-------------------------+-------------------------------------------+
| font-weight-bold        | .font-weight-bold { font-weight: bold }   |
+-------------------------+-------------------------------------------+

Duplicates the string ``{ font-weight: bold }``.

DRY solution 1


.. code:: css

    .bold, font-weight-bold { font-weight: bold }

Scenario 2:


+-------------------------+-----------------------------------+
| Value Encoding Format   | CSS Property Value Output         |
+=========================+===================================+
| padding-10              | .padding-10 { padding: 10px }     |
+-------------------------+-----------------------------------+
| padding-10px            | .padding-10px { padding: 10px }   |
+-------------------------+-----------------------------------+

Duplicates the string ``{ padding: 10px }``

DRY solution 2


.. code:: css

    .padding-10, .padding-10px { padding: 10px }

Drop requirement for hexadecimal color values to be prefixed with a property name. Implemented: 11/28/2015
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Integrate optional px :point\_right: em Unit Conversion. Implemented: 11/28/2015
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Integrate option hexidecimal :point\_right: rgb() Unit Conversion.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Create Seamless Media Queries for responsive layouts:
'''''''''''''''''''''''''''''''''''''''''''''''''''''

TODO: Implement this really cool feature. TODO: Document

Build responsive scaling fonts using -r:
''''''''''''''''''''''''''''''''''''''''

TODO: Implement this really cool feature. TODO: Document

Encoded Class


font-size-25-r

Resulting CSS media query.


TODO: Add CSS here.

.. code:: css

    .font-size-25-r {
        font-size: 25px;
    }

Sphinx Integration
''''''''''''''''''

TODO: Integrate Sphinx (in progress)
TODO: Put the docs on readthedocs

.. raw:: html

   <!--- Commented
   ##### Pattern Reducer - Find and reduce common patterns in html (skeptical as this reduces
   Assume that the following class pattern appears more than once:
   ```css
   class="padding-10 margin-right-5 margin-left-5 text-align-center"
   ```

   This could be identified and brought to the developers attention.  The developer could manually create a name for the
   replacement class; skip it; or allow class names to be generated automatically, for example, (.bd-1, .bd-2, .blowdry-3).

   ##### Implement using Javascript (consider what this would require)
   TODO: Implement this really cool feature.
   <br>TODO: Document

   ##### Support basic Tween Capability from GreenSock
    TODO: Implement (out of scope for the near future)
    <br>TODO: Document dependencies and basic usage.

   ##### DRY CSS File Analyzer (possibly belongs in a separate project)
   TODO: Return statistics on how many times a given property value appears in a CSS File.
   <br>TODO: Document
   -->