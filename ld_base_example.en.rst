.. meta::
    :version: renaissance
    :author: Michael Eichberg
    :description: LectureDoc2 Tutorial
    :license: Released under the terms of the `2-Clause BSD license`.
    :id: lecturedoc2-tutorial
    :slide-dimensions: 1920x1200
    :master-password: 123456

.. |at| unicode:: 0x40

.. |html-source| source::
    :prefix: https://delors.github.io/
    :suffix: .html 

.. role:: gray
.. role:: red
.. role:: peripheral
.. role:: obsolete
.. role:: incremental


:math:`LectureDoc^2` Tutorial
=============================

LectureDoc is an authoring system for creating lecture material; i. e., lecture slides, notes and exercises from a single document. 

A single LectureDoc document contains discussions of topis which are then used as templates for creating advanced slides as well as a standard document. LectureDoc is intended to be used in combination with rst2ld (reStructuredText to LectureDoc) which is a tool that converts reStructuredText documents into LectureDoc and makes authoring slides as easy as writing a text document. 

This tutorial is written in reStructuredText (*rst* in the following) and can be used as a template for creating your own lecture slides. The *code* of this tutorial is available on GitHub: |html-source|.

*Prof. Dr. Michael Eichberg*

.. container:: footer-left gray

     :Version: 2.0



Basics
-----------

A basic slide consists of a (section) header and some reStructuredText content.

.. example::

    .. code:: rst
        :class: copy-to-clipboard

        Basics
        -----------

        A basic slide consists of a (section) header 
        and some reStructuredText content.


Embedding Formulae
--------------------------------------

Embed math equations using reStructuredText's default directive (``.. math::``) and role (``:math:`...```).

.. example::

    .. grid::

        .. cell:: 

            The following rst fragment:

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                Computation in :math:`GF(2)`:

                .. math::

                    \begin{matrix}
                        1 + 1 & = 1 - 1 & = 0 \\
                        1 + 0 & = 1 - 0 & = 1 \\
                        0 + 1 & = 0 - 1 & = 1
                    \end{matrix}

        .. cell::

            Will render like this:

                Computation in :math:`GF(2)`:
                    
                .. math::

                    \begin{matrix}
                        1 + 1 & = 1 - 1 & = 0 \\
                        1 + 0 & = 1 - 0 & = 1 \\
                        0 + 1 & = 0 - 1 & = 1
                    \end{matrix}


.. class:: no-title

Creating Slides without a Title
---------------------------------

A slide without a title can be created by explicitly creating an empty title.

.. example:: 
    :class: encapsulate-floats

    .. note::

        You have to add a space after the backslash (``\``)!

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        \ 
        --



Alternatively, you can use ``no-title`` in combination with the ``class`` directive if you want to include the slide in an index.

.. example::

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        .. class:: no-title

        I will only show up in an index...
        ------------------------------------




Animation
----------

