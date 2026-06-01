"""Tests for the extended ``compound`` directive."""

import pytest
from docutils.utils import SystemMessage


class TestCompoundDirective:
    """Comprehensive tests for :theme: and :class: options on compound."""

    def test_plain_compound_no_theme(self, publish_html):
        """A compound without any custom options renders a basic div."""
        rst = """
Title
=====

.. compound::

   Paragraph inside compound.
"""
        html = publish_html(rst)
        assert '<div class="compound">' in html
        # The <body> tag may have its own data-theme attribute, so we assert
        # that the compound div specifically does not carry one.
        assert '<div class="compound" data-theme' not in html

    def test_compound_with_theme(self, publish_html):
        """The :theme: option is emitted as a data-theme attribute."""
        rst = """
Title
=====

.. compound::
   :theme: muted

   Paragraph inside compound.
"""
        html = publish_html(rst)
        assert '<div class="compound" data-theme="muted">' in html

    def test_compound_with_class(self, publish_html):
        """The built-in :class: option still works correctly."""
        rst = """
Title
=====

.. compound::
   :class: my-class

   Paragraph inside compound.
"""
        html = publish_html(rst)
        # Docutils prepends user classes before the default "compound" class.
        assert 'class="my-class compound"' in html
        assert '<div class="my-class compound" data-theme' not in html

    def test_compound_with_theme_and_class(self, publish_html):
        """Both :theme: and :class: can be used together."""
        rst = """
Title
=====

.. compound::
   :class: my-class another
   :theme: dark

   Paragraph inside compound.
"""
        html = publish_html(rst)
        assert 'class="my-class another compound"' in html
        assert 'data-theme="dark"' in html

    def test_compound_empty_theme_raises_error(self, publish_html):
        """A :theme: option without a value must raise an error."""
        rst = """
Title
=====

.. compound::
   :theme:

   Paragraph inside compound.
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)
