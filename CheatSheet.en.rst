.. meta::
    :author: Michael Eichberg
    :keywords: LectureDoc2, "Cheat Sheet"
    :description lang=de: Cheat Sheet for LectureDoc2/rst2ld.
    :id: ld2-cheat-sheet
    :slide-dimensions: 2560x1440

.. include:: ../docutils.shared.defs



.. SETTING THE CLASS TO CHEAT-SHEET CHANGES THE OVERALL SLIDE LAYOUT

.. class:: cheat-sheet

LectureDoc2 Cheat Sheet
-------------------------------------------------------------

.. container:: cheat-sheet-block

   .. rubric:: Information

   :Author: Michael Eichberg
   :Version: Work in Progress



.. container:: cheat-sheet-block

   .. rubric:: Admonitions

   Standard reStructuredText admonitions: ``attention``, ``caution``, ``danger``, ``error``, ``hint``, ``important``, ``note``, ``tip`` and ``warning``

   LectureDoc2 specific admonitions:
   ``background``, ``definition``, ``proof``, ``theorem``, ``lemma``, ``conclusion``, ``observation``, ``remark``, ``summary``, ``legend``, ``repetition``, ``question``, ``answer``, ``remember``, ``deprecated``, ``assessment``, and ``example``.

   .. popover:: Examples

      .. grid::

         .. cell:: width-25

            .. admonition:: Generic Admonition with Custom Title

               This is a generic admonition.

            .. attention::
               This is an attention admonition.

            .. caution::
               This is a caution admonition.

            .. danger::
               This is a danger admonition.

            .. error::
               This is an error admonition.

            .. hint::
               This is a hint admonition.

            .. important::
               This is an important admonition.

            .. tip::
               This is a tip admonition.

            .. warning::
               This is a warning admonition.

         .. cell:: width-25

            .. background::
               This is a background admonition.

            .. definition::

               This is a definition admonition.

            .. definition:: A Definition with a very long title that spans multiple lines

               This is a definition admonition.

            .. proof::
               This is a proof admonition.

            .. theorem::
               This is a theorem admonition.

            .. lemma::
               This is a lemma admonition.

            .. conclusion::
               This is a conclusion admonition.

            .. observation::
               This is an observation admonition.

         .. cell:: width-25

            .. remark::

               This is a remark admonition.

            .. example::

               This is an example admonition.

            .. example:: With a title

               This is an example admonition.

            .. summary::

               This is a summary admonition.

            .. legend::
               This is a legend admonition.

            .. repetition::
               This is a repetition admonition.

            .. question::
               This is a question admonition.

            .. answer::
               This is an answer admonition.

            .. remember::
               This is a remember admonition.

         .. cell:: width-25

            .. deprecated::
               This is a deprecated admonition.

            .. assessment::
               This is an assessment admonition.

            .. rubric:: Support for Notes

            Text above the note.

            .. note::
                :class: width-25

                This is a note.

            Notes are floated to the right w.r.t. the content that follows the note. Often, notes are explicitly sized using the ``:class: width-<Percentage>`` option.

            .. tip::
               :class: clear-float

               This tip is shown below the **note** because the class ``clear-float`` is used to *clear the float* of the note.

               .. example::

                  .. code:: rst
                     :class: copy-to-clipboard
                     :number-lines:

                     .. note::
                        :class: width-40

                        This is a note.

                     Text that is left of the note.

                     .. tip::
                        :class: clear-float

                        This tip is shown ...

   .. popover:: Code

      .. rubric:: Most basic Example

      .. code:: rst
         :class: copy-to-clipboard

         .. definition:: A Definition with a very long title that spans multiple lines

               This is a definition admonition.


