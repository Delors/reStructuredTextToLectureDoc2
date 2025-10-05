from itertools import batched
import json
import textwrap

from docutils import nodes, frontend
from docutils.nodes import General, Element, inline, container, title, rubric, make_id
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged
from docutils.writers import html5_polyglot

import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, SHA256
from Crypto.Random import get_random_bytes


"""
Writer for LectureDoc2 HTML output.

This Writer is heavily inspired by the rst2s5 writer:
https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/s5_html/__init__.py

# Examples definitions of `nodes` are in `docutils.nodes`
"""


def validate_modules_list(
    setting, value=None, option_parser=None, config_parser=None, config_section=None
):
    module_configurations = frontend.validate_comma_separated_list(
        setting, value, option_parser, config_parser, config_section
    )
    modules = dict(map(lambda tc: tc.split(sep=" ", maxsplit=1), module_configurations))

    return modules


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
            (
                "File in which the extracted passwords are stored.",
                ["--ld-passwords"],
                {"metavar": "<URL>"},
            ),
            (
                "Specifies the css file which defines the custom theme. The file has to be specified relative to LectureDoc's main folder.",
                ["--theme"],
                {"metavar": "<URL>"},
            ),
            (
                "Configures class-based modules.",
                ["--modules"],
                {
                    "metavar": "<class_name dir[,class_name dir,...]>",
                    "validator": validate_modules_list,
                },
            ),
        ),
    )

    config_section = "ld_html writer"
    config_section_dependencies = ("writers", "html writers", "html5_polyglot writer")

    def __init__(self):
        html5_polyglot.Writer.__init__(self)
        self.translator_class = LDTranslator


def generatePassword(length=8):
    """Generates a reasonably secure password; 'dashes' are added after every
    third letter for readability.

    The user is able to specify an arbitrary password. However,
    if the user does not provide a password, we generate a random
    one.

    Please recall, that we are "only" protecting exercise solutions
    which will not be graded or otherwise evaluated. It is just meant
    to keep the students from looking them up too easily.
    """
    assert length > 3
    b = batched(
        bytearray(map(lambda i: i % (122 - 97) + 97, get_random_bytes(8))).decode(
            "UTF-8"
        ),
        3,
    )
    m = map(lambda t: "".join(t), b)
    return "-".join(m)


ldPBKDF2IterationCount = 100000


def encryptAESGCM(pwd, plaintext, iterationCount=ldPBKDF2IterationCount):
    # The following encryption scheme is compatible with the one used by LectureDoc2.
    # Additionally, we want to encrypt the content in the same way when we
    # didn't change the content.
    base_hash = hashlib.sha512(plaintext.encode("utf-8")).digest()
    salt = base_hash[:32]  # get_random_bytes(32)
    iv = base_hash[32:44]  # get_random_bytes(12)
    aesKey = PBKDF2(pwd, salt, dkLen=32, count=iterationCount, hmac_hash_module=SHA256)
    cipher = AES.new(aesKey, AES.MODE_GCM, nonce=iv, mac_len=16)
    (ciphertext, tag) = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    return (
        base64.b64encode(str(iterationCount).encode("utf-8")).decode("utf-8")
        + ":"
        + base64.b64encode(salt).decode("utf-8")
        + ":"
        + base64.b64encode(iv).decode("utf-8")
        + ":"
        + base64.b64encode(ciphertext + tag).decode("utf-8")
    )


def make_classes(arguments: list[str]) -> list[str]:
    return [make_id(clazz) for arg in arguments for clazz in arg.split()]


class exercise(container):
    """Represents an exercise.

    Exercise nodes have the additional attribute title if the user provides one.
    """

    pass


