"""Tests for the ``exercise`` directive, focusing on title span wrapping."""

import pytest


class TestExerciseDirective:
    """Comprehensive tests for exercise title rendering."""

    def test_exercise_with_plain_title(self, publish_html):
        """A plain title should be wrapped in a <span> inside the rubric."""
        rst = """
Title
=====

.. exercise:: My Title

   Exercise content.
"""
        html = publish_html(rst)
        assert '<p class="ld-exercise-title rubric"><span>My Title</span></p>' in html

    def test_exercise_with_formatted_title(self, publish_html):
        """A formatted title with inline markup should be wrapped in a <span>."""
        rst = """
Title
=====

.. exercise:: My Title
   :formatted-title: This is *important*

   Exercise content.
"""
        html = publish_html(rst)
        assert '<p class="ld-exercise-title rubric"><span>This is <em>important</em></span></p>' in html

    def test_exercise_without_title(self, publish_html):
        """An exercise without a title should not emit a rubric."""
        rst = """
Title
=====

.. exercise::

   Exercise content.
"""
        html = publish_html(rst)
        assert "ld-exercise-title" not in html
        assert "<div class=\"ld-exercise\"" in html

    def test_exercise_with_class_option(self, publish_html):
        """The :class: option should be appended to the exercise div classes."""
        rst = """
Title
=====

.. exercise:: My Title
   :class: difficult

   Exercise content.
"""
        html = publish_html(rst)
        assert '<div class="ld-exercise difficult"' in html
        assert '<p class="ld-exercise-title rubric"><span>My Title</span></p>' in html

    def test_plain_rubric_not_wrapped(self, publish_html):
        """A rubric outside of an exercise should NOT be wrapped in a <span>."""
        rst = """
Title
=====

.. rubric:: A plain rubric

Some text.
"""
        html = publish_html(rst)
        assert '<p class="rubric">A plain rubric</p>' in html
        assert "<span>" not in html

    def test_exercise_data_attributes(self, publish_html):
        """Exercise div should have correct data-exercise-id and data-exercise-title."""
        rst = """
Title
=====

.. exercise:: My Title

   Exercise content.
"""
        html = publish_html(rst)
        assert 'data-exercise-id="1"' in html
        assert 'data-exercise-title="1 - My Title"' in html
        assert 'id="ld-exercise-1"' in html
