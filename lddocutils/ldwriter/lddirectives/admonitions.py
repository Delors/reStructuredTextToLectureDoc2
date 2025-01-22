# 
# Additional Admonitions (LD2 - Renaissance)

from docutils.languages import en, de
from docutils.nodes import Element, Admonition
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

de.labels["example"] = "Beispiel"
en.labels["example"] = "Example"
class example(Admonition, Element): pass
de.labels["background"] = "Hintergrund"
en.labels["background"] = "Background"
class background(Admonition, Element): pass
de.labels["definition"] = "Definition"
en.labels["definition"] = "Definition"
class definition(Admonition, Element): pass
de.labels["proof"] = "Beweis"
en.labels["proof"] = "Proof"
class proof(Admonition, Element): pass
de.labels["theorem"] = "Satz"
en.labels["theorem"] = "Theorem"
class theorem(Admonition, Element): pass
de.labels["lemma"] = "Lemma"
en.labels["lemma"] = "Lemma"
class conclusion(Admonition, Element): pass
de.labels["conclusion"] = "Schlussfolgerung"
en.labels["conclusion"] = "Conclusion"
class lemma(Admonition, Element): pass
de.labels["observation"] = "Beobachtung"
en.labels["observation"] = "Observation"
class observation(Admonition, Element): pass
de.labels["remark"] = "Bemerkung"
en.labels["remark"] = "Remark"
class remark(Admonition, Element): pass
de.labels["summary"] = "Zusammenfassung"
en.labels["summary"] = "Summary"
class summary(Admonition, Element): pass
de.labels["legend"] = "Legende"
en.labels["legend"] = "Legend"
class legend(Admonition, Element): pass
de.labels["repetition"] = "Wiederholung"
en.labels["repetition"] = "Repetition"
class repetition(Admonition, Element): pass
de.labels["question"] = "Frage"
en.labels["question"] = "Question"
class question(Admonition, Element): pass


class Example(BaseAdmonition):

    node_class = example

class Background(BaseAdmonition):

    node_class = background

class Definition(BaseAdmonition):
    
    node_class = definition

class Proof(BaseAdmonition):
    
    node_class = proof

class Theorem(BaseAdmonition):
    
    node_class = theorem

class Lemma(BaseAdmonition):

    node_class = lemma

class Conclusion(BaseAdmonition):

    node_class = conclusion

class Observation(BaseAdmonition):

    node_class = observation

class Remark(BaseAdmonition):

    node_class = remark

class Summary(BaseAdmonition):

    node_class = summary

class Legend(BaseAdmonition):

    node_class = legend

class Repetition(BaseAdmonition):

    node_class = repetition

class Question(BaseAdmonition):

    node_class = question

directives.register_directive("example", Example)
directives.register_directive("background", Background)
directives.register_directive("definition", Definition)
directives.register_directive("proof", Proof)
directives.register_directive("theorem", Theorem)
directives.register_directive("lemma", Lemma)
directives.register_directive("conclusion", Conclusion)
directives.register_directive("observation", Observation)
directives.register_directive("remark", Remark)
directives.register_directive("summary", Summary)
directives.register_directive("legend", Legend)
directives.register_directive("repetition", Repetition)
directives.register_directive("question", Question)
