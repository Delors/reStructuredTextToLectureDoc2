from docutils import nodes, frontend
from docutils.nodes import General, Element, inline, container, title, rubric
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged

from lddocutils.ldwriter import LDTranslator

class story(container):
    pass


class Story(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()

        text = "\n".join(self.content)
        node = story(rawsource=text)
        node.attributes["classes"] += self.arguments
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


def visit_story(self, node):
    self.body.append(
        # When we explicitly set the class attribute, we will end up with 
        # a class attribute in HTML that lists all classes twice! Hence, 
        # don't add: ", CLASS=" ".join(node.attributes["classes"]))"
        self.starttag(node, "ld-story") 
    )


def depart_story(self, node):
    self.body.append("</ld-story>")


LDTranslator.visit_story = visit_story
LDTranslator.depart_story = depart_story


directives.register_directive("story", Story)
