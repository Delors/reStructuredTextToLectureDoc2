from itertools import batched
import json

from docutils import nodes
from docutils import frontend
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives import unchanged_required, class_option, unchanged
from docutils.nodes import inline, container, title, rubric
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

def validate_ld_modules_list(setting, value=None, option_parser=None,
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
                "Configures class-based modules.",
                ["--ld-modules"],
                {'metavar': '<class_name dir[,class_name dir,...]>',
                 'validator': validate_ld_modules_list},
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

    Exercise node have the additional attribute title if the user provides one.
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
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


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
        if "layer" in self.arguments:
            raise self.error('"layer" is superfluous; it is automatically added.')

        text = "\n".join(self.content)
        node = layer(rawsource=text)
        node.attributes["classes"] += ["layer"] + self.arguments
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


# OBSOLETE
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
    optional_arguments = 0
    has_content = False
    option_spec = {"prefix": unchanged_required, "suffix": unchanged_required, "path": unchanged}

    def run(self):
        text = "File"
        node = source(rawsource=text)
        if "prefix" in self.options:
            node.attributes["prefix"] = self.options["prefix"]
        if "suffix" in self.options:
            node.attributes["suffix"] = self.options["suffix"]
        if "path" in self.options:
            match self.options["path"]:
                case "file":
                    # nothing to do here; default case
                    pass
                case "dir":
                    node.attributes["path"] = "dir"
                case _ :
                    raise self.error("Unknown path type")
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

    mathjax_script = '<script type="text/javascript" src="%s"></script>\n'
    """ We need to ensure that MathJax is properly initialized; we will 
       call it later to do the typesetting."""

    # ld_stylesheet_normalize = """<link rel="stylesheet" href="%(ld_path)s/normalize.css" />\n"""
    ld_stylesheet_normalize = """<style>@import url("%(ld_path)s/normalize.css") layer(normalize); </style>\n"""

    # NOW MODULARIZED:  <script src="%(ld_path)s/ld-crypto.js" type="text/javascript"></script>
    #                   <script src="%(ld_path)s/ld-lib.js" type="text/javascript"></script>
    # NOW A SIMPLE HTML FRAGMENT:
    #                   <script src="%(ld_path)s/ld-help.js" type="text/javascript"></script>
    ld_stylesheet_template = """
    <script src="%(ld_path)s/ld-core.js" type="module"></script>\n
    <script src="%(ld_path)s/ld-components.js" type="module"></script>\n
    <!-- Additional scripts that interact with LectureDoc have to be added below. -->
    <link rel="stylesheet" href="%(ld_path)s/ld.css" type="text/css" />\n
    <link rel="stylesheet" href="%(ld_path)s/themes/DHBW/theme.css" type="text/css" />\n
    <!-- When we make better use of HTML Components for LectureDoc's UI we can remove the following line -->
    <link rel="stylesheet" href="%(ld_path)s/ld-ui.css" type="text/css" />\n
    """


    embedded_stylesheet = '<style>@layer docutils { \n\n%s\n}</style>\n'
    """ We overwrite how the embedded stylesheet is inserted into the document 
        to assign it an appropriate CSS layer. This facilitates redefining the
        styles by later defined layers; otherwise the styles would be added
        to the unnamed layer which takes precedence over all other layers and
        therefore cannot be overridden by styles defined in normal layers.
    """

    
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
        # self.stylesheet.insert(0, self.ld_stylesheet_normalize % {"ld_path": ld_path+"/css"})
        # self.stylesheet.append(self.ld_stylesheet_template % {"ld_path": ld_path})
        self.stylesheet = [self.ld_stylesheet_template % {"ld_path": ld_path}]
        self.meta = [
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0, user-scalable=no" />\n'
        ]
        self.meta.append(
            '<meta http-equiv="Content-Type" ' 'content="text/html; charset=utf-8">\n'
        )
        self.meta.append('<meta name="version" content="LD2 0.1" />\n')

        self.section_count = 0

        # Identifies the first tag belonging to the slide to hide.
        # This is used to remove the slide from the output.
        self.start_of_slide_to_hide = None

        self.ld_exercises_passwords_file = self.document.settings.ld_exercises_passwords
        self.start_of_exercise = None  # used while parsing an exercise
        self.current_exercise_name = None  # used while parsing an exercise
        self.start_of_solution = None
        self.exercises_master_password = None
        self.exercises_passwords = []
        self.exercises_passwords_titles = {}
        self.exercise_count = 0  # incremented for each exercise

    def visit_document(self, node):
        #self.embedded_stylesheet = '<style>@layer docutils { \n\n%s\n}</style>\n'
        super().visit_document(node);
        pass;

    def analyze_classes(self,node):
        required_ld_modules = set()
        if hasattr(node, "attributes"):
            for cls in node.attributes["classes"]:
                if cls in self.settings.ld_modules:
                    required_ld_modules.add(self.settings.ld_modules[cls])
        if hasattr(node, "children"):
            for child in node.children:
                required_ld_modules.update(self.analyze_classes(child))
        return required_ld_modules

    def depart_document(self, node):
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
                self.head.extend(self.math_header)
            else:
                self.stylesheet.extend(self.math_header)

        if hasattr(self.settings, "ld_modules"):
            required_ld_modules = self.analyze_classes(node)
            for module in required_ld_modules:
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

        if len(self.exercises_passwords) > 0:
            # Write all passwords to the HTML document and (optionally) to a file
            # if self.exercises_master_password is None:
            #    self.exercises_master_password = generatePassword(10)

            pwds = [{"passwords": self.exercises_passwords}]
            if self.exercises_master_password is not None:
                pwds.insert(0,{"master password": self.exercises_master_password})

            pwdsJSON = json.dumps(pwds, indent=4)

            if self.exercises_master_password is not None:
                encryptedPWDs = encryptAESGCM(
                    self.exercises_master_password, pwdsJSON, 100000
                )
                self.head.insert(
                    0,
                    f'<meta name="exercises-passwords" content="{encryptedPWDs}" />\n',
                )

            if self.ld_exercises_passwords_file is not None:
                with open(self.ld_exercises_passwords_file, "w") as pwdsFile:
                    pwdsFile.write(pwdsJSON)

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
        else:
            html5_polyglot.HTMLTranslator.visit_meta(self, node)

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
        source = self.document["source"]
        if "path" in node.attributes and node.attributes["path"] == "dir":
            source = os.path.dirname(source)            
        if "suffix" in node.attributes:
            source = source + node.attributes["suffix"]
        if "prefix" in node.attributes:
            source = node.attributes["prefix"] + source
            self.body.append(f'<a class="reference external" href="{source}">{source}</a>')
        else: 
            self.body.append(source)

    def depart_source(self, node):
        pass


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
directives.register_directive("stack", Stack)
directives.register_directive("layer", Layer)


directives.register_directive("module", Module)

directives.register_directive("incremental", Incremental)
directives.register_directive("supplemental", Supplemental)

directives.register_directive("presenter-notes", PresenterNotes)

#
# Advanced directives which are (optionally) parametrized
directives.register_directive("exercise", Exercise)
directives.register_directive("solution", Solution)

directives.register_directive("source", Source)
