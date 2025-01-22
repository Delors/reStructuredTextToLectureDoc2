from docutils import nodes, frontend
from docutils.nodes import General, Element, inline, container, title, rubric
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged
from docutils.writers import html5_polyglot




# Support for lecture integrated "questions" that are to be discussed immediately. 
# (LD2 - Renaissance)

######### TODO ########
class question(container):
    pass

class Question(Directive):  
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = question(rawsource=text)
        node.attributes["classes"] += ["ld-question"] + self.arguments
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class answer(container):
    pass

class Answer(Directive):
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = answer(rawsource=text)
        node.attributes["classes"] += ["ld-answer"] + self.arguments
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]
    
directives.register_directive("question", Question)
directives.register_directive("answer", Answer)
