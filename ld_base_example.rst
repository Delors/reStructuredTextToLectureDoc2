.. meta::
    :author: Michael Eichberg
    :license: Released under the terms of the `2-Clause BSD license`.

:math:`LectureDoc^2` Tutorial
=============================

LectureDoc is an authoring system for creating lecture slides/notes/exercises. LectureDoc enables you to write a single (HTML or) reStructuredText document that contains the slides, additional annotations and also exercises.

*Dr. Michael Eichberg*


Basics
-----------

A basic slide consists of a (section) header and some reStructuredText content.

.. admonition:: Example

    ::

        First Slide
        -----------------

        A basic slide...


Embedding Formulae
--------------------------------------

You can embed math equations in your slides using reStructuredText's default directives (``.. math::``) and roles (``:math:`...```).

.. admonition:: Example
    :class: smaller

    .. container:: two-columns

        .. container:: column

            The following code:

                ::

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

    ::

        \ 
        --

    .. note::
        You have to add a space after the backslash (``\``)!


Animation
----------

Basic *appear* animations can be created using the (CSS) class ``incremental``.


Slide Dimensions
----------------

The slide dimensions can be controlled by specifying the corresponding meta information.
If not specified, the default dimension is set to :math:`1920 \times 1200`; i.e., a ratio of 16:10.
    
    