#
# Additional Admonitions (LD2 - Renaissance)

from docutils import nodes
from docutils.languages import de, en
from docutils.nodes import Element, General
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import set_classes
from docutils.writers._html_base import SimpleListChecker
from lddocutils.ldwriter import LDTranslator, make_classes


def _raise_node_found(self, node):
    raise nodes.NodeFound


def _noop(self, node):
    pass


class TitledAdmonition(Directive):
    """Admonition with an optional title."""

    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {"class": directives.class_option, "name": directives.unchanged}
    has_content = True

    node_class = None
    """Subclasses must set this to the appropriate admonition node class."""

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = "\n".join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)
        admonition_node.source, admonition_node.line = (
            self.state_machine.get_source_and_line(self.lineno)
        )
        if len(self.arguments) > 0:
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text, self.lineno)
            title = nodes.title(title_text, "", *textnodes)
            title.source, title.line = self.state_machine.get_source_and_line(
                self.lineno
            )
            admonition_node += title
            admonition_node += messages
        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]


# ──────────────────────────────────────────────────────────────────────
# Shared HTML rendering helpers for titled admonitions
# ──────────────────────────────────────────────────────────────────────


def _visit_titled_admonition(self, node, label_key, theme):
    """Render the opening markup for a titled admonition.

    *label_key* is the key used to look up the localised label in
    ``self.language.labels`` (e.g. ``"definition"``).
    *theme* is the admonition-specific data-theme name
    (e.g. ``"definition"``).
    """
    classes = ["admonition"] + node.get("classes", [])
    class_attr = " ".join(make_classes(classes))
    self.body.append(f'<aside class="{class_attr}" data-theme="{theme}">')

    # Render title: "Label: {optional title}"
    label = getattr(self, "language", None).labels.get(label_key, theme.title())
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


def _depart_titled_admonition(self, node):
    """Render the closing markup for a titled admonition."""
    self.body.append("</aside>")


# ──────────────────────────────────────────────────────────────────────
# Factory for registering admonitions
# ──────────────────────────────────────────────────────────────────────


def _register_titled_admonition(directive_name, label_key, theme, label_de, label_en):
    """Create node class, directive class, visit/depart methods and wire everything up."""
    de.labels[label_key] = label_de
    en.labels[label_key] = label_en

    # Node class (e.g. class definition(General, Element): pass)
    node_cls = type(directive_name, (General, Element), {})
    globals()[directive_name] = node_cls

    # Directive class (e.g. class Definition(TitledAdmonition): node_class = definition)
    dir_cls_name = directive_name.capitalize()
    dir_cls = type(dir_cls_name, (TitledAdmonition,), {"node_class": node_cls})
    globals()[dir_cls_name] = dir_cls

    # Translator visit/depart methods
    def _visit(self, node):
        _visit_titled_admonition(self, node, label_key, theme)

    def _depart(self, node):
        _depart_titled_admonition(self, node)

    visit_name = f"visit_{directive_name}"
    depart_name = f"depart_{directive_name}"
    setattr(LDTranslator, visit_name, _visit)
    setattr(LDTranslator, depart_name, _depart)

    # Register RST directive
    directives.register_directive(directive_name, dir_cls)

    # SimpleListChecker wiring
    setattr(SimpleListChecker, visit_name, _raise_node_found)
    setattr(SimpleListChecker, depart_name, _noop)


_ADMONITIONS = [
    # (directive_name, label_key, theme, label_de, label_en)
    ("definition", "definition", "definition", "Definition", "Definition"),
    ("example", "example", "example", "Beispiel", "Example"),
    ("discussion", "discussion", "discussion", "Diskussion", "Discussion"),
    ("background", "background", "background", "Hintergrund", "Background"),
    ("proof", "proof", "proof", "Beweis", "Proof"),
    ("theorem", "theorem", "theorem", "Satz", "Theorem"),
    ("lemma", "lemma", "lemma", "Lemma", "Lemma"),
    ("conclusion", "conclusion", "conclusion", "Schlussfolgerung", "Conclusion"),
    ("observation", "observation", "observation", "Beobachtung", "Observation"),
    ("remark", "remark", "remark", "Bemerkung", "Remark"),
    ("summary", "summary", "summary", "Zusammenfassung", "Summary"),
    ("legend", "legend", "legend", "Legende", "Legend"),
    ("repetition", "repetition", "repetition", "Wiederholung", "Repetition"),
    ("question", "question", "question", "Frage", "Question"),
    ("answer", "answer", "answer", "Antwort", "Answer"),
    ("remember", "remember", "remember", "Zur Erinnerung", "Remember"),
    ("deprecated", "deprecated", "deprecated", "Veraltet", "Deprecated"),
    ("assessment", "assessment", "assessment", "Bewertung", "Assessment"),
]

for _spec in _ADMONITIONS:
    _register_titled_admonition(*_spec)
