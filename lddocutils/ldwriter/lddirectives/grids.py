from docutils import nodes, frontend
from docutils.nodes import General, Element, inline, container, title, rubric
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged
from docutils.writers import html5_polyglot

from lddocutils.ldwriter import LDTranslator

class grid(container):
    """ Represents a grid.
    """

    pass


# The class is closely modeled after:
# docutils.parsers.rst.directives.admonitions.BaseAdmonition
class Grid(Directive):
    """
    We are supporting grid layouts by means of grid containers and cells.

    .. grid:: <classes>

        .. cell:: <classes>

            <cell content>

    Unless a specific configuration is given, a grid layout just creates
    a simple multiple column layout.
    """

    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True


    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = grid(rawsource=text)
        if len(self.arguments) > 0:
            node.attributes["classes"] = self.arguments
        # TODO add possibility to specify the overall layout
        node.attributes["classes"] += ["default-layout"]
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

def visit_grid(self, node):
    starttag = self.starttag(node, "ld-grid")
    self.body.append(starttag)

def depart_grid(self, node):
    self.body.append("</ld-grid>")


class cell(container):
    pass


class Cell(Directive):

    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = { "align": unchanged_required}

    def run(self):
        # TODO check that cells are the only children of grid nodes
        self.assert_has_content()

        text = "\n".join(self.content)
        node = cell(rawsource=text)
        if len(self.arguments) > 0:
            node.attributes["classes"] = self.arguments
        if "align" in self.options:
            node.attributes["align"] = self.options["align"]
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes

def visit_cell(self, node):
    style = "align-self:"+ (node.attributes["align"] if "align" in node.attributes else "auto")+";"
    attributes = {
        # "class": " ".join(node.attributes["classes"]),
        "style": style
    }
    starttag = self.starttag(node, "ld-cell", **attributes)
    self.body.append(starttag)

def depart_cell(self, node):
    self.body.append("</ld-cell>")

LDTranslator.visit_grid = visit_grid
LDTranslator.depart_grid = depart_grid

LDTranslator.visit_cell = visit_cell
LDTranslator.depart_cell = depart_cell

directives.register_directive("grid", Grid)
directives.register_directive("cell", Cell)
