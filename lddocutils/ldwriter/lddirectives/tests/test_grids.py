"""Tests for the extended ``cell`` directive."""

import pytest
from docutils.utils import SystemMessage


class TestCellDirective:
    """Comprehensive tests for :theme: option on cell."""

    def test_plain_cell_no_theme(self, publish_html):
        """A cell without any custom options renders a basic ld-cell."""
        rst = """
Title
=====

.. grid::

   .. cell::

      Paragraph inside cell.
"""
        html = publish_html(rst)
        assert "<ld-cell" in html
        # The <body> tag has its own data-theme; assert the cell specifically does not.
        assert '<ld-cell data-theme' not in html
        assert '<ld-cell style="align-self:auto;">' in html

    def test_cell_with_theme(self, publish_html):
        """The :theme: option is emitted as a data-theme attribute."""
        rst = """
Title
=====

.. grid::

   .. cell::
      :theme: dark

      Paragraph inside cell.
"""
        html = publish_html(rst)
        assert "<ld-cell" in html
        assert 'data-theme="dark"' in html
        assert 'style="align-self:auto;"' in html

    def test_cell_with_align_and_theme(self, publish_html):
        """Both :align: and :theme: can be used together."""
        rst = """
Title
=====

.. grid::

   .. cell::
      :align: center
      :theme: muted

      Paragraph inside cell.
"""
        html = publish_html(rst)
        assert "<ld-cell" in html
        assert 'data-theme="muted"' in html
        assert 'style="align-self:center;"' in html

    def test_cell_empty_theme_raises_error(self, publish_html):
        """A :theme: option without a value must raise an error."""
        rst = """
Title
=====

.. grid::

   .. cell::
      :theme:

      Paragraph inside cell.
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)
