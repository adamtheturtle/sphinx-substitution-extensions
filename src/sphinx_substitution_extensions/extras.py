"""
sphinx-prompt support for Sphinx Substitution Extensions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from docutils.parsers.rst import Directive, directives

from sphinx_substitution_extensions.shared import (
    EXISTING_DIRECTIVES,
    SUBSTITUTION_OPTION_NAME,
)

if TYPE_CHECKING:
    from docutils.nodes import raw

_EXISTING_PROMPT_DIRECTIVE: Directive = EXISTING_DIRECTIVES["prompt"]


class SubstitutionPrompt(_EXISTING_PROMPT_DIRECTIVE):  # type: ignore[misc, valid-type]
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    option_spec = _EXISTING_PROMPT_DIRECTIVE.option_spec or {}
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[raw]:
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
            new_item = item
            for name, value in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    replacement = value.astext()
                    new_item = new_item.replace(f"|{name}|", replacement)

            new_content.append(new_item)

        self.content = (  # pylint: disable=attribute-defined-outside-init
            new_content
        )
        return list(super().run())
