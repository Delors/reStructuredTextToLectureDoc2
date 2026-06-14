.. meta::
    :author: Michael Eichberg
    :keywords: LectureDoc2, "Cheat Sheet", Directives
    :description lang=de: Cheat Sheet for LectureDoc2/rst2ld Custom Directives.
    :id: ld2-directives-cheat-sheet
    :slide-dimensions: 2560x1440

.. include:: ../docutils.shared.defs



.. class:: cheat-sheet

LectureDoc2 Custom Directives Cheat Sheet
------------------------------------------

.. container:: cheat-sheet-block

    .. rubric:: Layout Directives

    .. rubric:: Grid & Cell

    ``.. grid:: <classes>``

    ``.. cell:: <classes>``

    .. list-table::
        :class: compact

        * - :info:`:align:`
          - ``auto`` (default), ``center``, ``start``, ``end``
        * - :info:`:theme:`
          - Any theme name (emitted as ``data-theme``)

    .. code:: rst
        :class: copy-to-clipboard

        .. grid::

            .. cell:: width-50
                :align: center
                :theme: muted

                Cell content.

            .. cell:: width-50

                Another cell.


    .. rubric:: Deck & Card

    ``.. deck:: <classes>``

    ``.. card:: <classes>``

    .. list-table::
        :class: compact

        * - :info:`:theme:` *(deck)*
          - Any theme name (emitted as ``data-theme`` on ``<ld-deck>``)
        * - :info:`:theme:` *(card)*
          - Any theme name (emitted as ``data-theme`` on ``<ld-card>``)
        * - :info:`:not-incremental:` *(card)*
          - Flag; prevents the card from being shown incrementally

    .. code:: rst
        :class: copy-to-clipboard

        .. deck::
            :theme: dark

            .. card::
                :theme: light

                First card content.

            .. card::
                :not-incremental:

                This card is not incremental.


    .. rubric:: Compound

    ``.. compound::`` — Standard docutils directive, extended with:

    .. list-table::
        :class: compact

        * - :info:`:theme:`
          - Any theme name (emitted as ``data-theme``)

    .. code:: rst
        :class: copy-to-clipboard

        .. compound::
            :theme: muted

            Content inside a compound container.


.. container:: cheat-sheet-block

    .. rubric:: Information Directives

    .. rubric:: Global Information

    ``.. global-information:: <title>``

    .. list-table::
        :class: compact

        * - :info:`:formatted-title:`
          - Inline markup supported (e.g. ``**bold**``)
        * - :info:`:symbol:`
          - Single character symbol (e.g. ``λ``)
        * - :info:`:type:`
          - ``cheat-sheet`` (default) or ``slide``
        * - :info:`:embed:`
          - Flag; embed in document flow
        * - :info:`:class:`
          - CSS class(es)
        * - :info:`:name:`
          - Reference name

    .. code:: rst
        :class: copy-to-clipboard

        .. global-information:: Functional Programming
            :symbol: λ
            :type: cheat-sheet
            :embed:

            Background information.


    .. rubric:: Supplemental

    ``.. supplemental:: <classes>``

    .. list-table::
        :class: compact

        * - :info:`:embed-in-document-flow:`
          - Flag; makes content indistinguishable from main content in document view

    .. code:: rst
        :class: copy-to-clipboard

        .. supplemental::
            :embed-in-document-flow:

            This appears inline in the document.


    .. rubric:: Presenter Note

    ``.. presenter-note:: <classes>``

    .. list-table::
        :class: compact

        * - :info:`:name:`
          - Reference name

    .. code:: rst
        :class: copy-to-clipboard

        .. presenter-note::

            Notes for the presenter.


    .. rubric:: Module

    ``.. module:: <name>``

    .. list-table::
        :class: compact

        * - :info:`:class:`
          - CSS class(es)
        * - :info:`:scope:`
          - ``slide``, ``document``, or ``all`` (default)

    .. code:: rst
        :class: copy-to-clipboard

        .. module:: My Module
            :scope: slide

            Module content.


    .. rubric:: Source

    ``.. source:: <filename>``

    .. list-table::
        :class: compact

        * - :info:`:prefix:`
          - Text to prepend to the resolved path
        * - :info:`:suffix:`
          - Text to append to the resolved path
        * - :info:`:path:`
          - ``relative`` (default) or ``absolute``

    .. code:: rst
        :class: copy-to-clipboard

        .. source:: my_file.rst
            :prefix: https://example.com/
            :path: absolute


    .. rubric:: Include SVG

    ``.. include-svg:: <filename>``

    .. list-table::
        :class: compact

        * - :option:`:width:`
          - Required; CSS width value (e.g. ``500px``, ``100%``)
        * - :option:`:height:`
          - Required; CSS height value (e.g. ``300px``, ``100%``)
        * - :option:`:class:`
          - CSS class(es) on the wrapping div
        * - :option:`:name:`
          - Reference name (emitted as ``id`` on the wrapping div)
        * - :option:`:alt:`
          - Accessible description (emitted as ``aria-label`` on the wrapping div)

    .. code:: rst
        :class: copy-to-clipboard

        .. include-svg:: my_diagram.svg
            :width: 500px
            :height: 300px
            :class: diagram
            :name: figure-1
            :alt: A diagram showing the system architecture


