"""Tests for custom admonition directives."""

import pytest


class TestAdmonitionIds:
    """Tests that target references (.. _label:) propagate IDs correctly."""

    def test_target_reference_id_on_admonition(self, publish_html):
        """A preceding target reference must appear as id on the admonition."""
        rst = """
Title
=====

.. _openness:

.. definition::

   Test definition.
"""
        html = publish_html(rst)
        assert '<aside class="admonition" id="openness" data-theme="definition">' in html

    def test_target_reference_id_on_theorem(self, publish_html):
        """Target IDs work for all admonition types."""
        rst = """
Title
=====

.. _my-theorem:

.. theorem:: Pythagorean Theorem

   a^2 + b^2 = c^2
"""
        html = publish_html(rst)
        assert '<aside class="admonition" id="my-theorem" data-theme="theorem">' in html

    def test_admonition_without_target_no_id(self, publish_html):
        """Admonitions without a preceding target reference have no id attribute."""
        rst = """
Title
=====

.. definition::

   Test definition.
"""
        html = publish_html(rst)
        assert "<aside class=\"admonition\" data-theme=" in html
        assert ' id=' not in html.split("<aside ")[1].split(">")[0]
