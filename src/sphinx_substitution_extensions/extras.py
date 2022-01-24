"""
sphinx-prompt support for Sphinx Substitution Extensions.
"""
from __future__ import annotations

from docutils.parsers.rst import directives  # type: ignore
from docutils.parsers.rst import Directive

from sphinx_substitution_extensions.shared import (
    EXISTING_DIRECTIVES,
    SUBSTITUTION_OPTION_NAME,
)

_EXISTING_PROMPT_DIRECTIVE: Directive = EXISTING_DIRECTIVES['prompt']


class SubstitutionPrompt(_EXISTING_PROMPT_DIRECTIVE):  # type: ignore
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    option_spec = _EXISTING_PROMPT_DIRECTIVE.option_spec or {}
    option_spec['substitutions'] = directives.flag

    def run(self) -> list:
        """
        Replace placeholders with given variables.
        """
        new_content = []
        self.content = (  # pylint: disable=attribute-defined-outside-init
            self.content
        )  # type: list[str]
        existing_content = self.content
        substitution_defs = self.state.document.substitution_defs
        for item in existing_content:
            for name, value in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    replacement = value.astext()
                    item = item.replace(f'|{name}|', replacement)

            new_content.append(item)

        self.content = (  # pylint: disable=attribute-defined-outside-init
            new_content
        )
        return list(super().run())