.. container:: cheat-sheet-block

   .. rubric:: SVGs

   SVGs can easily be embedded directly in RST documents. Direct embedding has the advantage that animation is then possible.

   .. popover:: Sizing of SVGs

        **External SVGs**

        *Usage: slide view and document view*

        In general, SVGs should be designed with the slide view in mind. They will automatically be scaled in the document view based on the font-ratio between the base font size used in the slide view and the base font size used in the document view.

        *Usage: document view only*

        SVGs shown only in the document view (e.g. solutions to exercises) should be designed with the document view in mind and hence should use the base font size of the document view as the foundation.

        **Embedded SVGs**

        They should be designed independent of any specific size and only use relative sizing. This ensures that they look beautiful in all contexts.

        :peripheral:`(See the respective example for more details.)`

   .. popover:: Basic Example

        .. example::

            .. raw:: html
                :class: center-content

                <div style="width: 5ch; height: 5ch;">
                <svg    viewBox="0 0 5 5"
                        font-size="2"
                        version="1.1"
                        xmlns="http://www.w3.org/2000/svg">
                    <rect x="0.5" y="0.5" width="4" height="4" fill="darkblue"/>
                    <text x="0.75" y="3" fill="white">SVG</text>
                </svg>
                </div>

            .. code:: rst
                :number-lines:
                :class: copy-to-clipboard

                .. raw:: html

                    <div style="width: 5ch; height: 5ch;">
                    <svg    viewBox="0 0 5 5"
                            font-size="2"
                            version="1.1"
                            xmlns="http://www.w3.org/2000/svg">
                        <rect x="0.5" y="0.5" width="4" height="4" fill="darkblue"/>
                        <text x="0.75" y="3" fill="white">SVG</text>
                    </svg>
                    </div>


   .. popover:: Markers and Styles

        **Embedded SVGs Only**

        .. important::

            A single SVG in an rst source file, will be found at least three times in the HTML: In the document view, the slide view, and the lighttable view.

        .. attention::

            :IDs: If an SVG uses ``id``\ s, they are no longer unique which may cause rendering issues (in particular with Firefox). Therefore SVG elements with ids (typically markers) need to be defined using shared definitions.

            :Styles: Note that all styles defined in an SVG are global and affect all elements. Therefore, it is recommended to define them once using the ``:svg-defs:`` meta information tag.

        Shared definitions in LD-rst documents:

        .. example::

            .. code:: rst
                :number-lines:
                :class: copy-to-clipboard

                .. meta::
                    <other meta information>
                    :svg-style:
                        g.graph {
                            circle{
                                fill: var(--current-fg-color);
                                stroke-width: 0.2;

                                &.red { fill: red;}
                                &.green { fill: green; }
                                &.blue { fill: blue; }
                                &.start-node {
                                    fill: none;
                                    stroke: red;
                                    stroke-width: 0.3;
                                }
                            }
                        }
                    :svg-defs:
                        <marker
                            id="arrow"
                            viewBox="0 0 2 2"
                            refX="1.8"
                            refY="1"
                            markerUnits="strokeWidth"
                            markerWidth="6"
                            markerHeight="6"
                            orient="auto-start-reverse">
                            <path class="arrow-head" d="M 0 0 L 2 1 L 0 2 z" fill="context-stroke" />
                        </marker>



   .. popover:: Font-size dependent SVGs

        LectureDoc generally distinguishes between the slide view and the document view. Both views represent the content in similar ways, but the slide view is optimized for presentation and generally uses a much larger font size (e.g., 48px) while the document view uses a smaller font size (e.g., 14px or 16px). Hence, it is recommended to draw an SVG uusing a font-size of 1 (no unit!) and to put the SVG in a fixed sized container where the size of the container depends on the font-size.

        .. example::

            .. grid::

                .. cell:: width-20

                    .. raw:: html
                        :class: center-content

                        <div style="width: 5ch; height: 5ch;">
                        <svg    viewBox="0 0 5 5"
                                font-size="1"
                                version="1.1"
                                xmlns="http://www.w3.org/2000/svg">
                            <rect x="0.5" y="0.5" width="4" height="4" fill="darkblue"/>
                            <text x="1.75" y="3" fill="white">SVG</text>
                        </svg>
                        </div>

                .. cell::  width-80

                    .. code:: rst
                        :number-lines:
                        :class: copy-to-clipboard

                        .. raw:: html

                            <div style="width: 5ch; height: 5ch;">
                            <svg    viewBox="0 0 5 5"
                                    font-size="1"
                                    version="1.1"
                                    xmlns="http://www.w3.org/2000/svg">
                                <rect x="0.5" y="0.5" width="4" height="4" fill="darkblue"/>
                                <text x="1.75" y="3" fill="white">SVG</text>
                            </svg>
                            </div>


