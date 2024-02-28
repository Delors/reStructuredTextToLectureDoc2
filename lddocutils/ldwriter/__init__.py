from sys import stderr

from docutils import frontend, nodes, utils
from docutils.nodes import TextElement, Inline, container, title, rubric
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import unchanged_required, class_option
from docutils.writers import html5_polyglot

import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, SHA256
from Crypto.Random import get_random_bytes



"""
This Writer is heavily inspired by the rst2s5 writer:
https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/s5_html/__init__.py
"""
class Writer(html5_polyglot.Writer):

    supported = ("html", "xhtml")
    """Formats this writer supports."""

    settings_spec = html5_polyglot.Writer.settings_spec + (
        "LectureDoc2 Specific Options",
        "Configuration options used when generating LectureDoc2 lecture notes.",
        (
            (
                "Specifies the path to LectureDoc2.",
                ["--ld-path"],
                {"metavar": "<URL>", "default": "ld"},
            ),
        ),
    )

    config_section = "ld_html writer"
    config_section_dependencies = ("writers", "html writers", "html5_polyglot writer")

    def __init__(self):
        html5_polyglot.Writer.__init__(self)
        self.translator_class = LDTranslator


"""
We are supporting protected exercise solutions in the following way:

.. exercise:: "title"
    :class: warning
    
    <exercise content>

    .. solution:: "password"

        Helpful Links:

            https://gist.github.com/mastbaum/2655700

            https://docutils.sourceforge.io/docs/howto/rst-directives.html
"""


class solution(container):
    # Examples are in `docutils.nodes`
    pass


class Solution(Directive):
    # Examples are in docutils.parsers.rst.directives.*

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 0
    has_content = True
    option_spec = {"pwd": unchanged_required, "class": class_option}

    def run(self):
        # TODO check that solution is the last child element of an exercise
        self.assert_has_content()
        if "pwd" not in self.options or len(self.options["pwd"]) < 3:
            raise self.error(
                'solution requires a password with at least three characters: ":pwd: <password>"'
            )
        text = "\n".join(self.content)
        node = solution(rawsource=text)
        node.attributes["pwd"] = self.options["pwd"]
        if "class" in self.options:
            node.classes = " ".join(self.options["class"])
        if len(self.arguments) > 0:
            node += rubric(text=self.arguments[0])
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class exercise(container):
    # Examples are in `docutils.nodes`
    pass


class Exercise(Directive):
    # Examples are in docutils.parsers.rst.directives.*

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {"name": unchanged_required, "class": class_option}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = exercise(rawsource=text)
        node.classes = "ld-exercise"
        if "class" in self.options:
            node.classes += " " +" ".join(self.options["class"])
        if len(self.arguments) > 0:
            node += rubric(text=self.arguments[0])        
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class stack(container):
    # Examples are in `docutils.nodes`
    pass


