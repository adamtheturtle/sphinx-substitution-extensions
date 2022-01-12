from typing import Dict

from docutils.parsers.rst import directives  # type: ignore
from docutils.parsers.rst import Directive
from sphinx.directives.code import CodeBlock

_EXISTING_DIRS = directives._directives  # pylint: disable=protected-access
_EXISTING_DIRECTIVES: Dict[str, Directive] = _EXISTING_DIRS
_EXISTING_CODE_BLOCK_DIRECTIVE = CodeBlock

# This is hardcoded in doc8 as a valid option so be wary that changing this
# may break doc8 linting.
# See https://github.com/PyCQA/doc8/pull/34.
_SUBSTITUTION_OPTION_NAME = 'substitutions'
