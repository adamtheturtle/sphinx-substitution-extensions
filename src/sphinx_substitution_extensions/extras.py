"""
sphinx-prompt support for Sphinx Substitution Extensions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from docutils.parsers.rst import directives

from sphinx_substitution_extensions.shared import (
    SUBSTITUTION_OPTION_NAME,
)

if TYPE_CHECKING:
    from docutils.nodes import raw


sphinx_prompt = __import__("sphinx-prompt")
PromptDirective = sphinx_prompt.PromptDirective


class SubstitutionPrompt(PromptDirective):  # type: ignore[misc, valid-type]
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    option_spec = PromptDirective.option_spec or {}
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[raw]:
        """
        Replace placeholders with given variables.
        """
        new_content = []
        self.content: list[  # pylint: disable=attribute-defined-outside-init
            str
        ] = self.content
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