class Stack(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = stack(rawsource=text)
        if "stack" in self.arguments:
            raise self.error(
                'The class "stack" is superfluous; it is automatically added.'
            )
        node.classes = "stack " + " ".join(self.arguments)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class layer(container):
    # Examples are in `docutils.nodes`
    pass


class Layer(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = layer(rawsource=text)
        # TODO add check for "superfluous" classes
        node.classes = "layer " + " ".join(self.arguments)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class supplemental(container):
    # Examples are in `docutils.nodes`
    pass


class Supplemental(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = stack(rawsource=text)
        # TODO add check for "superfluous" classes
        node.classes = "supplemental " + " ".join(self.arguments)
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class PresenterNotes(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        # TODO - for the time being we just swallow the content
        return []


class LDTranslator(html5_polyglot.HTMLTranslator):

    ld_stylesheet_normalize = """<link rel="stylesheet" href="%(ld_path)s/normalize.css" type="text/css" />\n"""

    ld_stylesheet_template = """\
    <script src="%(ld_path)s/ld-animations.js" type="text/javascript"></script>
    <script src="%(ld_path)s/ld-help.js" type="text/javascript"></script>
    <script src="%(ld_path)s/ld-core.js" type="text/javascript"></script>
    <link rel="stylesheet" href="%(ld_path)s/ld.css" type="text/css" />
    <link rel="stylesheet" href="%(ld_path)s/themes/DHBW/theme.css" type="text/css" />\n"""

    def __init__(self, *args):
        html5_polyglot.HTMLTranslator.__init__(self, *args)
        # insert ld-specific stylesheet and script stuff:
        """
        self.theme_file_path = None
        try:
            self.setup_theme()
        except docutils.ApplicationError as e:
            self.document.reporter.warning(e)
        view_mode = self.document.settings.view_mode
        control_visibility = ('visible', 'hidden')[self.document.settings
                                                   .hidden_controls]
        self.stylesheet.append(self.s5_stylesheet_template
                               % {'path': self.theme_file_path,
                                  'view_mode': view_mode,
                                  'control_visibility': control_visibility})
        if not self.document.settings.current_slide:
            self.stylesheet.append(self.disable_current_slide)
        self.s5_footer = []
        self.s5_header = []
        
        self.theme_files_copied = None
        """
        # overwrite HTML meta tag default
        ld_path = self.document.settings.ld_path
        self.stylesheet.insert(0, self.ld_stylesheet_normalize % {"ld_path": ld_path})
        self.stylesheet.append(self.ld_stylesheet_template % {"ld_path": ld_path})
        self.meta = [
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0, user-scalable=no" />\n'
        ]
        self.meta.append(
            '<meta http-equiv="Content-Type" ' 'content="text/html; charset=utf-8">\n'
        )
        self.meta.append('<meta name="version" content="LD2 0.1" />\n')

        self.section_count = 0

        self.start_of_exercise = None
        self.start_of_solution = None

    def depart_document(self, node):
        self.head_prefix.extend(
            [
                self.doctype,
                self.head_prefix_template % {"lang": self.settings.language_code},
            ]
        )
        self.html_prolog.append(self.doctype)
        self.head = self.meta[:] + self.head
        if self.math_header:
            if self.math_output == "mathjax":
                self.head.extend(self.math_header)
            else:
                self.stylesheet.extend(self.math_header)
        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        self.fragment.extend(self.body)
        # title = ''.join(self.html_title).replace('<h1 class="title">', '<h1>')
        # layout = self.layout_template % {'header': header,
        #                                 'title': title,
        #                                 'footer': footer}
        # self.body_prefix.extend(layout)
        # self.body_prefix.append('<main>\n')
        all_classes = node.document["classes"]
        all_classes.append("ld-slide")
        self.body_prefix.append(
            self.starttag({"classes": all_classes, "ids": ["slide0"]}, "div")
        )
        if not self.section_count:
            self.body.append("</div>\n")

        # self.body_suffix.insert(0, '</main>\n')
        self.html_body.extend(
            self.body_prefix[1:]
            + self.body_pre_docinfo
            + self.docinfo
            + self.body
            + self.body_suffix[:-1]
        )

    def visit_title(self, node):
        html5_polyglot.HTMLTranslator.visit_title(self, node)

    def visit_subtitle(self, node):
        if isinstance(node.parent, nodes.section):
            level = self.section_level + self.initial_header_level - 1
            if level == 1:
                level = 2
            tag = "h%s" % level
            self.body.append(self.starttag(node, tag, ""))
            self.context.append("</%s>\n" % tag)
        else:
            html5_polyglot.HTMLTranslator.visit_subtitle(self, node)

    def visit_section(self, node):
        if not self.section_count:
            self.body.append("</div>\n")
        self.section_count += 1
        self.section_level += 1
        if self.section_level > 1:
            # dummy for matching div's
            self.body.append(self.starttag(node, "div", CLASS="section"))
        else:
            self.body.append(self.starttag(node, "div", CLASS="ld-slide"))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append("</div>")

    def visit_subscript(self, node):
        self.body.append(self.starttag(node, "sub"))

    def depart_subscript(self, node):
        self.body.append("</sub>")

    def visit_superscript(self, node):
        self.body.append(self.starttag(node, "sup"))

    def depart_superscript(self, node):
        self.body.append("</sup>")

    def visit_stack(self, node):
        self.body.append(self.starttag(node, "div", CLASS=node.classes))

    def depart_stack(self, node):
        self.body.append("</div>")

    def visit_layer(self, node):
        self.body.append(self.starttag(node, "div", CLASS=node.classes))

    def depart_layer(self, node):
        self.body.append("</div>")

    def visit_supplemental(self, node):
        self.body.append(self.starttag(node, "div", CLASS=node.classes))

    def depart_supplemental(self, node):
        self.body.append("</div>")

    def visit_exercise(self, node):
        if self.start_of_exercise is not None:
            raise self.error("exercises cannot be nested")
        self.start_of_exercise = len(self.body)
        self.body.append(self.starttag(node, "div", CLASS=node.classes))

    def depart_exercise(self, node):
        self.start_of_exercise = None
        self.body.append("</div>")

    def visit_solution(self, node):
        if self.start_of_solution is not None:
            raise self.error("solutions cannot be nested")

        self.body.append(self.starttag(node, "div", CLASS="ld-exercise-solution"))
        self.start_of_solution = len(self.body)

    def depart_solution(self, node):
        # Idea:
        # 1. Extract the solution
        # 2. Remove the solution from the body
        # 3. Encrypt the solution
        # 4. Add the encrypted solution to the body (base64 encoded)
        end_of_solution = len(self.body)
        exercise_body = "".join(self.body[self.start_of_solution : end_of_solution + 1])
        del self.body[self.start_of_solution :]
        self.start_of_solution = None
        key = node.attributes["pwd"].encode("utf-8")
        salt = get_random_bytes(16)
        aesKey = PBKDF2(key, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        cipher = AES.new(aesKey, AES.MODE_CTR)
        ciphertext = cipher.encrypt(exercise_body.encode("utf-8"))
        self.body.append(base64.b64encode(salt).decode("utf-8"))
        self.body.append(":")
        self.body.append(base64.b64encode(ciphertext).decode("utf-8"))
        self.body.append("</div>")


#
# Convenience directives which are shortcuts for using containers
# with classes:
directives.register_directive("stack", Stack)
directives.register_directive("layer", Layer)

directives.register_directive("supplemental", Supplemental)

directives.register_directive("presenter-notes", PresenterNotes)

#
# Directives which implement more advanced features:
directives.register_directive("exercise", Exercise)
directives.register_directive("solution", Solution)
