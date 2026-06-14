#
# Include SVG Directive (LD2 - Renaissance)
#
# Embeds the raw content of an SVG file directly into the HTML output,
# wrapped in a <div> with inline width/height styles.
#
# Usage::
#
#     .. include-svg:: my_diagram.svg
#         :width: 500px
#         :height: 300px
#         :class: my-class
#         :name: my-diagram
#
# Generated HTML::
#
#     <div style="width: 500px; height: 300px;" class="my-class" id="my-diagram">
#       <svg ...>...</svg>
#     </div>

from docutils import nodes
from docutils.nodes import Element, General
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import class_option, unchanged, unchanged_required
from docutils.writers._html_base import SimpleListChecker
from lddocutils.ldwriter import LDTranslator, make_classes

# ──────────────────────────────────────────────────────────────────────
# Node
# ──────────────────────────────────────────────────────────────────────


class include_svg(General, Element):
    """Custom node for inline SVG embedding."""

    pass


# ──────────────────────────────────────────────────────────────────────
# Directive
# ──────────────────────────────────────────────────────────────────────


class IncludeSVG(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False
    option_spec = {
        "width": unchanged_required,
        "height": unchanged_required,
        "class": class_option,
        "name": unchanged,
        "alt": unchanged,
    }

    def run(self):
        if "width" not in self.options:
            raise self.error("The :width: option is required.")
        if "height" not in self.options:
            raise self.error("The :height: option is required.")

        filename = self.state_machine.document["source"]
        relative_curdir = os.path.dirname(filename)
        svg_path = os.path.join(relative_curdir, self.arguments[0])

        try:
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
        except FileNotFoundError:
            raise self.error(f"SVG file not found: {svg_path}")
        except IOError as e:
            raise self.error(f"Could not read SVG file {svg_path}: {e}")

        node = include_svg()
        node["svg_content"] = svg_content
        node["width"] = self.options["width"]
        node["height"] = self.options["height"]

        if "class" in self.options:
            node["classes"] = self.options["class"]

        if "name" in self.options:
            self.add_name(node)

        if "alt" in self.options:
            node["alt"] = self.options["alt"]

        node.source, node.line = self.state_machine.get_source_and_line(self.lineno)

        return [node]


# ──────────────────────────────────────────────────────────────────────
# HTML rendering (LDTranslator visitor)
# ──────────────────────────────────────────────────────────────────────


def visit_include_svg(self, node):
    style = f"width: {node['width']}; height: {node['height']};"
    attributes = {"style": style}
    if "alt" in node:
        attributes["aria-label"] = node["alt"]
    self.body.append(self.starttag(node, "div", **attributes))
    self.body.append(node["svg_content"])


def depart_include_svg(self, node):
    self.body.append("</div>")


LDTranslator.visit_include_svg = visit_include_svg
LDTranslator.depart_include_svg = depart_include_svg


# ──────────────────────────────────────────────────────────────────────
# SimpleListChecker — prevent NotImplementedError for this node type
# ──────────────────────────────────────────────────────────────────────


def _raise_node_found(self, node):
    raise nodes.NodeFound


SimpleListChecker.visit_include_svg = _raise_node_found
SimpleListChecker.depart_include_svg = lambda self, node: None


# ──────────────────────────────────────────────────────────────────────
# Register directive
# ──────────────────────────────────────────────────────────────────────

import os

directives.register_directive("include-svg", IncludeSVG)
