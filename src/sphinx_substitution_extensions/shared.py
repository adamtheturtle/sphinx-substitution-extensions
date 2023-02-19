"""
Constants and functions shared between modules.
"""

from docutils.parsers.rst import Directive, directives

EXISTING_DIRS = directives._directives  # noqa: SLF001
EXISTING_DIRECTIVES: dict[str, Directive] = EXISTING_DIRS

# This is hardcoded in doc8 as a valid option so be wary that changing this
# may break doc8 linting.
# See https://github.com/PyCQA/doc8/pull/34.
SUBSTITUTION_OPTION_NAME = "substitutions"
