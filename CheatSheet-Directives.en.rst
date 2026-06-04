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

        * - :option:`:align:`
          - ``auto`` (default), ``center``, ``start``, ``end``
        * - :option:`:theme:`
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

        * - :option:`:theme:` *(deck)*
          - Any theme name (emitted as ``data-theme`` on ``<ld-deck>``)
        * - :option:`:theme:` *(card)*
          - Any theme name (emitted as ``data-theme`` on ``<ld-card>``)
        * - :option:`:not-incremental:` *(card)*
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

        * - :option:`:theme:`
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

        * - :option:`:formatted-title:`
          - Inline markup supported (e.g. ``**bold**``)
        * - :option:`:symbol:`
          - Single character symbol (e.g. ``λ``)
        * - :option:`:type:`
          - ``cheat-sheet`` (default) or ``slide``
        * - :option:`:embed:`
          - Flag; embed in document flow
        * - :option:`:class:`
          - CSS class(es)
        * - :option:`:name:`
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

        * - :option:`:embed-in-document-flow:`
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

        * - :option:`:name:`
          - Reference name

    .. code:: rst
        :class: copy-to-clipboard

        .. presenter-note::

            Notes for the presenter.


    .. rubric:: Module

    ``.. module:: <name>``

    .. list-table::
        :class: compact

        * - :option:`:class:`
          - CSS class(es)
        * - :option:`:scope:`
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

        * - :option:`:prefix:`
          - Text to prepend to the resolved path
        * - :option:`:suffix:`
          - Text to append to the resolved path
        * - :option:`:path:`
          - ``relative`` (default) or ``absolute``

    .. code:: rst
        :class: copy-to-clipboard

        .. source:: my_file.rst
            :prefix: https://example.com/
            :path: absolute


.. container:: cheat-sheet-block

    .. rubric:: Exercise Directives

    .. rubric:: Exercise

    ``.. exercise:: <title>``

    .. list-table::
        :class: compact

        * - :option:`:formatted-title:`
          - Inline markup supported
        * - :option:`:name:`
          - Reference name
        * - :option:`:class:`
          - CSS class(es)

    .. code:: rst
        :class: copy-to-clipboard

        .. exercise:: My Exercise

            Exercise description.


    .. rubric:: Solution

    ``.. solution:: <title>`` *(must be nested inside exercise)*

    .. list-table::
        :class: compact

        * - :option:`:pwd:`
          - Password (min. 3 chars); auto-generated if omitted
        * - :option:`:class:`
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

        * - :option:`:class:`
          - CSS class(es)
        * - :option:`:name:`
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

        * - :option:`:height:`
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

        * - :option:`:class:`
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

        * - :option:`:line-number-digits:`
          - Integer 1–4; minimum padding width for line numbers

    Implicitly enables ``:number-lines:`` when set.

    .. code:: rst
        :class: copy-to-clipboard

        .. code:: java
            :line-number-digits: 2

            public static void main(...) { }


