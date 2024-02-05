.. meta:: 
    :author: Michael Eichberg
    :keywords: LectureDoc2, "Cheat Sheet", DHBW
    :description lang=de: Cheat Sheet für die Generierung von Vorlesungsunterlagen mit LectureDoc2 im DHBW Corporate Design.
    :id: ld2-dhbw-cheat-sheet
    :slide-dimensions: 2560x1440

.. |date| date::

.. role:: dhbw-red
.. role:: shiny-red
.. role:: shiny-green
.. role:: the-green
.. role:: the-blue
.. role:: dark-red
.. role:: black

.. role:: minor


.. class:: cheat-sheet-8-columns 

LectureDoc2 Cheat Sheet for Slides using the DHBW Corporate Design 
-------------------------------------------------------------------------------

.. container:: cheat-sheet-block

   .. rubric:: Information
   
   :Author: Michael Eichberg
   :Version: |date|


.. CHANGING THE OVERALL SLIDE LAYOUT   
   
.. container:: cheat-sheet-block

   .. rubric:: Vertical Titles

   Add the class ``vertical-title``. This will change the layout of the slide to a column-based layout. To get back to a row based layout add a container with the class ``width-100``.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. class:: vertical-title

      <Slide Title>
      ----------------

      .. container:: width-100

         ...



