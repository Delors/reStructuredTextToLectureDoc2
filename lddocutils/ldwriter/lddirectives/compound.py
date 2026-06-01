"""Extend the ``compound`` directive with a ``:theme:`` option.

Monkey-patches :class:`~docutils.parsers.rst.directives.body.Compound`
to support ``:theme:`` (free-form string) which is then emitted as a
``data-theme`` attribute in HTML output.
"""

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.body import Compound


# --- monkey-patch Compound --------------------------------------------------

Compound.option_spec["theme"] = directives.unchanged_required

_original_run = Compound.run


def _patched_run(self):
    result = _original_run(self)

    theme = self.options.get("theme")
    if theme:
        for node in result:
            if isinstance(node, nodes.compound):
                node.attributes["theme"] = theme

    return result


Compound.run = _patched_run
