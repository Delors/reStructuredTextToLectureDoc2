
from docutils import frontend, nodes, utils
from docutils.writers import html5_polyglot

from sys import stderr

"""

This Writer is heavily inspired by the rst2s5 writer:
https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/s5_html/__init__.py
"""

class Writer(html5_polyglot.Writer):

    supported = ('html', 'xhtml')
    """Formats this writer supports."""

    settings_spec = html5_polyglot.Writer.settings_spec + (
        'LectureDoc2 Specific Options',
        'Configuration options used when generating LectureDoc2 lecture notes.',
        (('Specifies the path to LectureDoc2.',
          ['--ld-path'],
          {'metavar': '<URL>', 'default':'ld'}),))
           

    config_section = 'ld_html writer'
    config_section_dependencies = ('writers', 'html writers',
                                   'html5_polyglot writer')
    def __init__(self):
        html5_polyglot.Writer.__init__(self)
        self.translator_class = LDTranslator


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
        self.stylesheet.insert(0,self.ld_stylesheet_normalize % {'ld_path' : ld_path})
        self.stylesheet.append(self.ld_stylesheet_template % {'ld_path': ld_path})
        self.meta = ['<meta name="viewport" '
                         'content="width=device-width, initial-scale=1.0, user-scalable=no" />\n']
        self.meta.append('<meta http-equiv="Content-Type" '
                            'content="text/html; charset=utf-8">\n')
        self.meta.append('<meta name="version" content="LD2 0.1" />\n')

        self.section_count = 0


    def depart_document(self, node):
        self.head_prefix.extend([self.doctype,
                                 self.head_prefix_template %
                                 {'lang': self.settings.language_code}])
        self.html_prolog.append(self.doctype)
        self.head = self.meta[:] + self.head
        if self.math_header:
            if self.math_output == 'mathjax':
                self.head.extend(self.math_header)
            else:
                self.stylesheet.extend(self.math_header)
        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        self.fragment.extend(self.body)
        #title = ''.join(self.html_title).replace('<h1 class="title">', '<h1>')
        #layout = self.layout_template % {'header': header,
        #                                 'title': title,
        #                                 'footer': footer}
        # self.body_prefix.extend(layout)
        # self.body_prefix.append('<main>\n')
        all_classes = node.document['classes']
        all_classes.append('ld-slide')
        self.body_prefix.append(
            self.starttag({'classes': all_classes, 'ids': ['slide0']}, 'div'))
        if not self.section_count:
            self.body.append('</div>\n')
        
        # self.body_suffix.insert(0, '</main>\n')
        self.html_body.extend(self.body_prefix[1:] + self.body_pre_docinfo
                              + self.docinfo + self.body
                              + self.body_suffix[:-1])


    def visit_section(self, node):
        if not self.section_count:
            self.body.append('</div>\n')
        self.section_count += 1
        self.section_level += 1
        if self.section_level > 1:
            # dummy for matching div's
            self.body.append(self.starttag(node, 'div', CLASS='section'))
        else:
            self.body.append(self.starttag(node, 'div', CLASS='ld-slide'))

    def visit_subscript(self, node):
        self.body.append(self.starttag(node, 'sub'))
        
    def depart_subscript(self, node):
        self.body.append('</sub>')

    def visit_superscript(self, node):
        self.body.append(self.starttag(node, 'sup'))
        
    def depart_superscript(self, node):
        self.body.append('</sup>')

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</div>')

    def visit_subtitle(self, node):
        if isinstance(node.parent, nodes.section):
            level = self.section_level + self.initial_header_level - 1
            if level == 1:
                level = 2
            tag = 'h%s' % level
            self.body.append(self.starttag(node, tag, ''))
            self.context.append('</%s>\n' % tag)
        else:
            html5_polyglot.HTMLTranslator.visit_subtitle(self, node)


    def visit_title(self, node):
        html5_polyglot.HTMLTranslator.visit_title(self, node)