.. container:: cheat-sheet-block

   .. rubric:: Slide Tweaks 
      
   .. rubric:: Slide without Title
   
   For a slide without a title set the title to a single space character using a backslash and an explicit space :code:`\␣` and assign the class ``no-title`` to the slide.

   .. rubric:: Smaller Slide Titles

   Add the class `smaller-slide-title`` to the slide.

   .. rubric:: Centered Content on Slide
   
   Use the class ``center-child-elements``.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard
   
      .. class:: center-child-elements 
                 no-title

      \  
      ___

         Text

.. container:: cheat-sheet-block

   .. rubric:: Sections and Subsections

   Create a slide that marks the beginning of a new section or subsection by adding the class ``new-section`` or ``new-subsection`` to the slide.

.. container:: cheat-sheet-block

   .. rubric:: Exercises and Solutions

   Create a slide with exercises by adding the class ``integrated-exercise`` to the slide. Solutions can be added by using the custom directive ``protected-exercise-solution`` 

   .. rubric:: Example (Solution in supplemental information)

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. admonition:: Solution
         :class: supplemental
                 exercise-solution

   .. rubric:: Example (Solution requires password.)

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. class:: integrated-exercise 

      Exercise: XYZ
      --------------

      Calculate uvw...

      .. protected-exercise-solution:: Solution

         The result is ...


.. container:: cheat-sheet-block
   
   .. rubric:: Table of Contents

   A navigable table of contents (e.g. of the section slides) can be manually created by 
   referencing the titles. 

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      Table of Contents
      ------------------

      - `Section 1 Title`_
      - `Subsection 1.1 Title`_



.. container:: cheat-sheet-block
   
   .. rubric:: Footnotes

   ``.. [#]`` and ``[#]_`` create footnotes.

   .. code:: rst
      :class: smaller copy-to-clipboard

      Test\ [#]_
      -----------------

      ...

      .. [#] `test.org`


.. container:: cheat-sheet-block

   .. rubric:: Explicit Footers

   Use a container with the class ``footer-left`` or ``footer-right``.





.. container:: cheat-sheet-block

   .. rubric:: References 

   Use standard rst references.

   .. rubric:: Example   

   .. code:: rst
      :class: smaller copy-to-clipboard

      ...
      Like described in [Eic24]_ ...
      ...

      References
      -----------
      
      .. [Eic24] LectureDoc2; 2024 

.. container:: cheat-sheet-block

   .. rubric:: Copy to Clipboard

   To make it easily possible to copy code the clipboard add the class ``copy-to-clipboard`` to the code block.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. code:: java
         :class: copy-to-clipboard

         public static void main(...)


.. container:: cheat-sheet-block

   .. rubric:: Fade-out Content

   Use the class ``faded-to-white`` for the container with the content that should be faded out.
   


.. container:: cheat-sheet-block

   .. rubric:: Boxes with Supplemental Information on the Slide

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. admonition:: TBD
         :class: note 

         Some text in a box.

     

.. container:: cheat-sheet-block

   .. rubric:: Supplemental Information

   Add a container with the class ``supplemental`` to add respective information. How this information is rendered depends on the chosen view.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. container:: supplemental

         Text

.. container:: cheat-sheet-block

   .. rubric:: Text Alignment

   Text alignment can be controlled with: ``text-align-left``, ``text-align-center`` and ``text-align-right``



.. container:: cheat-sheet-block

   .. rubric:: Images

   Adding a drop-shadow and rounded corners: ``picture``.



.. container:: cheat-sheet-block

   .. rubric:: Tables

   The layout can be adapted using:
   ``compact``, ``compact-cells``, ``no-table-borders``, ``no-inner-borders``, ``no-column-borders``, ``fake-header-row`` and ``fake-header-column``.


   .. rubric:: Animation
   
   ``incremental`` (and ``wobble``).

   ``highlight-line-on-hover`` (always usable) or ``highlight-on-hover`` (explicit column or row headers are not supported)



.. container:: cheat-sheet-block

   .. rubric:: Lists

   .. class:: list-with-explanations

   -  Use ``li-margin-top-0-75em`` to have more space between the list items.
   - ``list-with-explanations`` renders text paragraphs of list items less pronounced.
  
     (As shown here.)
   - Use ``impressive`` to make the list more impressive:
    
   .. class:: impressive

   -  Add ``negative-list`` to use "❗️" for bullet points.

   -  Add ``positive-list`` to use "✓" for bullet points.


   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      - Point 1
   
      .. class:: negative-list list-with-explanations
      - Point 2
        Some on-slide explanation. 

      .. class:: positive-list
      - Point 3
      - Point 4


.. container:: cheat-sheet-block

   .. rubric:: Decorations

   ``line-above`` draws a horizontal lines.

   ``box-shadow`` adds a shadow.

   ``rounded-corners`` the corners will be rounded.

   .. rubric:: Example
   
   .. code:: rst
      :class: smaller copy-to-clipboard

      .. container:: margin-top-1em 
                     line-above
                     padding-top-1em
                     box-shadow

         Text

.. container:: cheat-sheet-block

   .. rubric:: Font Styling

   **"rem" based relative sizes**: ``xxl``, ``huge``, ``large``, ``small``, ``footnotesize``, ``scriptsize``, ``tiny``, ``x-tiny``, ``xx-tiny``

   **"em" based relative sizes**: ``larger``, ``smaller``, ``much-smaller``

   **Font weight**: ``bold``, ``light``, ``thin``

   **Font family**: ``monospaced``, ``serif``

   **Font style**: ``italic``

.. ANIMATIONS

.. container:: cheat-sheet-block

   .. rubric:: Slide Transitions

   Available slide transitions:
   ``transition-move-left``, ``transition-scale``, ``transition-fade``, ``transition-move-to-top``
   
   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. class:: transition-move-left

      <Slide Title>
      ----------------

.. container:: cheat-sheet-block
   
   .. rubric:: Revealing Slide Content
   
   All elements with the class ``incremental`` are revealed incrementally.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. class:: incremental

      - Item 1 - Part 1 
        :incremental:`Item 1 - Part 2`
      - Item 2 

        - Item 2.1
        
          .. class:: incremental
        - Item 2.2


.. COMPLEX LAYOUTS


.. container:: cheat-sheet-block

   .. rubric:: Column-based Layouts

   We support 2- (``two-columns``) and 3-column (``three-columns``) layouts based on nested rst ``container``\ s for each column.

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      .. container:: two-columns 

         .. container:: column 
      
            Column 1
      
         .. container:: column 
      
            Column 2

   To enable unbalanced column widths add the class ``no-default-width`` to the root container. To remove the separator between two columns use the class ``no-separator`` on the left column.
   



.. container:: cheat-sheet-block

   .. rubric:: Stacked Layouts

   Stacked layouts are based on nested rst ``container``\ s for each layer. In general. each layer - except the first one - needs to have the class ``incremental``. If a new layer should be transparent; e.g., to incrementally build up an image, add the class ``overlay`` to the layer. :dhbw-red:`(Currently, up to 10 layers are supported (CSS Limitation).)`

   .. rubric:: Images in Stacked Layouts

   To avoid that a parent element of a floating element is collapsed, add the class ``clearfix`` to the parent element. This is in particular necessary when you use a stacked layout where an element of a layer is a floating image. 

   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard 

      .. container:: stack

        .. container:: layer clearfix
        
           .. image:: <p1.svg>
              :align: left

        .. container:: layer overlay
        
           .. image:: <p2.svg>
              :align: left

         .. container:: layer 
                        incremental

            Important!




.. CHANGING INDIVIDUAL PROPERTIES OF ELEMENTS

.. container:: cheat-sheet-block

   .. rubric:: Semantic-based Text Markup

   ``minor``: for less important text.
   ``obsolete``: for obsolete statements.
   ``ger``: to markup German Words.
   ``eng``: to markup English words.
   ``ger-quote``: Uses German quotation marks.


.. container:: cheat-sheet-block

   .. rubric:: Box sizes

   Use ``width-100``\ % and ``width-75``\ % to control the width of a container.

.. container:: cheat-sheet-block

   .. rubric:: Colors (``roles``)
   
   .. rubric:: Font Colors

   :minor:`DHBW Colors:` ``dhbw-red``, ``dhbw-gray``, ``dhbw-light-gray``
   
   :minor:`DHBW Compatible Colors:` ``the-blue``, ``the-green``, ``the-orange``

   :minor:`Other:` ``black``, ``shiny-green``, ``shiny-red``, ``dark-red``

   .. rubric:: Background Colors

   :minor:`DHBW Colors:` ``dhbw-red-background``, ``dhbw-gray-background``, ``dhbw-light-gray-background``
   
   :minor:`DHBW Compatible Colors:` ``the-blue-background``, ``the-green-background``, ``the-yellow-background``

   :minor:`Other:` ``light-green-background``, ``white-background``


   .. rubric:: Example

   .. code:: rst
      :class: smaller copy-to-clipboard

      :dhbw-red:`Red Text.`
       
   



.. container:: cheat-sheet-block
   
   .. rubric:: Controlling Whitespace

   Adding space around an element (in particular images): ``border-transparent-1em``
  
   .. rubric:: Fine-grained Control (Try to avoid!)

   ``margin-none``, ``margin-0-5em``, ``margin-1em``, ``margin-top-1em``, ``margin-top-2em``, ``margin-bottom-1em``, ``margin-bottom-2em``, ``margin-right-1em``, ``margin-left-1em``, ``padding-none``, ``padding-0-5em``, ``padding-1em``, ``padding-top-1em``, ``padding-top-2em``


.. container:: cheat-sheet-block

   .. rubric:: Meta-Information

   LectureDoc meta information:

   ``id`` A unique identifier for the slide set. Required to store the current state of the presentation.

   ``slide-dimensions`` The dimensions of the slides (default: "1920x1200").
   
   ``first-slide`` The first slide that is shown when the presentation is started (e.g., <Slide Number> or "last-viewed").

   .. rubric:: Example
   
   .. code:: rst
      :class: smaller copy-to-clipboard
      
      .. meta:: 
        :id: <unique id>
        :slide-dimensions: 2560x1440
        :first-slide: last-viewed


.. container:: cheat-sheet-block

   .. rubric:: Cheat Sheets with LD\ :sup:`2`

   A cheat-sheet is a slide with the class ``cheat-sheet-8-columns``. 

   .. rubric:: Template

   .. code:: rst
      :class: much-smaller copy-to-clipboard

      .. class:: cheat-sheet-8-columns

         <Title>
         -------

         .. container:: cheat-sheet-block

            .. rubric:: <TOPIC>
   
            .. rubric:: <SUB-TOPIC>

         .. container:: cheat-sheet-block

            .. rubric:: <TOPIC>
   
            .. rubric:: <SUB-TOPIC>



.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: much-smaller copy-to-clipboard

      .. |date| date::
      .. |at| unicode:: 0x40

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: ger-quote
      .. role:: minor
      .. role:: obsolete
      .. role:: dhbw-red
      .. role:: dhbw-gray
      .. role:: dhbw-light-gray
      .. role:: the-blue
      .. role:: the-green
      .. role:: the-orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: black
      .. role:: dark-red

      .. role:: raw-html(raw)
         :format: html

.. container:: cheat-sheet-block

   .. rubric:: Links

   .. container:: smaller

      `DocUtils (rst reStructuredText) <https://docutils.sourceforge.io/docs/index.html>`_

      `Example Slide Sets <http://www.michael-eichberg.de/teaching.html>`_ 
      


