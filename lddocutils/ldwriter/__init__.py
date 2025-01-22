from itertools import batched
import json
import textwrap

from docutils import nodes, frontend
from docutils.nodes import General, Element, inline, container, title, rubric
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

import lddocutils.ldwriter.admonitions
import lddocutils.ldwriter.exercises

"""
Writer for LectureDoc2 HTML output.

This Writer is heavily inspired by the rst2s5 writer:
https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/s5_html/__init__.py

# Examples definitions of `nodes` are in `docutils.nodes`
"""

def validate_modules_list(setting, value=None, option_parser=None,
                         config_parser=None, config_section=None):
    module_configurations = frontend.validate_comma_separated_list(setting, value, option_parser,config_parser,config_section)
    modules = dict(map(lambda tc: tc.split(sep=" ",maxsplit=1) , module_configurations))

    return modules


class Writer(html5_polyglot.Writer):

    supported = ("html", "xhtml")
    """Formats this writer supports."""

    settings_spec = html5_polyglot.Writer.settings_spec + (
        "LectureDoc2 Specific Options",
        "Configuration options used when generating LectureDoc2 lecture notes.",
        (
             (
                "Specifies the default version of LectureDoc2 that is to be used.",
                ["--ld-default-version"],
                {"choices": ["genesis","renaissance"], "default": "genesis"},
            ),
            (
                "Specifies the path to LectureDoc2.",
                ["--ld-path"],
                {"metavar": "<URL>", "default": "ld"},
            ),
            (
                "File in which the exercises' passwords are stored.",
                ["--ld-exercises-passwords"],
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
                {'metavar': '<class_name dir[,class_name dir,...]>',
                 'validator': validate_modules_list},
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


class exercise(container):
    """Represents an exercise.

    Exercise nodes have the additional attribute title if the user provides one.
    """

    pass


class Exercise(Directive):
    """
    We are supporting protected exercise solutions in the following way:

    .. exercise:: "title"
        :class: complicated

        <exercise content>

        .. solution::
            :pwd: "password"

            <solution content>
    """

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
        node.attributes["classes"] = ["ld-exercise"] 
        if "class" in self.options:
            node.attributes["classes"] += self.options["class"]
        if len(self.arguments) > 0:
            exercise_title = self.arguments[0]
            node.attributes["title"] = exercise_title
            node += rubric(text=exercise_title)
            # exercise_rubric = rubric(rawsource=exercise_title)
            # self.state.nested_parse(exercise_title, self.content_offset, exercise_rubric)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class solution(container): # TODO add ",part" to the base class (https://github.com/docutils/docutils/blob/master/docutils/docutils/nodes.py - line 1437)
    # Examples are in `docutils.nodes`
    pass


class Solution(Directive):
    # Examples are in docutils.parsers.rst.directives.*

    required_arguments = 0
    optional_arguments = 0
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
            raise self.error('"stack" is superfluous; it is automatically added.')
        node.attributes["classes"] += ["stack"] + self.arguments 
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class layer(container):
    pass


class Layer(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        if "layer" in self.arguments:
            raise self.error('"layer" is superfluous; it is automatically added.')

        text = "\n".join(self.content)
        node = layer(rawsource=text)
        node.attributes["classes"] += ["layer"] + self.arguments
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class deck(container):
    pass


class Deck(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
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

    required_arguments = 0
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
        node = stack(rawsource=text)
        node.attributes["classes"] += ["supplemental"] + self.arguments
        self.state.nested_parse(self.content, self.content_offset, node)
        nodes = [node]
        return nodes


class incremental(container):
    pass


class Incremental(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        if "incremental" in self.arguments:
            raise self.error(
                '"incremental" is superfluous; it is automatically added.'
            )

        text = "\n".join(self.content)
        node = incremental(rawsource=text)
        
        node.attributes["classes"] += ["incremental"] + self.arguments
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
            raise self.error(
                '"module" is superfluous; it is automatically added.'
            )
        text = "\n".join(self.content)
        node = module(text,nodes.Text(text))
        node.attributes["classes"] += ["module"] + self.arguments
        if "class" in self.options:
            node.attributes["classes"] += self.options["class"]
        # self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class source(inline):
    pass


class Source(Directive):

    required_arguments = 0
    final_argument_whitespace = False
    optional_arguments = 1
    has_content = False
    option_spec = {"prefix": unchanged_required, "suffix": unchanged_required, "path": unchanged}

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
                case _ :
                    raise self.error("Unknown path type")
        else:
            node.attributes["resolved_path"] = relative_path
        
        nodes = [node]
        return nodes

class presenter_note(General, Element): pass

class PresenterNote(Directive):

    required_arguments = 0
    final_argument_whitespace = True
    optional_arguments = 1
    has_content = True
    option_spec = {'name': directives.unchanged}

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        try:
            if self.arguments:
                classes = directives.class_option(self.arguments[0])
            else:
                classes = []
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        node = presenter_note(text)
        node['classes'].extend(classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class LDTranslator(html5_polyglot.HTMLTranslator):

    mathjax_script = '<script type="text/javascript" src="%s"></script>\n'
    """ We need to ensure that MathJax is properly initialized; we will 
        call it later to do the typesetting."""

    ld_scripts_and_styles_template_genesis = """
    <script src="%(ld_path)s/ld-core.js" type="module"></script>\n
    <script src="%(ld_path)s/ld-components.js" type="module"></script>\n
    <link rel="stylesheet" href="%(ld_path)s/ld.css" />\n
    <link rel="stylesheet" href="%(ld_path)s/themes/DHBW/theme.css" />\n
    <link rel="stylesheet" href="%(ld_path)s/ld-ui.css" />\n
    """

    ld_scripts_and_styles_template_renaissance = """
    <script src="%(ld_path)s/ld.js" type="module"></script>\n
    <link rel="stylesheet" href="%(ld_path)s/ld.css" />\n
    """

    theme_template_renaissance = """
    <!-- As of 2024 it is not yet possible to use "layer" with linked stylesheets 
         <link rel="stylesheet" href="%(ld_path)s%(theme_path)s" layer="theme" />\n -->
         <style>@import url("%(ld_path)s%(theme_path)s") layer(theme)</style>
    """

    def __init__(self, *args):
        html5_polyglot.HTMLTranslator.__init__(self, *args)

        # Get the settings from the document to make them easily accessible
        self.ld_path = self.document.settings.ld_path
        self.ld_version = self.document.settings.ld_default_version
        self.ld_theme_path = self.document.settings.theme
        self.ld_exercises_passwords_file = self.document.settings.ld_exercises_passwords

        # Overwrite HTMLTranslator's meta tag default
        self.meta = [
            '<meta charset="utf-8">\n',
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0" />\n'
        ]

        self.section_count = 0
        self.card_count = []

        # Identifies the first tag belonging to a slide which should be hidden;
        # i. e., which will not be in the generated output.
        self.start_of_slide_to_hide = None

        # The following attributes are used to handle exercises and solutions
        self.start_of_exercise = None  
        self.current_exercise_name = None  
        self.start_of_solution = None
        self.exercises_master_password = None
        self.exercises_passwords = []
        self.exercises_passwords_titles = {}
        self.exercise_count = 0  

    def visit_document(self, node):
        super().visit_document(node);
        pass;

    def analyze_classes(self,node):
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
        ld_path = self.ld_path + "/" + self.ld_version 

        if self.ld_version == "genesis":
            self.stylesheet = [self.ld_scripts_and_styles_template_genesis % {"ld_path": ld_path}]
        elif self.ld_version == "renaissance":
            self.stylesheet = [self.ld_scripts_and_styles_template_renaissance % {"ld_path": ld_path}]
            if self.ld_theme_path is not None:
                self.stylesheet.append(self.theme_template_renaissance % {"ld_path": ld_path, "theme_path": "/" + self.ld_theme_path})
        else: 
            raise Exception("Unknown LectureDoc2 version: " + self.ld_version)

        self.meta.append(f'<meta name="version" content="LD2 {self.ld_version.upper()}" />\n')

        if len(self.exercises_passwords) > 0:
            # Write all passwords to the HTML document and (optionally) to a file
            # if self.exercises_master_password is None:
            #    self.exercises_master_password = generatePassword(10)

            passwords = [{"passwords": self.exercises_passwords}]
            if self.exercises_master_password is not None:
                passwords.insert(0,{"master password": self.exercises_master_password})

            passwordsJSON = json.dumps(passwords, indent=4)

            if self.exercises_master_password is not None:
                encryptedPWDs = encryptAESGCM(
                    self.exercises_master_password, passwordsJSON, 100000
                )
                self.meta.append(
                    f'<meta name="exercises-passwords" content="{encryptedPWDs}" />\n',
                )

            if self.ld_exercises_passwords_file is not None:
                with open(self.ld_exercises_passwords_file, "w") as passwordsFile:
                    passwordsFile.write(passwordsJSON)

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
                self.head.append(textwrap.dedent("""\
                    <script>
                        window.MathJax = {
                            tex: { tags: 'ams', },
                            chtml: { displayAlign: 'center' /*left or center*/ }
                        };
                    </script>\n"""))
                self.head.extend(self.math_header)
            else:
                self.stylesheet.extend(self.math_header)

        if hasattr(self.settings, "modules"):
            required_modules = self.analyze_classes(node)
            if len(required_modules) > 0:
                self.stylesheet.append(
                        f'\n    <!-- Modules added for specific classes used in the document: -->'
                    )
                for module in required_modules:
                    self.stylesheet.append(
                        f'\n    <script src="{module}" type="module"></script>'
                    )

        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        self.fragment.extend(self.body)

        title_slide_classes = node.document["classes"] + ["ld-slide"]
        title_slide_id = next(iter(node.ids))
        self.body_prefix.append(
            self.starttag({}, "template")
        ) 
        self.body_suffix.insert(0,"</template>\n");
        self.body_prefix.append(
            self.starttag({"classes": title_slide_classes, "ids": [title_slide_id] }, "div")
        )
        if not self.section_count:
            self.body.append("</div>\n")

        self.html_body.extend(
            self.body_prefix[1:]
            + self.body_pre_docinfo
            + self.docinfo
            + self.body
            + self.body_suffix[:-1]
        )

    def visit_meta(self, node):
        if node.attributes["name"] == "exercises-master-password":
            self.exercises_master_password = node.attributes["content"]
        elif node.attributes["name"] == "version":
            self.ld_version = node.attributes["content"]
        else:
            html5_polyglot.HTMLTranslator.visit_meta(self, node)

    def visit_image(self, node):
        if node.attributes["uri"].endswith(".svg"):
            # SVGs need to be embedded using an object tag to be displayed
            # correctly, when external fonts are referenced in the svg file.
            # TODO Handle "alts"
            attributes = {
                "class": " ".join(node.attributes["classes"]),
                "data": node.attributes["uri"],
                "type": "image/svg+xml",
                "role": "img",
            }
            if "align" in node.attributes:
                attributes["class"] += " align-"+node.attributes["align"]
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
        if(node.attributes["uri"].endswith(".svg")):
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
            self.body.append("</div>\n")

        self.section_count += 1
        self.section_level += 1
        if self.section_level > 1:
            # dummy for matching div's
            self.body.append(self.starttag(node, "div", CLASS="section"))
        else:
            if "hide-slide" in node.attributes["classes"]:
                self.start_of_slide_to_hide = len(self.body)
            else:
                self.body.append(self.starttag(node, "div", CLASS="ld-slide"))

    def depart_section(self, node):
        self.section_level -= 1
        if self.start_of_slide_to_hide is not None:
            del self.body[self.start_of_slide_to_hide :]
            self.start_of_slide_to_hide = None
        else:
            self.body.append("</div>")


    def visit_question(self, node):
        self.body.append(self.starttag(node, "ld-question", CLASS=" ".join(node.attributes["classes"])))
    
    def depart_question(self, node):
        self.body.append("</ld-question>")
    
    def visit_answer(self, node):
        self.body.append(self.starttag(node, "ld-answer", CLASS=" ".join(node.attributes["classes"])))

    def depart_answer(self, node):
        self.body.append("</ld-answer>")

    def visit_subscript(self, node):
        self.body.append(self.starttag(node, "sub"))

    def depart_subscript(self, node):
        self.body.append("</sub>")

    def visit_superscript(self, node):
        self.body.append(self.starttag(node, "sup"))

    def depart_superscript(self, node):
        self.body.append("</sup>")

    def visit_stack(self, node):
        self.body.append(self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"])))

    def depart_stack(self, node):
        self.body.append("</div>")

    def visit_layer(self, node):
        self.body.append(self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"])))

    def depart_layer(self, node):
        self.body.append("</div>")

    def visit_deck(self, node):
        self.card_count.append(0)
        self.body.append(self.starttag(node, "ld-deck", CLASS=" ".join(node.attributes["classes"])))

    def depart_deck(self, node):
        self.card_count.pop()
        self.body.append("</ld-deck>")

    def visit_card(self, node):
        if (len(self.card_count) == 0):
            raise Exception("card directive must be nested in a deck directive")
        card_id = self.card_count.pop()
        if(card_id > 0):
            node.attributes["classes"] += ["incremental"]
        self.card_count.append(card_id + 1)
        self.body.append(self.starttag(node, "ld-card", CLASS=" ".join(node.attributes["classes"])))

    def depart_card(self, node):
        self.body.append("</ld-card>")

    def visit_incremental(self, node):
        self.body.append(self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"])))

    def depart_incremental(self, node):
        self.body.append("</div>")

    def visit_module(self, node):
        self.body.append(self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"])))

    def depart_module(self, node):
        self.body.append("</div>")

    def visit_supplemental(self, node):
        self.body.append(self.starttag(node, "div", CLASS=" ".join(node.attributes["classes"])))

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

    def visit_presenter_note(self, node):
        self.body.append(self.starttag(node, "ld-presenter-note", CLASS=" ".join(node.attributes["classes"])))

    def depart_presenter_note(self, node):
        self.body.append("</ld-presenter-note>")

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
directives.register_directive("stack", Stack) # [DEPRECATED] GENESIS
directives.register_directive("layer", Layer) # [DEPRECATED] GENESIS
directives.register_directive("deck", Deck) # RENAISSANCE
directives.register_directive("card", Card) # RENAISSANCE

directives.register_directive("module", Module)

directives.register_directive("incremental", Incremental)
directives.register_directive("supplemental", Supplemental)

directives.register_directive("presenter-note", PresenterNote)

#
# Advanced directives which are (optionally) parametrized
directives.register_directive("exercise", Exercise)
directives.register_directive("solution", Solution)

directives.register_directive("source", Source)
