.. meta::
    :author: Michael Eichberg
    :keywords: LectureDoc2, "Cheat Sheet"
    :description lang=de: Cheat Sheet for LectureDoc2/rst2ld.
    :id: ld2-dhbw-cheat-sheet
    :slide-dimensions: 2560x1440

.. role:: red


.. THE FOLLOWING CHANGES THE OVERALL SLIDE LAYOUT   

.. class:: cheat-sheet

LectureDoc2 Cheat Sheet
-------------------------------------------------------------

.. container:: cheat-sheet-block

   .. rubric:: Information
   
   :Author: Michael Eichberg
   :Version: August 2024

   
.. container:: cheat-sheet-block

   .. rubric:: Vertical Titles

   Add the class ``vertical-title`` to rotate the title and to change the layout of the slide to a column-based layout. To get back to a row based layout add a container with the class ``width-100``.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      .. class:: vertical-title

      <Slide Title>
      ----------------

      .. container:: width-100

         <Row based content layout.>



.. container:: cheat-sheet-block

   .. rubric:: Slide Tweaks 
      
   .. rubric:: Slide without Title
   
   To hide the title of a slide assign the class ``no-title``.

   .. rubric:: Smaller Slide Titles

   Use the class ``smaller-slide-title``.

   .. rubric:: Vertically Centered Content  
   
   Use the class ``center-child-elements``.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard
   
      .. class:: center-child-elements 
                 no-title
                 smaller-slide-title

      Hidden on the slide! 
      --------------------

      <Slide Content>

.. container:: cheat-sheet-block

   .. rubric:: Sections and Subsections

   Create a slide that marks the beginning of a new section or subsection by adding the class ``new-section`` or ``new-subsection`` to the slide.

.. container:: cheat-sheet-block

   .. rubric:: Exercises and Solutions

   Associate the class ``exercises`` with a slide to indicate that the slide contains an exercise.

   Use the directive ``.. exercise::`` to add an exercise. To add a solution use the custom directive ``.. solution::`` inside of an exercise block and specify the password (optional) using the attribute ``:pwd:``.
   
   .. rubric:: Example (Solution in supplemental information)

   .. code:: rst
      :class: copy-to-clipboard

      .. exercise:: <Title>

         <Description of the exercise.>

         .. solution:: <Title>
            :pwd: 1234 

            <Solution>

   You can configure a master-password using meta information:

   .. code:: rst

      .. meta::
         :master-password: <Master-password>

.. container:: cheat-sheet-block
   
   .. rubric:: Table of Contents

   A navigable table of contents can be created using standard ``rst`` techniques.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      Table of Contents
      ------------------

      - `Section 1 Title`_
      - `Subsection 1.1 Title`_



