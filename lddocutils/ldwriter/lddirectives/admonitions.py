#
# Additional Admonitions (LD2 - Renaissance)

from docutils.languages import en, de
from docutils.nodes import Element, Admonition
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

# Example Admonition

de.labels["example"] = "Beispiel"
en.labels["example"] = "Example"

class example(Admonition, Element):
    pass

class Example(BaseAdmonition):

    node_class = example

directives.register_directive("example", Example)


# Background Admonition

de.labels["background"] = "Hintergrund"
en.labels["background"] = "Background"


class background(Admonition, Element):
    pass


de.labels["definition"] = "Definition"
en.labels["definition"] = "Definition"


class definition(Admonition, Element):
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



class Background(BaseAdmonition):

    node_class = background


directives.register_directive("background", Background)


class Definition(BaseAdmonition):

    node_class = definition


directives.register_directive("definition", Definition)


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
