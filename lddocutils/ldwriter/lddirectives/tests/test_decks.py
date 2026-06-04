"""Tests for the extended ``deck`` and ``card`` directives."""

import pytest
from docutils.utils import SystemMessage


class TestDeckDirective:
    """Comprehensive tests for :theme: option on deck."""

    def test_plain_deck_no_theme(self, publish_html):
        """A deck without any custom options renders a basic ld-deck."""
        rst = """
Title
=====

.. deck::

   .. card::

      Card content.
"""
        html = publish_html(rst)
        assert "<ld-deck" in html
        assert '<ld-deck data-theme' not in html

    def test_deck_with_theme(self, publish_html):
        """The :theme: option is emitted as a data-theme attribute on ld-deck."""
        rst = """
Title
=====

.. deck::
   :theme: dark

   .. card::

      Card content.
"""
        html = publish_html(rst)
        assert '<ld-deck data-theme="dark">' in html

    def test_deck_empty_theme_raises_error(self, publish_html):
        """A :theme: option without a value must raise an error."""
        rst = """
Title
=====

.. deck::
   :theme:

   .. card::

      Card content.
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)


class TestCardDirective:
    """Comprehensive tests for :theme: option on card."""

    def test_plain_card_no_theme(self, publish_html):
        """A card without any custom options renders a basic ld-card."""
        rst = """
Title
=====

.. deck::

   .. card::

      Card content.
"""
        html = publish_html(rst)
        assert "<ld-card" in html
        assert '<ld-card data-theme' not in html

    def test_card_with_theme(self, publish_html):
        """The :theme: option is emitted as a data-theme attribute on ld-card."""
        rst = """
Title
=====

.. deck::

   .. card::
      :theme: muted

      Card content.
"""
        html = publish_html(rst)
        assert '<ld-card data-theme="muted">' in html

    def test_card_not_incremental_with_theme(self, publish_html):
        """Both :not-incremental: and :theme: can be used together."""
        rst = """
Title
=====

.. deck::

   .. card::
      :not-incremental:
      :theme: dark

      Card content.
"""
        html = publish_html(rst)
        assert '<ld-card data-theme="dark">' in html
        # The first card should not get the incremental class even when
        # it is not the first card in the deck.

    def test_card_empty_theme_raises_error(self, publish_html):
        """A :theme: option without a value must raise an error."""
        rst = """
Title
=====

.. deck::

   .. card::
      :theme:

      Card content.
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)


class TestDeckAndCardTogether:
    """Tests for theme on both deck and card simultaneously."""

    def test_deck_and_card_with_theme(self, publish_html):
        """Both deck and card can carry a theme at the same time."""
        rst = """
Title
=====

.. deck::
   :theme: light

   .. card::
      :theme: dark

      Card content.
"""
        html = publish_html(rst)
        assert '<ld-deck data-theme="light">' in html
        assert '<ld-card data-theme="dark">' in html

    def test_deck_theme_card_no_theme(self, publish_html):
        """Only the deck has a theme; the card does not."""
        rst = """
Title
=====

.. deck::
   :theme: light

   .. card::

      Card content.
"""
        html = publish_html(rst)
        assert '<ld-deck data-theme="light">' in html
        assert "<ld-card" in html
        assert '<ld-card data-theme' not in html

    def test_deck_no_theme_card_with_theme(self, publish_html):
        """Only the card has a theme; the deck does not."""
        rst = """
Title
=====

.. deck::

   .. card::
      :theme: dark

      Card content.
"""
        html = publish_html(rst)
        assert "<ld-deck" in html
        assert '<ld-deck data-theme' not in html
        assert '<ld-card data-theme="dark">' in html
