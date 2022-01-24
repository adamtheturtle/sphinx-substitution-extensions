"""
Custom Sphinx extensions.
"""

from __future__ import annotations

import logging
from typing import Dict, Tuple

from docutils.nodes import Node, system_message

# See https://github.com/python/typeshed/issues/5755
from docutils.parsers.rst import directives  # type: ignore
from docutils.parsers.rst.roles import code_role
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock

from sphinx_substitution_extensions.shared import (
    EXISTING_DIRECTIVES,
    SUBSTITUTION_OPTION_NAME,
)

LOGGER = logging.getLogger(__name__)


class SubstitutionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    option_spec = CodeBlock.option_spec
    option_spec['substitutions'] = directives.flag

    def run(self) -> list:
        """
        Replace placeholders with given variables.
        """
        self.option_spec['substitutions'] = directives.flag

        new_content = []
        self.content = self.content  # type: list[str]
        existing_content = self.content
        substitution_defs = self.state.document.substitution_defs
        for item in existing_content:
            for name, value in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    replacement = value.astext()
                    item = item.replace(f'|{name}|', replacement)
            new_content.append(item)

        self.content = new_content
        return list(super().run())


def _exists_dependency(
    name: str,
) -> bool:
    """
    Returns true if the dependency is installed.
    """
    try:
        __import__(name)
    except ImportError:
        return False
    return True


def substitution_code_role(  # pylint: disable=dangerous-default-value
    typ: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Dict = {},
    content: list[str] = [],
) -> Tuple[list[Node], list[system_message]]:
    """
    Replace placeholders with given variables.
    """
    document = inliner.document  # type: ignore
    for name, value in document.substitution_defs.items():
        replacement = value.astext()
        text = text.replace(f'|{name}|', replacement)
        rawtext = text.replace(f'|{name}|', replacement)
        rawtext = rawtext.replace(name, replacement)

    result_nodes, system_messages = code_role(
        role=typ,
        rawtext=rawtext,
        text=text,
        lineno=lineno,
        inliner=inliner,
        options=options,
        content=content,
    )

    return result_nodes, system_messages


substitution_code_role.options = {  # type: ignore
    'class': directives.class_option,
    'language': directives.unchanged,
}

if _exists_dependency('sphinx-prompt') and 'prompt' not in EXISTING_DIRECTIVES:
    MESSAGE = (
        'sphinx-prompt must be in the conf.py extensions list before '
        'sphinx_substitution_extensions'
    )
    LOGGER.warning(MESSAGE)


def setup(app: Sphinx) -> dict:
    """
    Add the custom directives to Sphinx.
    """
    # pylint: disable=import-outside-toplevel
    app.add_config_value('substitutions', [], 'html')
    directives.register_directive('code-block', SubstitutionCodeBlock)
    if 'prompt' in EXISTING_DIRECTIVES:

        from sphinx_substitution_extensions.extras import SubstitutionPrompt

        directives.register_directive('prompt', SubstitutionPrompt)
    app.add_role('substitution-code', substitution_code_role)
    return {'parallel_read_safe': True}
