"""
Constants and functions shared between modules.
"""
from typing import Dict

from docutils.parsers.rst import directives  # type: ignore
from docutils.parsers.rst import Directive

EXISTING_DIRS = directives._directives  # pylint: disable=protected-access
EXISTING_DIRECTIVES: Dict[str, Directive] = EXISTING_DIRS

# This is hardcoded in doc8 as a valid option so be wary that changing this
# may break doc8 linting.
# See https://github.com/PyCQA/doc8/pull/34.
SUBSTITUTION_OPTION_NAME = 'substitutions'
