.. meta::
    :author: Michael Eichberg
    :license: Released under the terms of the `2-Clause BSD license`.
    :id: lecturedoc2-tutorial
    :slide-dimensions: 1920x1200

.. role:: red
.. role:: green
.. role:: blue
.. role:: minor
.. role:: obsolete
.. role:: incremental

:math:`LectureDoc^2` Tutorial
=============================

LectureDoc is an authoring system for creating lecture slides/notes/exercises. LectureDoc enables you to write a single (HTML or) reStructuredText document that contains the slides, additional annotations and also exercises.

*Dr. Michael Eichberg*


Basics
-----------

A basic slide consists of a (section) header and some reStructuredText content.

.. admonition:: Example
    :class: footnotesize

    .. class:: margin-above

    .. code:: rst
        :class: black

        Basics
        -----------

        A basic slide consists of a (section) header 
        and some reStructuredText content.


Embedding Formulae
--------------------------------------

Embed math equations using reStructuredText's default directive (``.. math::``) and role (``:math:`...```).

.. admonition:: Example
    :class: footnotesize

    .. container:: two-columns 

        .. container:: column

            The following code:

                .. code:: rst
                  :class: black

                  Computation in :math:`GF(2)`:

                  .. math::

                    \begin{matrix}
                    1 + 1 & = 1 - 1 & = 0 \\
                    1 + 0 & = 1 - 0 & = 1 \\
                    0 + 1 & = 0 - 1 & = 1
                    \end{matrix}

        .. container:: column

            Will render like this:

                Computation in :math:`GF(2)`:
                    
                .. math::

                    \begin{matrix}
                    1 + 1 & = 1 - 1 & = 0 \\
                    1 + 0 & = 1 - 0 & = 1 \\
                    0 + 1 & = 0 - 1 & = 1
                    \end{matrix}


\ 
--

A slide without an explicit title can be created by explicitly creating an empty title:

.. admonition:: Example
    :class: footnotesize

    .. class:: margin-above

    .. code:: rst
        :class: black

        \ 
        --

    .. note:: 

        You have to add a space after the backslash (``\``)!

   

Animation
----------

Basic *appear* animations can be created using the (CSS) class ``incremental``. :incremental:`You can also define a custom role to animate parts of a text.`

.. admonition:: Example
    :class: incremental footnotesize 

    .. class:: margin-above

    .. code:: rst
        :class: black 

        Animation
        ----------

        Basic *appear* animations can be created using the (CSS) class 
        ``incremental``. :incremental:`You can also define a custom 
        role to animate parts of a text.`

        .. admonition:: Example
            :class: incremental

            ...

Advanced Animation
-------------------

In case of lists (`ol` or `ul`) it is sufficient to specify `incremental` in the class attribute of `ol` or `ul`; it is possible, but not necessary to specify the class attribute of every list element.

.. admonition:: Example
    :class: footnotesize 

    .. class:: margin-above

    .. code:: rst
        :class: black 

        ..class:: incremental

        - this
        - is
        - a test


Slide Dimensions
----------------

The slide dimensions can be controlled by specifying the corresponding meta information.
If not specified, the default dimension is set to :math:`1920 \times 1200`; i.e., a ratio of 16:10.
    
.. admonition:: Example
    :class: footnotesize 
    
    In HTML documents add at the following meta tag:

    .. code:: html
        :class: black 

        <meta name="slide-dimensions" content="1600x1200">

    In reStructuredText documents add at the beginning:

    .. code:: rst
        :class: black 

        .. meta::
            :slide-dimensions: 1600x1200


Adding Supplemental Information
---------------------------------

Adding information that should not be on the slides, but provide additional information, can be added using an admonition in combination with the class ``supplemental``.

.. admonition:: Example 
    :class: footnotesize

    .. code:: rst
        :class: black 

        .. admonition:: Formatting Slides
            :class: supplemental

            Creating heavily formatted slides is easily possible 
            using rst directives and roles which are mapped to 
            CSS classes.

.. admonition:: Formatting Slides
            :class: supplemental

            Creating heavily formatted slides is easily possible using rst directives and roles which are mapped to CSS classes.


Creating Section Marker Slides
--------------------------------

Creating a slide which marks the beginning of a new section can be done using the "new-section" class.

.. admonition:: Example 
    :class: footnotesize

    .. code:: rst
        :class: black 

        .. class:: new-section

        <Title of Section>
        -------------------

        ...

        <Title of next Slide>
        ----------------------


Adding Code
--------------------------------

Adding code can be done using reStructuredText's code directive. 

.. admonition:: Example
    :class: footnotesize

    .. container:: two-columns 

        .. container:: column

            The following code:

                .. code:: rst
                    :class: black

                    .. code:: python
                        :class: black

                        for i in range(0,10):
                            print(i)

        .. container:: column

            Will render like this:

                .. code:: python
                  :class: black

                  for i in range(0,10):
                    print(i)


.. class:: new-section

Advanced Formatting    
---------------------

Formatting defined in ``default.css``
--------------------------------------

LectureDoc2's ``default.css`` has some predefined css classes that facilitate the creation of more advanced layouts. While these css classes are defined in the default.css file they are still not considered to be part of the LectureDoc2 core. You are free to adapt them to your needs.


THE NEXT NEEDS TO BE DONE TODODODODODODODODODODODODODOD.......................

Additional horizontal lines
-----------------------------

::

    .. container:: line-above
    
        A container with a line-above.

Renders like this:

.. container:: line-above
    
        A container with a line-above.

Adapting Colors
-----------------

You can define custom roles for the standard colors: .. role

::

    .. role:: red
    .. role:: green
    .. role:: blue
    .. role:: minor


::

    :class: white-background

Sometimes relevant in combination with syntax highlighting)


Controlling Whitespace
-----------------------

::

    .. class:: more-space-between-list-items

    - This is a line
    - And this is a second line with ``more-space-between-list-items``


Renders like this:

.. class:: more-space-between-list-items

- This is a line
- And this is a second line with ``more-space-between-list-items``


::

    .. container:: 

        Test

    Test

    .. container:: margin-below 

        Test
    
    Test

Renders like this:

    .. container:: 

        Test

    Test

    .. container:: margin-below 

        Test
    
    Test


Marking up Text that is in a foreign language
------------------------------------------------

::

    .. role:: eng
    .. role:: ger


Language specific formatting:

::
    .. role:: ger-quote


Other Text Formatting
----------------------

Marking up something as being outdated/obsolete.

::

    .. role:: obsolete



Simple Multi-column layouts
------------------------------

two-columns or three-columns ...