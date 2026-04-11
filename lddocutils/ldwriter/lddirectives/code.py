"""Extend the ``code`` directive with a ``:line-number-digits:`` option.

Monkey-patches :class:`~docutils.parsers.rst.directives.body.CodeBlock`
to support ``:line-number-digits:`` (integer 1–4) controlling the
minimum padding width for line numbers.
"""

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.body import CodeBlock


def _line_number_digits(argument):
    """Validate ``:line-number-digits:`` – integer in 1 … 4."""
    value = directives.nonnegative_int(argument)
    if not 1 <= value <= 4:
        raise ValueError("line-number-digits must be between 1 and 4")
    return value


# --- monkey-patch CodeBlock --------------------------------------------------

CodeBlock.option_spec["line-number-digits"] = _line_number_digits

_original_run = CodeBlock.run


def _patched_run(self):
    min_digits = self.options.pop("line-number-digits", None)

    # Implicitly enable line numbering when only :line-number-digits: is set.
    if min_digits is not None and "number-lines" not in self.options:
        self.options["number-lines"] = None

    result = _original_run(self)

    if min_digits is not None:
        for node in result:
            if isinstance(node, nodes.literal_block):
                _repad_line_numbers(node, min_digits)

    return result


def _repad_line_numbers(node, min_digits):
    """Re-pad ``ln`` inlines to at least *min_digits* width."""
    # Determine effective width: max(min_digits, natural width)
    # so we never *shrink* padding if the block already has more lines.
    last_num = 0
    for child in node.children:
        if isinstance(child, nodes.inline) and "ln" in child.get("classes", []):
            try:
                last_num = int(child.astext())
            except ValueError:
                pass
    width = max(min_digits, len(str(last_num)))
    fmt = f"%{width}d"

    for child in node.children:
        if isinstance(child, nodes.inline) and "ln" in child.get("classes", []):
            try:
                num = int(child.astext())
                child.children = [nodes.Text(fmt % num)]
            except ValueError:
                pass


CodeBlock.run = _patched_run