# The class is closely modeled after:
# docutils.parsers.rst.directives.admonitions.BaseAdmonition
class Exercise(Directive):
    """
    We are supporting protected exercise solutions in the following way:

    .. exercise:: "title"
        :formatted-title: This is **important**
        :class: complicated

        <exercise content>

        .. solution::
            :pwd: "password"

            <solution content>
    """

    optional_arguments = 1  # the optional title
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        "formatted-title": unchanged_required,
        "name": unchanged_required,
        "class": class_option,
    }

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        exercise_node = exercise(rawsource=text)
        exercise_node.attributes["classes"] = ["ld-exercise"]
        if "class" in self.options:
            exercise_node.attributes["classes"] += self.options["class"]

        if len(self.arguments) > 0:
            exercise_title = self.arguments[0]
            exercise_node.attributes["title"] = exercise_title

            if "formatted-title" in self.options:
                exercise_formatted_title = self.options["formatted-title"]
                textnodes, messages = self.state.inline_text(
                    exercise_formatted_title, self.lineno
                )
                title = nodes.rubric(exercise_title, "", *textnodes)
                title.source, title.line = self.state_machine.get_source_and_line(
                    self.lineno
                )
                title.attributes["classes"] = ["ld-exercise-title"]
                exercise_node += title
                exercise_node += messages
            else:
                title = nodes.rubric(text=exercise_title)
                title.source, title.line = self.state_machine.get_source_and_line(
                    self.lineno
                )
                title.attributes["classes"] = ["ld-exercise-title"]
                exercise_node += title

        self.state.nested_parse(self.content, self.content_offset, exercise_node)
        return [exercise_node]


class solution(
    container
):  # TODO add ",part" to the base class (https://github.com/docutils/docutils/blob/master/docutils/docutils/nodes.py - line 1437)
    # Examples are in `docutils.nodes`
    pass


class Solution(Directive):

    has_content = True
    option_spec = {"pwd": unchanged_required, "class": class_option}

    def run(self):
        # TODO check that solution is the last child element of an exercise
        self.assert_has_content()

        text = "\n".join(self.content)
        node = solution(rawsource=text)

        if "pwd" not in self.options:
            node.attributes["pwd"] = generatePassword()
        elif len(self.options["pwd"]) < 3:
            raise self.error('solution password too short: ":pwd: <password>"')
        else:
            node.attributes["pwd"] = self.options["pwd"]

        node.attributes["classes"] = ["ld-exercise-solution"]
        if "class" in self.options:
            node.attributes["classes"] += self.options["class"]
        if len(self.arguments) > 0:
            node += rubric(text=self.arguments[0])
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class supplemental(container):
    pass


