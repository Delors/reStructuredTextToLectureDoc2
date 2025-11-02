# popover_directive.py
from docutils import nodes
from docutils.parsers.rst import Directive, directives
import re
from lddocutils.ldwriter import LDTranslator, make_classes


class popover(nodes.General, nodes.Element):
    pass



def class_option(argument):
    return directives.class_option(argument)

class PopoverDirective(Directive):
    has_content = True
    required_arguments = 1   # title
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'class': class_option,
    }

    def run(self):
        title_text = self.arguments[0]

        # Parse inline markup inside the title
        title_nodes, title_messages = self.state.inline_text(title_text, self.lineno)

        # Create container and assign a document-unique id derived from title
        container = popover()
        popover_id_candidate = nodes.make_id(title_text);
        self.state.document.set_id(container,suggested_prefix=popover_id_candidate )
        popover_id = container['ids'][0]

        container['popover_id'] = popover_id
        container['title_nodes'] = title_nodes
        container['button_classes'] = ['popover'] + (self.options.get('class', []) or [])

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container] + title_messages

def visit_popover(self, node: popover):
    btn_classes = ' '.join(node.get('button_classes', ['popover']))
    pop_id = node.get('popover_id') or (node['ids'][0] if node.get('ids') else '')
    
    self.body.append(
        f'<button class="{btn_classes}" popovertarget="{pop_id}">'
    )

    # Render inline-formatted title
    for title_child in node.get('title_nodes', []):
        title_child.walkabout(self)

    # Close button
    self.body.append('</button>')

    # Start the popover div; body content will follow
    self.body.append(f'<div id="{pop_id}" popover="auto">')

def depart_popover(self, node: popover):
    # Close the popover div after content is rendered
    self.body.append('</div>')


LDTranslator.visit_popover = visit_popover
LDTranslator.depart_popover = depart_popover

directives.register_directive('popover', PopoverDirective)