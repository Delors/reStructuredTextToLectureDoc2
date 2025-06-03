from docutils.parsers.rst import Directive, directives
from docutils.nodes import container

# from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged

from lddocutils.ldwriter import LDTranslator


class deck(container):
    pass


class Deck(Directive):

    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = deck(rawsource=text)
        if "deck" in self.arguments:
            raise self.error('"deck" is superfluous; it is automatically added.')
        node.attributes["classes"] += self.arguments
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class card(container):
    pass


class Card(Directive):

    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        if "card" in self.arguments:
            raise self.error('"card" is superfluous; it is automatically added.')

        if "incremental" in self.arguments:
            raise self.error('"incremental" is superfluous; it is automatically added.')

        text = "\n".join(self.content)
        node = card(rawsource=text)
        node.attributes["classes"] += self.arguments
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

def visit_deck(self, node):
    self.card_count.append(0)  # required to determine if a card is incremental
    starttag = self.starttag(node, "ld-deck")
    self.body.append(starttag)

def depart_deck(self, node):
    self.card_count.pop()
    self.body.append("</ld-deck>")

def visit_card(self, node):
    if len(self.card_count) == 0:
        raise Exception("card directive must be nested in a deck directive")
    card_id = self.card_count.pop()
    if card_id > 0:
        node.attributes["classes"] += ["incremental"]
    self.card_count.append(card_id + 1)
    self.body.append(self.starttag(node, "ld-card"))

def depart_card(self, node):
    self.body.append("</ld-card>")


LDTranslator.visit_deck = visit_deck
LDTranslator.depart_deck = depart_deck

LDTranslator.visit_card = visit_card
LDTranslator.depart_card = depart_card

directives.register_directive("deck", Deck)  # RENAISSANCE
directives.register_directive("card", Card)  # RENAISSANCE