Basic *appear* animations can be created using the (CSS) class ``incremental``\ [#]_. You can also define a corresponding custom role (``.. role:: incremental``) :incremental:`to animate parts of a text.`

.. example::
    :class: incremental

    .. code:: rst
        :class: copy-to-clipboard 
        :number-lines:

        Animation
        ----------

        Basic *appear* animations can be created using the (CSS) class 
        ``incremental``. You can also define a corresponding custom role 
        (``.. role:: incremental``) :incremental:`to animate parts of a text.`

        .. example::
            :class: incremental

            ...

.. [#] Animation progress can be reset by pressing the ``r`` key.



Animation of Lists
-------------------

In case of (un-)ordered lists (``ol`` or ``ul`` in HTML) it is sufficient to associate the class ``incremental`` using the ``class`` directive with the list. It is also possible, to only specify the class attribute for the required list items.

.. example::

    .. grid::
        
        .. cell::

            The following code:

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                .. class:: incremental

                - this
                - is
                - a test

        .. cell::

            Will render incrementally like this:

                .. class:: incremental

                - this
                - is
                - a test



Slide Dimensions
----------------

The slide dimensions can be controlled by specifying the corresponding meta information.
If not specified, the dimension is set to :math:`1920 \times 1200` (default); i.e., a ratio of 16:10.
    
.. example::
    :class: far-far-smaller 
    
    In HTML documents add the following meta tag:

    .. code:: html
        :class: copy-to-clipboard 

        <meta name="slide-dimensions" content="1600x1200">

    In reStructuredText documents add at the beginning:

    .. code:: rst
        :class: copy-to-clipboard

        .. meta::
            :slide-dimensions: 1600x1200


Associating a document with a unique id
----------------------------------------

Many functions in LectureDoc2 - e.g. persistence of the slide progress - require that a document is associated with a unique id. This id can be set using the meta directive. If no id is set, the respective functions are not available.

.. example::

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        .. meta::
            :id: lecturedoc2-tutorial
            :description: LectureDoc2 Tutorial
            :author: Michael Eichberg
            :license: Released under the terms of the `2-Clause BSD license`.
        


Adding Supplemental Information
---------------------------------

Adding information that should not be on the slides, but provide additional information/explanations, can be added using the ``supplemental`` directive. 

.. example:: 

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        .. supplemental::

            **Formatting Slides**

            Formatting slides is done using classes and roles.



.. supplemental::

    **Formatting Slides**

    Creating heavily formatted slides is easily possible using rst directives and roles which are mapped to CSS classes.


.. class:: new-section transition-flip

Structuring Documents
----------------------


.. class:: transition-move-left

Creating Sections
--------------------------------

Creating a slide which marks the beginning of a new section can be done using the ``new-section`` class.

.. example:: 
    :class: far-far-smaller

    .. code:: rst
        :class: black copy-to-clipboard

        .. class:: new-section

        Structuring Documents
        ----------------------

        .. class:: new-subsection

        Creating Sections
        -----------------


.. class:: transition-move-to-top

Slide Transitions
------------------

Slide transitions can be controlled using the ``transition-...`` classes\ [#]_:

- ``transition-fade``
- ``transition-move-left``
- ``transition-move-to-top``
- ``transition-scale``
- ``transition-flip``

.. example:: 
    :class: far-far-smaller

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        .. class:: transition-move-to-top

        Slide Transitions
        ------------------

.. [#] See the LectureDoc2 Cheat Sheet for a comprehensive list of predefined transitions.


.. class:: transition-scale

Adding Code
--------------------------------

Adding code can be done using reStructuredText's code directive. 

.. example::
    
    .. container:: two-columns 

        .. container:: column

            The following code:

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                .. code:: python
                    :number-lines:

                    for i in range(0,10):
                        print(i)

        .. container:: column

            Will render like this:

                .. code:: python
                    :number-lines:

                    for i in range(0,10):
                    print(i)


.. class:: transition-fade

Links to External Resources
---------------------------

LectureDoc2 supports links to external resources: 
 - https://github.com/Delors/LectureDoc2
 - `LectureDoc2 Sourcecode <https://github.com/Delors/LectureDoc2>`_

.. example:: 

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        LectureDoc2 supports links to external resources: 

        - https://github.com/Delors/LectureDoc2
        - `LectureDoc2 Sourcecode <https://github.com/Delors/LectureDoc2>`_



Links to Internal Targets
-------------------------

LectureDoc2 supports links to external resources: 

- The title of a slide can be used as a link target ➠ `Advanced Formatting`_
- An element which is explicitly marked as a target can be used as a link target:

  ➠ `Link Target in Incremental Block`_

.. example:: 

    .. grid::

        .. cell::

            Slide with explicit marked-up element:

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                Adv. Formatting
                ---------------------

                .. container:: incremental

                  .. _Link Target in Block:

                  See the LectureDoc2 Cheat Sheet.

        .. cell::

            References are defined as follows:

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                Links to internal targets: 

                - Link to slide: `Adv. Formatting`_
                - Link to a marked-up element: 
                
                  `Link Target in Block`_


Scientific Citations
--------------------

Citations are fully supported in LectureDoc2.

A reference to a book: [Martin2017]_ (Details are found in the bibliography (see next slide)).

.. example:: 

    .. code:: rst
        :class: copy-to-clipboard

        A reference to a book: [Martin2017]_



Bibliography
------------

- .. [Martin2017] Clean Architecture: A Craftsman's Guide to Software Structure and Design; Robert C. Martin, Addison-Wesley, 2017
- ...

.. example:: 

    .. code:: rst
        :class: copy-to-clipboard


        .. [Martin2017] Clean Architecture: ...; Robert C. Martin, Addison-Wesley, 2017



Advanced Formatting    
---------------------

LectureDoc comes with a set of predefined (CSS) classes that can be used to format the slides. Some of these classes have explicit support by LectureDoc and will be rendered differently in the different situations (e.g., document view vs. slide view will render *stacked layouts* or *supplemental information* differently). 

.. class:: incremental

- :red:`red`
- :peripheral:`peripheral`
- :obsolete:`obsolete`

.. container:: incremental

    .. _Link Target in Incremental Block:

    `See the LectureDoc2 Cheat Sheet for a comprehensive list of predefined CSS classes.`


Stacked layouts
----------------

Stacked layouts enables updating parts of a slide by putting the content into layers and then showing the layers incrementally.

.. example:: 

    .. container:: two-columns smaller

        .. container:: column

            .. deck:: monospaced

                .. card::

                    :gray:`This text is gray.`

                .. card:: overlay

                    .. raw:: html

                        <svg width="600" height="80">
                            <rect width="600" height="80" 
                                  style="fill:rgb(0,0,255,0.25);stroke-width:1;stroke:rgb(0,0,0)" />
                        </svg>

        .. container:: column 

            .. code:: rst
                :class: black copy-to-clipboard 

                .. deck:: monospaced

                  .. card::

                    :gray:`This text is gray.`

                  .. card:: overlay

                    .. raw:: html

                      <svg width="600" height="80">
                      ⇥ ⇥<rect width="600" height="80" 
                      ⇥ ⇥ ⇥ ⇥ ⇥style="fill:rgb(0,0,255,0.25);
                      ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ stroke-width:1;
                      ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ ⇥ stroke:rgb(0,0,0)" />
                      </svg>


Presenter-Notes
----------------

Presenter notes can be added to a slide using the ``presenter-note`` directive. 

**A presenter note - including its presence - is only visible after entering the master password** (press ``m`` and then enter: ``123456``).

.. presenter-note::

    This is a short presenter note. Presenter notes can contain complex content, e.g., images, code, or math formulae.

.. example:: 

    .. code:: rst
        :class: copy-to-clipboard
        :number-lines:

        .. presenter-note::

            This is a presenter note.

            It is only visible after entering the master password (123456).


.. class:: exercises

Integrated Exercises
---------------------

Exercises can be integrated into the slide set.

.. example:: 

    .. container:: two-columns

        .. container:: column

            .. exercise:: Exercise: 1+1

                Compute: :math:`\sqrt 2 = ?`

                .. solution::
                    :pwd: sqrt

                    Solution: :math:`1,4142135624`.

            To unlock the solution go to the document view and enter the password (sqrt).
    
        .. container:: column
            
            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                .. exercise:: Exercise: 1+1

                    Compute: :math:`\sqrt 2 = ?`.

                    .. solution::
                        :pwd: sqrt

                        Solution: :math:`1,4142135624`.

If you have multiple exercises, you can define a master password (123456) to unlock all solutions at once (press ``m`` to open the dialog).

.. code:: rst 
    :class: copy-to-clipboard

    .. meta::
        :master-password: 123456



.. class:: new-section transition-fade

Images
-------


.. class:: no-title padding-none transition-scale

Image in the Background (Hack)
-------------------------------

.. deck::

    .. card:: 

        .. image:: ld_base_example/tag_cloud.png
            :width: 100%
            :align: center

    .. card:: overlay

        .. example:: 
            :class: backdrop-blur margin-0-5em

            .. code:: rst
                :class: copy-to-clipboard
                :number-lines:

                .. class:: padding-none no-title transition-scale

                Image in the Background 
                ------------------------

                .. deck:: 

                    .. card::

                        .. image:: ld_base_example/tag_cloud.png
                            :width: 100%
                            :align: center

                    .. card:: overlay

                        Content on the slide...

