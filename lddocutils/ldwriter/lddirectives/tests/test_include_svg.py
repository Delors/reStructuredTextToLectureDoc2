"""Tests for the ``include-svg`` directive."""

import os
import pytest
from docutils.utils import SystemMessage


class TestIncludeSVGDirective:
    """Comprehensive tests for the include-svg directive."""

    def test_basic_include_svg(self, publish_html, tmp_path):
        """Basic directive with width and height renders correctly."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100"/></svg>'
        svg_file = tmp_path / "diagram.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 500px
   :height: 300px
"""
        html = publish_html(rst)
        assert 'style="width: 500px; height: 300px;"' in html
        assert svg_content in html
        assert "</div>" in html

    def test_include_svg_with_class(self, publish_html, tmp_path):
        """The :class: option is emitted on the wrapping div."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40"/></svg>'
        svg_file = tmp_path / "circle.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 200px
   :height: 200px
   :class: my-class another-class
"""
        html = publish_html(rst)
        assert 'class="my-class another-class"' in html
        assert 'style="width: 200px; height: 200px;"' in html
        assert svg_content in html

    def test_include_svg_with_name(self, publish_html, tmp_path):
        """The :name: option is emitted as an id on the wrapping div."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><text x="10" y="20">Hello</text></svg>'
        svg_file = tmp_path / "text.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 100%
   :height: 100%
   :name: my-diagram
"""
        html = publish_html(rst)
        assert 'id="my-diagram"' in html
        assert 'style="width: 100%; height: 100%;"' in html
        assert svg_content in html

    def test_include_svg_with_class_and_name(self, publish_html, tmp_path):
        """Both :class: and :name: can be used together."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="0" x2="100" y2="100"/></svg>'
        svg_file = tmp_path / "line.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 400px
   :height: 400px
   :class: diagram
   :name: figure-1
"""
        html = publish_html(rst)
        assert 'id="figure-1"' in html
        assert 'class="diagram"' in html
        assert 'style="width: 400px; height: 400px;"' in html
        assert svg_content in html

    def test_include_svg_with_alt(self, publish_html, tmp_path):
        """The :alt: option is emitted as an aria-label on the wrapping div."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"/></svg>'
        svg_file = tmp_path / "rect.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 100px
   :height: 100px
   :alt: A small rectangle
"""
        html = publish_html(rst)
        assert 'aria-label="A small rectangle"' in html
        assert 'style="width: 100px; height: 100px;"' in html
        assert svg_content in html

    def test_include_svg_with_all_options(self, publish_html, tmp_path):
        """All options (width, height, class, name, alt) can be used together."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><polygon points="0,0 10,10"/></svg>'
        svg_file = tmp_path / "poly.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 200px
   :height: 200px
   :class: diagram
   :name: figure-2
   :alt: A simple polygon
"""
        html = publish_html(rst)
        assert 'id="figure-2"' in html
        assert 'class="diagram"' in html
        assert 'aria-label="A simple polygon"' in html
        assert 'style="width: 200px; height: 200px;"' in html
        assert svg_content in html

    def test_include_svg_missing_width_raises_error(self, publish_html, tmp_path):
        """Omitting the required :width: option raises a SystemMessage error."""
        svg_file = tmp_path / "diagram.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :height: 300px
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_missing_height_raises_error(self, publish_html, tmp_path):
        """Omitting the required :height: option raises a SystemMessage error."""
        svg_file = tmp_path / "diagram.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :width: 500px
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_missing_file_raises_error(self, publish_html, tmp_path):
        """Referencing a non-existent SVG file raises a hard error."""
        missing_file = tmp_path / "nonexistent.svg"

        rst = f"""
Title
=====

.. include-svg:: {missing_file}
   :width: 500px
   :height: 300px
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_relative_path(self, publish_html, tmp_path):
        """The filename is resolved relative to the source document."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg"><ellipse cx="50" cy="50" rx="40" ry="20"/></svg>'
        svg_file = tmp_path / "images" / "shape.svg"
        svg_file.parent.mkdir()
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: images/shape.svg
   :width: 250px
   :height: 150px