.. container:: cheat-sheet-block
   
   .. rubric:: Footnotes

   ``[#]_`` and ``.. [#]`` create footnotes.

   .. code:: rst
      :class: copy-to-clipboard

      Test\ [#]_
      -----------------

      .. [#] `test.org`


.. container:: cheat-sheet-block

   .. rubric:: Explicit Footers

   A container with the class ``footer-left``, ``footer-right`` or ``block-footer``.



.. container:: cheat-sheet-block

   .. rubric:: References 

   Use standard rst references.

   .. rubric:: Example   

   .. code:: rst
      :class: copy-to-clipboard

      ...
      Like described in [Eic24]_ ...
      ...

      References
      -----------
      
      .. [Eic24] LectureDoc2; 2024 



.. container:: cheat-sheet-block

   .. rubric:: Copy to Clipboard

   Add ``copy-to-clipboard`` to a code block to enable copying code to the clipboard.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      .. code:: java
         :class: copy-to-clipboard

         public static void main(...)


.. container:: cheat-sheet-block

   .. rubric:: Fade-out Content

   Add the class ``fade-out`` to a container to whiten the content.
   

     

.. container:: cheat-sheet-block

   .. rubric:: Supplemental Information

   Use the directive ``supplemental`` for respective information. 

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      .. supplemental:: 

         <Text>

.. container:: cheat-sheet-block

   .. rubric:: Text Alignment

   Control text alignment: ``text-align-[left|center|right]``



.. container:: cheat-sheet-block

   .. rubric:: Images

   Adding a drop-shadow and rounded corners: ``picture``.



.. container:: cheat-sheet-block

   .. rubric:: Tables

   The layout can be adapted using:
   ``compact``, ``compact-cells``, ``no-table-borders``, ``no-inner-borders``, ``no-column-borders``, ``fake-header[-2nd]-row`` and ``fake-header[-2nd]-column``.


   .. rubric:: Animation
   
   ``incremental`` (and ``wobble``).

   ``highlight-line-on-hover`` (always usable), ``highlight-on-hover`` (explicit column or row headers are not supported) or ``highlight-identical-cells``



.. container:: cheat-sheet-block

   .. rubric:: Lists

   .. class:: list-with-explanations

   - ``list-with-explanations`` renders text paragraphs of list items less pronounced.
  
     (As shown here.)
   - Use ``impressive`` to make the list more impressive:
    
   .. class:: impressive

   -  Add ``negative-list`` to use "❗️" for bullet points.

   -  Add ``positive-list`` to use "✓" for bullet points.


   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      - Point 1
   
      .. class:: negative-list list-with-explanations
      - Point 2
        Some on-slide explanation. 

      .. class:: positive-list
      - Point 3



.. container:: cheat-sheet-block

   .. rubric:: Decorations

   ``line-above`` draws a horizontal lines.

   ``box-shadow`` adds a shadow.

   ``rounded-corners`` the corners will be rounded.

   .. rubric:: Example
   
   .. code:: rst
      :class: copy-to-clipboard

      .. container:: margin-top-1em 
                     line-above
                     padding-top-1em
                     box-shadow

         Text

.. container:: cheat-sheet-block

   .. rubric:: Font Styling

   **"rem" based relative sizes**: ``xxl``, ``huge``, ``large``, ``small``, ``footnotesize``, ``scriptsize``, ``tiny``, ``x-tiny``, ``xx-tiny``

   **"em" based relative sizes**: ``larger``, ``smaller``, ``far-smaller``

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
      :class: copy-to-clipboard

      .. class:: transition-move-left

      <Slide Title>
      ----------------

.. container:: cheat-sheet-block
   
   .. rubric:: Revealing Slide Content
   
   All elements with the class ``incremental`` are revealed incrementally.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      .. class:: incremental

      - Item 1 - Part 1 
        :incremental:`Item 1 - Part 2`
      - Item 2 



.. COMPLEX LAYOUTS


.. container:: cheat-sheet-block

   .. rubric:: Column-based Layouts

   Use ``two-columns`` and ``three-columns`` for respective layouts.

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      .. container:: two-columns 

         .. container:: column no-separator
      
            <Column 1>
      
         .. container:: column 
      
            <Column 2>

   Add ``no-default-width`` to the root container for content based column widths. Use class ``no-separator`` on the left column to remove the separator.
   



.. container:: cheat-sheet-block

   .. rubric:: Stacked Layouts

   Stacked layouts are based on nested layers. Each layer - except of the first one - needs to have the class ``incremental`` and/or the class ``overlay`` for transparent layers. :red:`(Up to 10 layers are supported.)` To turn off the numbering of opaque layers use ``.no-number``.

   .. rubric:: Images in Stacked Layouts

   To avoid that a parent element of a floating element is collapsed add the class ``clearfix`` to the parent element; i. e., when a layer just contains a floating image. 

   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard 

      .. deck::

        .. card:: clearfix
        
           .. image:: <p1.svg>
              :align: left

        .. card:: overlay
        
           .. image:: <p2.svg>

         .. card:: warning

            <Content>




.. CHANGING INDIVIDUAL PROPERTIES OF ELEMENTS

.. container:: cheat-sheet-block

   .. rubric:: Semantic-based Text Markup

   ``peripheral``: for less important text.
   ``obsolete``: for obsolete statements.
   ``ger``: to markup German Words.
   ``eng``: to markup English words.


.. container:: cheat-sheet-block

   .. rubric:: Box sizes

   Use ``width-100``\ % and ``width-75``\ % to control the width of a container.

.. container:: cheat-sheet-block

   .. rubric:: Colors (``roles``)
   
   .. rubric:: Font Colors

   ``red``, ``gray``, ``light-gray``, ``blue``, ``green``, ``orange``, ``black``, ``shiny-green``, ``shiny-red``, ``dark-red``

   .. rubric:: Background Colors

   ``red-background``, ``dhbw-gray-background``, ``dhbw-light-gray-background``, ``white-background``, ``blue-background``, ``light-green-background``, ``green-background``, ``yellow-background``


   .. rubric:: Example

   .. code:: rst
      :class: copy-to-clipboard

      :dhbw-red:`Red Text.`
       
   



.. container:: cheat-sheet-block
   
   .. rubric:: Fine-grained Control (Try to avoid!)

   ``margin-none``, ``margin-0-5em``, ``margin-1em``, ``margin-top-1em``, ``margin-top-2em``, ``margin-bottom-1em``, ``margin-bottom-2em``, ``margin-right-1em``, ``margin-left-1em``, ``padding-none``, ``padding-0-5em``, ``padding-1em``, ``padding-top-1em``, ``padding-top-2em``



.. container:: cheat-sheet-block

   .. rubric:: Hiding slides (⚠️ rst2ld only)

   Use ``hide-slide`` to exempt it from slide generation.

   .. rubric:: Example
   
   .. code:: rst
      :class: copy-to-clipboard
      
      .. class:: hide-slide
      
      <Hidden Slide >
      -----------------



.. container:: cheat-sheet-block

   .. rubric:: Configuration

   LectureDoc meta information:

   ``id`` The unique identifier for the slide set. Required to store the current state of the presentation.

   ``slide-dimensions`` the slides dimension (default: "1920x1200").
   
   ``first-slide`` Determines the first slide that is shown (e.g., <Slide Number> or "last-viewed").

   .. rubric:: Example
   
   .. code:: rst
      :class: copy-to-clipboard
      
      .. meta:: 
        :id: <unique id>
        :slide-dimensions: 2560x1440
        :first-slide: last-viewed


.. container:: cheat-sheet-block

   .. rubric:: Cheat Sheets with LD\ :sup:`2`

   A cheat-sheet is a slide with the class ``cheat-sheet-8-columns``. 

   .. rubric:: Template

   .. code:: rst
      :class: copy-to-clipboard

      .. class:: cheat-sheet-8-columns

         <Title>
         -------

         .. container:: cheat-sheet-block

            .. rubric:: <TOPIC>
   
            .. rubric:: <SUB-TOPIC>




.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html

.. container:: cheat-sheet-block

   .. rubric:: Links

   .. container:: smaller

      `DocUtils (rst reStructuredText) <https://docutils.sourceforge.io/docs/index.html>`_

      `Example Slide Sets <http://www.michael-eichberg.de/teaching.html>`_ 
      











.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html


.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html



.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html



.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html

.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html
         
.. container:: cheat-sheet-block

   .. rubric:: Useful Role and Substitution Definitions

   .. rubric:: Template   

   .. code:: rst 
      :class: copy-to-clipboard

      .. role:: incremental   
      .. role:: eng
      .. role:: ger
      .. role:: peripheral
      .. role:: obsolete
      .. role:: red
      .. role:: gray
      .. role:: light-gray
      .. role:: blue
      .. role:: green
      .. role:: orange
      .. role:: shiny-green
      .. role:: shiny-red 
      .. role:: dark-red
      .. role:: black

      .. role:: raw-html(raw)
         :format: html