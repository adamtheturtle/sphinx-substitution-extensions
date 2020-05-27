"""
Custom Sphinx extensions.
"""

import logging
from typing import Dict, List, Tuple

from docutils.nodes import Node, system_message
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import code_role
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx

LOGGER = logging.getLogger(__name__)

_EXISTING_DIRS = directives._directives  # pylint: disable=protected-access
_EXISTING_DIRECTIVES: Dict[str, Directive] = _EXISTING_DIRS
_EXISTING_CODE_BLOCK_DIRECTIVE = _EXISTING_DIRECTIVES['code-block']

if 'prompt' not in _EXISTING_DIRECTIVES:
    MESSAGE = (
        'sphinx-prompt must be in the conf.py extensions list before '
        'sphinx_substitution_extensions'
    )
    LOGGER.error(MESSAGE)

_EXISTING_PROMPT_DIRECTIVE: Directive = _EXISTING_DIRECTIVES['prompt']


class SubstitutionCodeBlock(_EXISTING_CODE_BLOCK_DIRECTIVE):  # type: ignore
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    option_spec = _EXISTING_CODE_BLOCK_DIRECTIVE.option_spec
    option_spec['substitutions'] = directives.flag

    def run(self) -> List:
        """
        Replace placeholders with given variables.
        """
        self.option_spec['substitutions'] = directives.flag

        new_content = []
        self.content = (  # pylint: disable=attribute-defined-outside-init
            self.content
        )  # type: List[str]
        existing_content = self.content
        substitution_defs = self.state.document.substitution_defs
        for item in existing_content:
            for name in self.state.document.substitution_names:
                if 'substitutions' in self.options:
                    replacement = substitution_defs[name].astext()
                    item = item.replace(
                        '|{original}|'.format(original=name),
                        replacement,
                    )
            new_content.append(item)

        self.content = (  # pylint: disable=attribute-defined-outside-init
            new_content
        )
        return list(super().run())


class SubstitutionPrompt(_EXISTING_PROMPT_DIRECTIVE):  # type: ignore
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    option_spec = _EXISTING_PROMPT_DIRECTIVE.option_spec or {}
    option_spec['substitutions'] = directives.flag

    def run(self) -> List:
        """
        Replace placeholders with given variables.
        """
        new_content = []
        self.content = (  # pylint: disable=attribute-defined-outside-init
            self.content
        )  # type: List[str]
        existing_content = self.content
        substitution_defs = self.state.document.substitution_defs
        for item in existing_content:
            for name in self.state.document.substitution_names:
                if 'substitutions' in self.options:
                    replacement = substitution_defs[name].astext()
                    item = item.replace(
                        '|{original}|'.format(original=name),
                        replacement,
                    )
            new_content.append(item)

        self.content = (  # pylint: disable=attribute-defined-outside-init
            new_content
        )
        return list(super().run())


def substitution_code_role(  # pylint: disable=dangerous-default-value
    typ: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Dict = {},
    content: List[str] = [],
) -> Tuple[List[Node], List[system_message]]:
    """
    Replace placeholders with given variables.
    """
    document = inliner.document  # type: ignore
    for name in document.substitution_names:
        replacement = document.substitution_defs[name].astext()
        text = text.replace(
            '|{original}|'.format(original=name),
            replacement,
        )
        rawtext = text.replace(
            '|{original}|'.format(original=name),
            replacement,
        )
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


def setup(app: Sphinx) -> None:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value('substitutions', [], 'html')
    directives.register_directive('prompt', SubstitutionPrompt)
    directives.register_directive('code-block', SubstitutionCodeBlock)
    app.add_role('substitution-code', substitution_code_role)