"""
        # We need to set the source document path to the tmp_path so relative
        # resolution works. publish_html doesn't set a source path, so we use
        # publish_string directly with a source_path override.
        from docutils.core import publish_string
        from lddocutils.ldwriter import Writer

        html = publish_string(
            source=rst,
            writer=Writer(),
            settings_overrides={
                "ld_path": "ld",
                "theme": "",
                "ld_passwords": "",
                "halt_level": 3,
                "source_path": str(tmp_path / "doc.rst"),
            },
        ).decode("utf-8")

        assert svg_content in html
        assert 'style="width: 250px; height: 150px;"' in html

    def test_include_svg_global(self, publish_html, tmp_path):
        """The :global: option prepends the SVG inside <ld-svg-globals>."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg" id="global-defs"><defs><linearGradient id="g"/></defs></svg>'
        svg_file = tmp_path / "global.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:

Some content.
"""
        html = publish_html(rst)
        assert "<ld-svg-globals>" in html
        assert "</ld-svg-globals>" in html
        assert svg_content in html
        assert html.index("<ld-svg-globals>") < html.index("<template")

    def test_include_svg_global_deduplication(self, publish_html, tmp_path):
        """The same :global: SVG referenced twice is included only once."""
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg" id="once"><symbol id="s"/></svg>'
        svg_file = tmp_path / "once.svg"
        svg_file.write_text(svg_content, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:

.. include-svg:: {svg_file}
   :global:
"""
        html = publish_html(rst)
        assert html.count(svg_content) == 1
        assert html.count("<ld-svg-globals>") == 1

    def test_include_svg_global_multiple_files(self, publish_html, tmp_path):
        """Multiple different :global: SVGs are included in order."""
        svg_a = '<svg xmlns="http://www.w3.org/2000/svg" id="a"><symbol id="sa"/></svg>'
        svg_b = '<svg xmlns="http://www.w3.org/2000/svg" id="b"><symbol id="sb"/></svg>'
        file_a = tmp_path / "a.svg"
        file_b = tmp_path / "b.svg"
        file_a.write_text(svg_a, encoding="utf-8")
        file_b.write_text(svg_b, encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {file_a}
   :global:

.. include-svg:: {file_b}
   :global:
"""
        html = publish_html(rst)
        assert html.index(svg_a) < html.index(svg_b)

    def test_include_svg_global_with_width_raises_error(self, publish_html, tmp_path):
        """:global: combined with :width: raises an error."""
        svg_file = tmp_path / "global.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:
   :width: 100px
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_global_with_height_raises_error(self, publish_html, tmp_path):
        """:global: combined with :height: raises an error."""
        svg_file = tmp_path / "global.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:
   :height: 100px
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_global_with_alt_raises_error(self, publish_html, tmp_path):
        """:global: combined with :alt: raises an error."""
        svg_file = tmp_path / "global.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:
   :alt: A global SVG
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_global_with_name_raises_error(self, publish_html, tmp_path):
        """:global: combined with :name: raises an error."""
        svg_file = tmp_path / "global.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:
   :name: my-global
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_global_with_class_raises_error(self, publish_html, tmp_path):
        """:global: combined with :class: raises an error."""
        svg_file = tmp_path / "global.svg"
        svg_file.write_text("<svg></svg>", encoding="utf-8")

        rst = f"""
Title
=====

.. include-svg:: {svg_file}
   :global:
   :class: my-global
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)

    def test_include_svg_global_missing_file_raises_error(self, publish_html, tmp_path):
        """A missing :global: SVG file raises a hard error."""
        missing_file = tmp_path / "missing.svg"

        rst = f"""
Title
=====

.. include-svg:: {missing_file}
   :global:
"""
        with pytest.raises(SystemMessage):
            publish_html(rst)
