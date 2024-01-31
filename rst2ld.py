#!/usr/bin/env python3

# Author: Michael Eichberg (mail@michael-eichberg.de)
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML slides using LectureDoc 2.
"""

from docutils.writers import html5_polyglot

from docutils.core import publish_cmdline, default_description
from lddocutils.ldwriter import Writer

DESCRIPTION = ('Generates LectureDoc HTML documents from standalone '
               'reStructuredText sources.  ' + default_description)

publish_cmdline(writer=Writer(), writer_name='html', description=DESCRIPTION)