.. container:: cheat-sheet-block

    .. rubric:: Exercise Directives

    .. rubric:: Exercise

    ``.. exercise:: <title>``

    .. list-table::
        :class: compact

        * - :info:`:formatted-title:`
          - Inline markup supported
        * - :info:`:name:`
          - Reference name
        * - :info:`:class:`
          - CSS class(es)

    .. code:: rst
        :class: copy-to-clipboard

        .. exercise:: My Exercise

            Exercise description.


    .. rubric:: Solution

    ``.. solution:: <title>`` *(must be nested inside exercise)*

    .. list-table::
        :class: compact

        * - :info:`:pwd:`
          - Password (min. 3 chars); auto-generated if omitted
        * - :info:`:class:`
          - CSS class(es)

    .. code:: rst
        :class: copy-to-clipboard

        .. exercise:: My Exercise

            .. solution::
                :pwd: 1234

                Solution content.


.. container:: cheat-sheet-block

    .. rubric:: Admonition Directives

    All custom admonitions support an optional title argument and the standard options:

    .. list-table::
        :class: compact

        * - :info:`:class:`
          - CSS class(es)
        * - :info:`:name:`
          - Reference name

    .. rubric:: Custom Admonitions

    ``.. background::``, ``.. definition::``, ``.. proof::``, ``.. theorem::``, ``.. lemma::``, ``.. conclusion::``, ``.. observation::``, ``.. remark::``, ``.. summary::``, ``.. legend::``, ``.. repetition::``, ``.. question::``, ``.. answer::``, ``.. remember::``, ``.. deprecated::``, ``.. assessment::``, ``.. example::``, ``.. discussion::``

    .. code:: rst
        :class: copy-to-clipboard

        .. theorem:: The Theorem Title
            :class: important

            The theorem statement.


.. container:: cheat-sheet-block

    .. rubric:: Content Directives

    .. rubric:: Story

    ``.. story:: <classes>``

    No custom options.

    .. code:: rst
        :class: copy-to-clipboard

        .. story::

            A story block.


    .. rubric:: Scrollable

    ``.. scrollable:: <classes>``

    .. list-table::
        :class: compact

        * - :info:`:height:`
          - CSS height value (e.g. ``300px``, ``10em``)

    .. code:: rst
        :class: copy-to-clipboard

        .. scrollable::
            :height: 300px

            Long content that scrolls.


    .. rubric:: Popover

    ``.. popover:: <title>``

    .. list-table::
        :class: compact

        * - :info:`:class:`
          - CSS class(es) for the trigger button

    .. code:: rst
        :class: copy-to-clipboard

        .. popover:: Click me
            :class: my-button

            Hidden popover content.


.. container:: cheat-sheet-block

    .. rubric:: Code Directive Extension

    ``.. code:: <language>`` — Standard docutils directive, extended with:

    .. list-table::
        :class: compact

        * - :info:`:line-number-digits:`
          - Integer 1–4; minimum padding width for line numbers

    Implicitly enables ``:number-lines:`` when set.

    .. code:: rst
        :class: copy-to-clipboard

        .. code:: java
            :line-number-digits: 2

            public static void main(...) { }
