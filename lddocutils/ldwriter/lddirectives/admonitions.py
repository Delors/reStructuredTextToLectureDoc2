#
# Additional Admonitions (LD2 - Renaissance)

from docutils import nodes
from docutils.languages import en, de
from docutils.nodes import General, Element, Admonition
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from lddocutils.ldwriter import LDTranslator, make_classes

"""Admonition with an optional title."""
class TitledAdmonition(Directive):

    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}
    has_content = True

    node_class = None
    """Subclasses must set this to the appropriate admonition node class."""

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)
        admonition_node.source, admonition_node.line = \
            self.state_machine.get_source_and_line(self.lineno)
        if len(self.arguments) > 0:
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text,
                                                         self.lineno)
            title = nodes.title(title_text, '', *textnodes)
            title.source, title.line = (
                    self.state_machine.get_source_and_line(self.lineno))
            admonition_node += title
            admonition_node += messages
            #if 'classes' not in self.options:
            #    admonition_node['classes'] += ['admonition-'
            #                                   + nodes.make_id(title_text)]
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)
        return [admonition_node]


de.labels["definition_admonition"] = "Definition"
en.labels["definition_admonition"] = "Definition"

class definition_admonition(General, Element):
    pass

class DefinitionAdmonition(TitledAdmonition):
    node_class = definition_admonition

# Custom HTML rendering for "definition" admonitions:
def visit_definition_admonition(self, node):
    classes = ["admonition", "definition"] + node.get("classes", [])
    class_attr = " ".join(make_classes(classes))
    self.body.append(f'<aside class="{class_attr}">')

    # Render title: "Definition: {optional title}"
    label = getattr(self, "language", None).labels.get("definition_admonition", "Definition")
    self.body.append('<p class="admonition-title"><span>')
    self.body.append(f"{label}")

    # Extract optional title node and render its inline content
    title_node = None
    for i, child in enumerate(node.children):
        if isinstance(child, nodes.title):
            title_node = child
            del node.children[i]  # prevent default title rendering
            break

    if title_node is not None:
        self.body.append(": ")
        for child in title_node.children:
            child.walkabout(self)

    self.body.append("</span></p>")

def depart_definition_admonition(self, node):
    # Close admonition container
    self.body.append("</aside>")

LDTranslator.visit_definition_admonition = visit_definition_admonition
LDTranslator.depart_definition_admonition = depart_definition_admonition

directives.register_directive("definition", DefinitionAdmonition)


de.labels["example"] = "Beispiel"
en.labels["example"] = "Example"
class example(Admonition, Element):
    pass

class Example(BaseAdmonition):

    node_class = example

directives.register_directive("example", Example)

de.labels["background"] = "Hintergrund"
en.labels["background"] = "Background"

class background(Admonition, Element):
    pass





de.labels["proof"] = "Beweis"
en.labels["proof"] = "Proof"


class proof(Admonition, Element):
    pass


de.labels["theorem"] = "Satz"
en.labels["theorem"] = "Theorem"


class theorem(Admonition, Element):
    pass


de.labels["lemma"] = "Lemma"
en.labels["lemma"] = "Lemma"


class conclusion(Admonition, Element):
    pass


de.labels["conclusion"] = "Schlussfolgerung"
en.labels["conclusion"] = "Conclusion"


class lemma(Admonition, Element):
    pass


de.labels["observation"] = "Beobachtung"
en.labels["observation"] = "Observation"


class observation(Admonition, Element):
    pass


de.labels["remark"] = "Bemerkung"
en.labels["remark"] = "Remark"


class remark(Admonition, Element):
    pass


de.labels["summary"] = "Zusammenfassung"
en.labels["summary"] = "Summary"


class summary(Admonition, Element):
    pass


de.labels["legend"] = "Legende"
en.labels["legend"] = "Legend"


class legend(Admonition, Element):
    pass


de.labels["repetition"] = "Wiederholung"
en.labels["repetition"] = "Repetition"


class repetition(Admonition, Element):
    pass


de.labels["question"] = "Frage"
en.labels["question"] = "Question"


class question(Admonition, Element):
    pass


de.labels["answer"] = "Antwort"
en.labels["answer"] = "Answer"


class answer(Admonition, Element):
    pass


de.labels["remember"] = "Zur Erinnerung"
en.labels["remember"] = "Remember"


class remember(Admonition, Element):
    pass


de.labels["deprecated"] = "Veraltet"
en.labels["deprecated"] = "Deprecated"
class deprecated(Admonition, Element):
    pass



de.labels["assessment"] = "Bewertung"
en.labels["assessment"] = "Assessment"


class assessment(Admonition, Element):
    pass



class Background(BaseAdmonition):

    node_class = background


directives.register_directive("background", Background)




class Proof(BaseAdmonition):

    node_class = proof


directives.register_directive("proof", Proof)


class Theorem(BaseAdmonition):

    node_class = theorem


directives.register_directive("theorem", Theorem)


class Lemma(BaseAdmonition):

    node_class = lemma


directives.register_directive("lemma", Lemma)


class Conclusion(BaseAdmonition):

    node_class = conclusion


directives.register_directive("conclusion", Conclusion)


class Observation(BaseAdmonition):

    node_class = observation


directives.register_directive("observation", Observation)


class Remark(BaseAdmonition):

    node_class = remark


directives.register_directive("remark", Remark)


class Summary(BaseAdmonition):

    node_class = summary


directives.register_directive("summary", Summary)


class Legend(BaseAdmonition):

    node_class = legend


directives.register_directive("legend", Legend)


class Repetition(BaseAdmonition):

    node_class = repetition


directives.register_directive("repetition", Repetition)


class Question(BaseAdmonition):

    node_class = question


directives.register_directive("question", Question)


class Answer(BaseAdmonition):

    node_class = answer


directives.register_directive("answer", Answer)


class Remember(BaseAdmonition):

    node_class = remember


directives.register_directive("remember", Remember)


class Deprecated(BaseAdmonition):

    node_class = deprecated


directives.register_directive("deprecated", Deprecated)


class Assessment(BaseAdmonition):

    node_class = assessment


directives.register_directive("assessment", Assessment)



