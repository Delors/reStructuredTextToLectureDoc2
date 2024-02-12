reStructuredText to LectureDoc\ :math:`^2` (``rst2ld``)
========================================================

`rst2ld` enables the conversion of lecture slides authored in `reStructuredText <https://docutils.sourceforge.io/rst.html>`__ to `LectureDoc2 <https://github.com/Delors/LectureDoc2>`__ format.


Setup a Project
----------------------

1. create a directory in which you want to store your slides; e.g., ``mkdir slides``
2. change to the director: ``cd slides``
3. initialize git: ``git init``
4. add LectureDoc2 and restructuredTextToLectureDoc2 projects to the folder
  - ``git submodule add https://github.com/delors/LectureDoc2``
  - ``git submodule add https://github.com/delors/reStructuredTextToLectureDoc2``
 
Optional
________
5. add script to generate slides (https://github.com/Delors/Lectures/blob/main/gen-slides.zsh)
6. add "docutils.conf" when necessary (https://github.com/Delors/Lectures/blob/main/docutils.conf)
7. add .gitignore file with "*.rst.html" if you don't want to archive the generated web pages