.. container:: cheat-sheet-block

    .. rubric:: Code Blocks

    Use the standard ``.. code::`` directive to create a code block.

    .. popover:: Numbering Lines

        LD2 extends the standard reStructuredText :rst:`code` directive to ensure proper alginment of subsequent line numbers if a listing is split up in multiple code blocks or if multiple listings are shown on a single slide.

        .. grid::

            .. cell::

                .. code:: java
                    :line-number-digits: 2
                    :class: head no-margin

                    void main() {
                        // 1. Create and initialize a heap
                        var heap = new Heap<String>(String.class, 5);
                        heap.insertAll("dies", "ist", "ein", "test");


                .. code:: java
                    :number-lines: 5
                    :class: tail incremental-code

                        // 2. Remove elements and print them
                        while (heap.nonEmpty()) {
                            String s = heap.remove();
                            IO.println(s);
                        }
                    }

                **The classes:** ``head``, ``tail``, and ``snippet``

                To controll the rendering of the line numbers, a code block that represents only the start of a code should get the class ``head`` and a code block that represents only the end of a code should get the class ``tail``, and a code block that is neither the start nor the end of a code block should get the class ``snippet``

            .. cell::

                .. code:: rst
                    :number-lines:
                    :class: copy-to-clipboard

                    .. code:: java
                        :line-number-digits: 2
                        :class: head no-margin

                        void main() {
                            // 1. Create and initialize a heap
                            var heap = new Heap<String>(String.class, 5);
                            heap.insertAll("dies", "ist", "ein", "test");


                    .. code:: pascal
                        :number-lines: 5
                        :class: tail incremental-code

                            // 2. Remove elements and print them
                            while (heap.nonEmpty()) {
                                String s = heap.remove();
                                IO.println(s);
                            }
                        }

    .. popover:: Copy to Clipboard

        Add ``copy-to-clipboard`` to a code block to enable copying code to the clipboard.

        .. rubric:: Example

        .. code:: rst
           :class: copy-to-clipboard

            .. code:: java
                :class: copy-to-clipboard

                public static void main(...)


.. container:: cheat-sheet-block

   .. rubric:: Supplemental Information

   Use the :rst:`supplemental` directive for information that should not be directly shown on the slide, but should be integrated in the document. If the supplemental information is considered regular information in the document view - i. e., it should not be distinguishable from the main content - use the optional option :rst:`:embed-in-document-flow:`

   .. popover:: Example

        .. example::

            .. grid::

                .. cell:: width-50

                    .. code:: rst
                        :class: copy-to-clipboard

                        .. supplemental::
                            :embed-in-document-flow:

                            <Supplemental Information>


                .. cell:: width-50

                        .. supplemental::
                            :embed-in-document-flow:

                            This is supplemental information.





.. container:: cheat-sheet-block

   .. rubric:: Vertical Titles TODO

   Add the class ``vertical-title`` to rotate the title and to change the layout of the slide to a column-based layout. To get back to a row based layout add a container with the class ``width-100``.

   .. popover:: Examples

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

   .. rubric:: Vertically Centered Content

   Use the class ``center-content``.

   .. popover:: Examples

      .. code:: rst
         :class: copy-to-clipboard

         .. class:: center-content
                  no-title

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

   .. rubric:: Fade-out Content

   Add the class ``fade-out`` to a container to whiten the content.







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

   ``red``, ``gray``, ``light-gray``, ``blue``, ``green``,  ``black``, ``white``, ``shiny-green``, ``shiny-red``

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