class Supplemental(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        if "supplemental" in self.arguments:
            raise self.error(
                '"supplemental" is superfluous; it is automatically added.'
            )

        text = "\n".join(self.content)
        node = container(rawsource=text)
        node.attributes["classes"] += ["supplemental"]
        node.attributes["classes"] += make_classes(self.arguments)
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class scrollable(container):
    pass


class Scrollable(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {"height": unchanged_required}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        node = scrollable(rawsource=text)
        if "height" in self.options:
            node.attributes["height"] = self.options["height"]
        node.attributes["classes"] += make_classes(self.arguments)
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class module(container):
    pass


class Module(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {"class": class_option}

    def run(self):
        self.assert_has_content()
        if "module" in self.arguments:
            raise self.error('"module" is superfluous; it is automatically added.')
        text = "\n".join(self.content)
        node = module(text, nodes.Text(text))
        node.attributes["classes"] += ["module"] + make_classes(self.arguments)
        if "class" in self.options:
            node.attributes["classes"] += self.options["class"]
        # self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class source(inline):
    pass


class Source(Directive):

    optional_arguments = 1  # the optional file name otherwise the current file
    final_argument_whitespace = False
    has_content = False
    option_spec = {
        "prefix": unchanged_required,
        "suffix": unchanged_required,
        "path": unchanged,
    }

    def run(self):
        text = self.content
        node = source(rawsource=text)

        if "prefix" in self.options:
            node.attributes["prefix"] = self.options["prefix"]
        if "suffix" in self.options:
            node.attributes["suffix"] = self.options["suffix"]

        # it is the name of the specified file or "this" file.
        filename = self.state_machine.document["source"]
        if len(self.arguments) == 0:
            relative_path = filename
        else:
            relative_curdir = os.path.dirname(filename)
            relative_path = relative_curdir + os.sep + self.arguments[0]

        if "path" in self.options:
            match self.options["path"]:
                case "relative":
                    node.attributes["resolved_path"] = relative_path
                case "absolute":
                    node.attributes["resolved_path"] = os.path.abspath(relative_path)
                case _:
                    raise self.error("Unknown path type")
        else:
            node.attributes["resolved_path"] = relative_path

        nodes = [node]
        return nodes


class presenter_note(General, Element):
    pass


class PresenterNote(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {"name": directives.unchanged}

    def run(self):
        self.assert_has_content()
        text = "\n".join(self.content)
        try:
            if self.arguments:
                classes = directives.class_option(self.arguments[0])
            else:
                classes = []
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0])
            )
        node = presenter_note(text)
        node["classes"].extend(classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class LDTranslator(html5_polyglot.HTMLTranslator):

    mathjax_script = '<script type="text/javascript" src="%s"></script>\n'
    """ We need to ensure that MathJax is properly initialized; we will
        call it later to do the typesetting."""

    ld_scripts_and_styles_template = """
    <script src="%(ld_path)s/ld.js" type="module"></script>\n
    <link rel="stylesheet" href="%(ld_path)s/ld.css" />\n
    """

    theme_template = """
    <!-- As of 2024 it is not yet possible to use "layer" with linked stylesheets
         <link rel="stylesheet" href="%(ld_path)s%(theme_path)s" layer="theme" />\n -->
         <style>@import url("%(ld_path)s%(theme_path)s") layer(theme);</style>
    """

    def __init__(self, *args):
        html5_polyglot.HTMLTranslator.__init__(self, *args)

        # Get the settings from the document to make them easily accessible
        self.ld_path = self.document.settings.ld_path
        self.ld_theme_path = self.document.settings.theme
        self.ld_passwords_file = self.document.settings.ld_passwords

        # Overwrite HTMLTranslator's meta tag default
        self.meta = [
            '<meta charset="utf-8">\n',
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0" />\n',
        ]

        # Global definitions that are preprended to the document; i.e., they are
        # added before the template element which contains the document's content.
        self.svg_style = None
        self.svg_defs = None

        self.section_count = 0
        self.card_count = []

        # Identifies the first tag belonging to a slide which should be hidden;
        # i. e., which will not be in the generated output.
        self.start_of_slide_to_hide = None

        # The following attributes are used to handle exercises and solutions
        self.start_of_exercise = None
        self.current_exercise_name = None
        self.start_of_solution = None
        self.exercises_passwords = []
        self.exercises_passwords_titles = {}
        self.exercise_count = 0

        self.master_password = None

        self.start_of_presenter_note = None
        self.presenter_note_count = 0

    def visit_document(self, node):
        super().visit_document(node)
        pass

    def analyze_classes(self, node):
        required_modules = set()
        if hasattr(node, "attributes"):
            for cls in node.attributes["classes"]:
                if cls in self.settings.modules:
                    required_modules.add(self.settings.modules[cls])
        if hasattr(node, "children"):
            for child in node.children:
                required_modules.update(self.analyze_classes(child))
        return required_modules

    def depart_document(self, node):
        ld_path = self.ld_path

        self.stylesheet = [self.ld_scripts_and_styles_template % {"ld_path": ld_path}]
        if self.ld_theme_path is not None:
            self.stylesheet.append(
                self.theme_template
                % {"ld_path": ld_path, "theme_path": "/" + self.ld_theme_path}
            )

        self.meta.append(f'<meta name="version" content="LD2 RENAISSANCE" />\n')

        passwords = []
        if len(self.exercises_passwords) > 0:
            passwords = [{"passwords": self.exercises_passwords}]

        if len(passwords) > 0:
            passwordsJSON = json.dumps(passwords, indent=4)
        else:
            passwordsJSON = "[\n]"

        if self.master_password is not None:
            encryptedPWDs = encryptAESGCM(self.master_password, passwordsJSON, 100000)
            self.meta.append(
                f'<meta name="exercises-passwords" content="{encryptedPWDs}" />\n',
            )

            passwords.insert(0, {"master password": self.master_password})

        if len(passwords) > 0 and self.ld_passwords_file is not None:
            with open(self.ld_passwords_file, "w") as passwordsFile:
                json.dump(passwords, passwordsFile, indent=2, ensure_ascii=False)

        if len(self.exercises_passwords) > 0 and self.ld_passwords_file is not None:
            with open(self.ld_passwords_file + ".md", "w") as passwordsFile:
                for (key,value) in self.exercises_passwords:
                    passwordsFile.write(f"- {key}: \t{value}\n")

        # let's search the DOM for classes that require special treatment
        # by JavaScript libraries, if we find any, we will add links to the
        # necessary JavaScript libraries to the document.

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
                self.head.append(
                    textwrap.dedent(
                        """\
                    <script>
                        window.MathJax = {
                            tex: { tags: 'ams' },
                            chtml: { displayAlign: 'center' /*left or center*/ }
                        };
                    </script>\n"""
                    )
                )
                self.head.extend(self.math_header)
            else:
                self.stylesheet.extend(self.math_header)

        if hasattr(self.settings, "modules"):
            required_modules = self.analyze_classes(node)
            if len(required_modules) > 0:
                self.stylesheet.append(
                    f"\n    <!-- Modules added for specific classes used in the document: -->"
                )
                for module in required_modules:
                    self.stylesheet.append(
                        f'\n    <script src="{module}" type="module"></script>'
                    )

        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        self.fragment.extend(self.body)

        title_slide_classes = node.document["classes"]
        title_slide_id = next(iter(node.ids))

        if self.svg_defs:
            self.body_prefix.append(
                '<svg xmlns="http://www.w3.org/2000/svg" class="svg-global-defs"><defs>'
            )
            self.body_prefix.append(self.svg_defs)
            self.body_prefix.append("</defs></svg>\n")

        if self.svg_style:
            self.body_prefix.append(
                '<svg xmlns="http://www.w3.org/2000/svg" class="svg-global-style"><style>'
            )
            self.body_prefix.append(self.svg_style)
            self.body_prefix.append("</style></svg>\n")

        self.body_prefix.append(self.starttag({}, "template"))
        self.body_suffix.insert(0, "</template>\n")
        slide_tag = "ld-topic"
        self.body_prefix.append(
            self.starttag(
                {"classes": title_slide_classes, "ids": [title_slide_id]}, slide_tag
            )
        )
        if not self.section_count:
            self.body.append("</ld-topic>\n")

        self.html_body.extend(
            self.body_prefix[1:]
            + self.body_pre_docinfo
            + self.docinfo
            + self.body
            + self.body_suffix[:-1]
        )

    def visit_comment(self, node):
        super().visit_comment(node)

    def visit_meta(self, node):
        if node.attributes["name"] == "master-password":
            self.master_password = node.attributes["content"]
        elif node.attributes["name"] == "version":
            self.ld_version = node.attributes["content"]
        elif node.attributes["name"] == "svg-defs":
            self.svg_defs = node.attributes["content"]
        elif node.attributes["name"] == "svg-style":
            self.svg_style = node.attributes["content"]
        else:
            html5_polyglot.HTMLTranslator.visit_meta(self, node)

    def visit_image(self, node):
        if (
            node.attributes["uri"].endswith(".svg")
            and not "icon" in node.attributes["classes"]
        ):
            # SVGs need to be embedded using an object tag to be displayed
            # correctly, when external fonts are referenced in the svg file.
            attributes = {
                "class": " ".join(node.attributes["classes"]),
                "data": node.attributes["uri"],
                "type": "image/svg+xml",
                "role": "img",
            }
            if "align" in node.attributes:
                attributes["class"] += " align-" + node.attributes["align"]
            if "alt" in node.attributes:
                attributes["aria-label"] = node.attributes["alt"]
            if "width" in node.attributes:
                attributes["width"] = node.attributes["width"]
            if "height" in node.attributes:
                attributes["height"] = node.attributes["height"]
            self.body.append(self.starttag(node, "object", **attributes))
        else:
            html5_polyglot.HTMLTranslator.visit_image(self, node)

    def depart_image(self, node):
        if node.attributes["uri"].endswith(".svg"):
            self.body.append("</object>")
        else:
            html5_polyglot.HTMLTranslator.depart_image(self, node)

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
        # The first section ends our title slide!
        if not self.section_count:
            self.body.append("</ld-topic>\n")

        self.section_count += 1
        self.section_level += 1
        if self.section_level > 1:
            # dummy for matching div's
            self.body.append(self.starttag(node, "div", CLASS="section"))
        else:
            if "hide-slide" in node.attributes["classes"]:
                self.start_of_slide_to_hide = len(self.body)
            else:
                self.body.append(self.starttag(node, "ld-topic"))

    def depart_section(self, node):
        self.section_level -= 1
        if self.start_of_slide_to_hide is not None:
            del self.body[self.start_of_slide_to_hide :]
            self.start_of_slide_to_hide = None
        elif self.section_level >= 1:
            self.body.append("</div>\n")
        else:
            self.body.append("</ld-topic>\n")

    def visit_subscript(self, node):
        # self.body.append(self.starttag(node, "sub"))
        self.body.append("<sub>")

    def depart_subscript(self, node):
        self.body.append("</sub>")

    def visit_superscript(self, node):
        self.body.append(self.starttag(node, "sup"))

    def depart_superscript(self, node):
        self.body.append("</sup>")

    def visit_module(self, node):
        self.body.append(
            self.starttag(node, "div")
        )  # , CLASS=" ".join(node.attributes["classes"])))

    def depart_module(self, node):
        self.body.append("</div>")

    def visit_supplemental(self, node):
        self.body.append(
            self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"]))
        )

    def depart_supplemental(self, node):
        self.body.append("</div>")

    def visit_source(self, node):
        source = node.attributes["resolved_path"]
        if "suffix" in node.attributes:
            source = source + node.attributes["suffix"]
        if "prefix" in node.attributes:
            source = node.attributes["prefix"] + source
        self.body.append(f'<a class="reference external" href="{source}">{source}</a>')

    def depart_source(self, node):
        pass

    def visit_scrollable(self, node):
        attributes = {"class": " ".join(node.attributes["classes"])}
        if "height" in node.attributes:
            attributes["data-height"] = node.attributes["height"]
        self.body.append(self.starttag(node, "ld-scrollable", **attributes))

    def depart_scrollable(self, node):
        self.body.append("</ld-scrollable>")

    def visit_presenter_note(self, node):
        self.presenter_note_count += 1

        if self.master_password is None:
            raise Exception("presenter notes require a master password")

        if self.start_of_presenter_note is not None:
            raise Exception(
                "presenter notes cannot be nested"
            )  # TODO move to parsing phase!

        attributes = {
            "class": " ".join(node.attributes["classes"]),
            "data-encrypted": "true",  # ENCRYPTED is a boolean attribute
        }
        self.body.append(self.starttag(node, "ld-presenter-note", **attributes))
        self.start_of_presenter_note = len(self.body)

    def depart_presenter_note(self, node):
        end_of_presenter_note = len(self.body)
        presenter_note_body = "".join(
            self.body[self.start_of_presenter_note : end_of_presenter_note + 1]
        )
        presenter_note_hash = hashlib.sha512(
            presenter_note_body.encode("utf-8")
        ).digest()
        # 2.
        del self.body[self.start_of_presenter_note :]
        self.start_of_presenter_note = None
        # 3.
        pwd = self.master_password.encode("utf-8")
        # We really want a stable salt and iv to avoid that re-running
        # rst2ld changes the output when the password is the same
        # and the content hasn't changed!
        salt = presenter_note_hash[:32]
        iv = presenter_note_hash[32:44]  # get_random_bytes(12)
        aesKey = PBKDF2(
            pwd, salt, dkLen=32, count=ldPBKDF2IterationCount, hmac_hash_module=SHA256
        )
        cipher = AES.new(aesKey, AES.MODE_GCM, nonce=iv, mac_len=16)
        (ciphertext, tag) = cipher.encrypt_and_digest(
            presenter_note_body.encode("utf-8")
        )
        # 4.
        self.body.append(
            base64.b64encode(str(ldPBKDF2IterationCount).encode("utf-8")).decode(
                "utf-8"
            )
        )
        self.body.append(":")
        self.body.append(base64.b64encode(salt).decode("utf-8"))
        self.body.append(":")
        self.body.append(base64.b64encode(iv).decode("utf-8"))
        self.body.append(":")
        self.body.append(base64.b64encode(ciphertext + tag).decode("utf-8"))
        self.body.append("</ld-presenter-note>\n")

    # --------------------------------------------------------------------------
    #
    # Handling of exercises and solutions
    #

    def visit_exercise(self, node):
        if self.start_of_exercise is not None:
            raise Exception("exercises cannot be nested")  # TODO move to parsing phase!

        self.exercise_count += 1
        title = ""
        if "title" in node.attributes:
            title = " - " + node.attributes["title"]
        title = str(self.exercise_count) + title
        self.current_exercise_name = title
        self.start_of_exercise = len(self.body)
        attributes = {
            "class": " ".join(node.attributes["classes"]),
            "ids": ["ld-exercise-" + str(self.exercise_count)],
            "data-exercise-id": str(self.exercise_count),
            "data-exercise-title": title,
        }
        self.body.append(self.starttag(node, "div", **attributes))

    def depart_exercise(self, node):
        self.start_of_exercise = None
        self.current_exercise_name = None
        self.body.append("</div>\n")

    def visit_solution(self, node):
        if self.start_of_exercise is None:
            raise Exception(
                "solutions must be nested in exercises"
            )  # TODO move to parsing phase!
        if self.start_of_solution is not None:
            raise Exception("solutions cannot be nested")  # TODO move to parsing phase!
        if self.current_exercise_name in self.exercises_passwords_titles:
            raise Exception(
                "one exercise can only have one solution"
            )  # TODO move to parsing phase!

        self.exercises_passwords.append(
            (self.current_exercise_name, node.attributes["pwd"])
        )
        self.exercises_passwords_titles[self.current_exercise_name] = node.attributes[
            "pwd"
        ]
        attributes = {
            "class": " ".join(node.attributes["classes"]),
            "data-encrypted": "true",  # ENCRYPTED is a boolean attribute
        }
        self.body.append(self.starttag(node, "div", **attributes))
        self.start_of_solution = len(self.body)

    def depart_solution(self, node):
        # Idea:
        # 1. Extract the solution
        # 2. Remove the "generated HTML of the solution" from the body
        # 3. Encrypt the solution using AES-GCM
        # 4. Add the encrypted solution to the body (base64 encoded)

        # 1.
        end_of_solution = len(self.body)
        solution_body = "".join(self.body[self.start_of_solution : end_of_solution + 1])
        solution_hash = hashlib.sha512(solution_body.encode("utf-8")).digest()
        # 2.
        del self.body[self.start_of_solution :]
        self.start_of_solution = None
        # 3.
        pwd = node.attributes["pwd"].encode("utf-8")
        # We really want a stable salt and iv to avoid that re-running
        # rst2ld changes the output when the password is the same
        # and the content hasn't changed!
        salt = solution_hash[:32]
        iv = solution_hash[32:44]  # get_random_bytes(12)
        aesKey = PBKDF2(
            pwd, salt, dkLen=32, count=ldPBKDF2IterationCount, hmac_hash_module=SHA256
        )
        cipher = AES.new(aesKey, AES.MODE_GCM, nonce=iv, mac_len=16)
        (ciphertext, tag) = cipher.encrypt_and_digest(solution_body.encode("utf-8"))
        # 4.
        self.body.append(
            base64.b64encode(str(ldPBKDF2IterationCount).encode("utf-8")).decode(
                "utf-8"
            )
        )
        self.body.append(":")
        self.body.append(base64.b64encode(salt).decode("utf-8"))
        self.body.append(":")
        self.body.append(base64.b64encode(iv).decode("utf-8"))
        self.body.append(":")
        self.body.append(base64.b64encode(ciphertext + tag).decode("utf-8"))
        self.body.append("</div>\n")


#
# Convenience directives which are "simple" shortcuts for containers with
# respective classes:
directives.register_directive("module", Module)

directives.register_directive("supplemental", Supplemental)

directives.register_directive("presenter-note", PresenterNote)

directives.register_directive("scrollable", Scrollable)

#
# Advanced directives which are (optionally) parametrized
directives.register_directive("exercise", Exercise)
directives.register_directive("solution", Solution)

directives.register_directive("source", Source)


# Imported for the "side effects" of registering the directives
import lddocutils.ldwriter.lddirectives.admonitions
import lddocutils.ldwriter.lddirectives.decks
import lddocutils.ldwriter.lddirectives.grids
import lddocutils.ldwriter.lddirectives.stories
