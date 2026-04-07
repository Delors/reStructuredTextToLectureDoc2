#
# Global Information Directive (LD2 - Renaissance)
#
# Marks up information that is globally relevant for an entire slide set,
# e.g. background knowledge or reference material a viewer may need.
#
# Usage::
#
#     .. global-information:: Funktionale Programmierung in Java
#         :formatted-title: Glossar - *Funktionale Programmierung* in Java
#         :symbol: λ
#         :type: cheat-sheet | slide
#         :embed:
#         :class: my-class
#
#         ... parsed content ...
#
# Generated HTML::
#
#     <ld-global-information type="cheat-sheet"
#                            title="Funktionale Programmierung in Java"
#                            formatted-title="Glossar - &lt;em&gt;..."
#                            symbol="λ"
#                            class="...">
#       ...content...
#     </ld-global-information>

from html import escape as html_escape

from docutils import nodes
from docutils.nodes import Element, General
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import flag
from docutils.writers._html_base import SimpleListChecker
from lddocutils.ldwriter import LDTranslator, make_classes

# ──────────────────────────────────────────────────────────────────────
# Node
# ──────────────────────────────────────────────────────────────────────


class global_information(General, Element):
    """Custom node for global-information blocks."""

    # Hint: Uses ``General`` (not ``Admonition``) so that the
    #       ``writer_aux.Admonitions`` transform does not rewrite the node
    #       class before the translator can visit it.

    pass


# ──────────────────────────────────────────────────────────────────────
# Directive
# ──────────────────────────────────────────────────────────────────────


def _type_option(argument):
    """Validate and return the *type* option (default handled in run())."""
    return directives.choice(argument, ("cheat-sheet", "slide"))


class GlobalInformation(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "formatted-title": directives.unchanged,
        "symbol": directives.unchanged,
        "type": _type_option,
        "embed": flag,
        "class": directives.class_option,
        "name": directives.unchanged,
    }

    def run(self):
        title_text = self.arguments[0]
        symbol = self.options.get("symbol")
        info_type = self.options.get("type", "cheat-sheet")

        node = global_information()
        node["title"] = title_text
        if symbol:
            node["symbol"] = symbol
        node["info_type"] = info_type
        node["embed"] = "embed" in self.options

        # Parse the optional formatted-title through docutils' inline
        # parser so that RST inline markup (emphasis, roles, …) is
        # honoured.
        formatted_title_text = self.options.get("formatted-title")
        title_messages = []
        if formatted_title_text:
            title_nodes, title_messages = self.state.inline_text(
                formatted_title_text, self.lineno
            )
            node["title_nodes"] = title_nodes
        else:
            node["title_nodes"] = None

        if "class" in self.options:
            node["classes"] = self.options["class"]

        self.add_name(node)
        node.source, node.line = self.state_machine.get_source_and_line(self.lineno)

        # Parse body content into the node.
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node] + title_messages


# ──────────────────────────────────────────────────────────────────────
# HTML rendering (LDTranslator visitor)
# ──────────────────────────────────────────────────────────────────────


def visit_global_information(self, node):
    title = node.get("title", "")
    symbol = node.get("symbol")
    info_type = node.get("info_type", "cheat-sheet")
    classes = node.get("classes", [])

    attrs = (
        f'type="{html_escape(info_type, quote=True)}"'
        f' title="{html_escape(title, quote=True)}"'
    )

    if symbol:
        attrs += f' symbol="{html_escape(symbol, quote=True)}"'

    # Render the optional formatted-title to an HTML fragment by
    # temporarily swapping the translator's body list.
    title_nodes = node.get("title_nodes")
    if title_nodes is not None:
        saved_body = self.body
        self.body = []
        for child in title_nodes:
            child.walkabout(self)
        formatted_title_html = "".join(self.body)
        self.body = saved_body
        attrs += f' formatted-title="{html_escape(formatted_title_html, quote=True)}"'

    if node.get("embed", False):
        attrs += " embed"

    if classes:
        class_str = " ".join(make_classes(classes))
        attrs += f' class="{html_escape(class_str, quote=True)}"'

    self.body.append(f"<ld-global-information {attrs}>")


def depart_global_information(self, node):
    self.body.append("</ld-global-information>")


LDTranslator.visit_global_information = visit_global_information
LDTranslator.depart_global_information = depart_global_information


# ──────────────────────────────────────────────────────────────────────
# SimpleListChecker — prevent NotImplementedError for this node type
# ──────────────────────────────────────────────────────────────────────


def _raise_node_found(self, node):
    raise nodes.NodeFound


SimpleListChecker.visit_global_information = _raise_node_found
SimpleListChecker.depart_global_information = lambda self, node: None


# ──────────────────────────────────────────────────────────────────────
# Register directive
# ──────────────────────────────────────────────────────────────────────

directives.register_directive("global-information", GlobalInformation)
