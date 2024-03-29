"""
sphinx-prompt support for Sphinx Substitution Extensions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import docutils.nodes
import sphinx_prompt
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import RSTState
from docutils.statemachine import StringList

from sphinx_substitution_extensions.shared import (
    SUBSTITUTION_OPTION_NAME,
)

if TYPE_CHECKING:
    from docutils.nodes import raw


class SubstitutionPrompt(sphinx_prompt.PromptDirective):
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    option_spec = sphinx_prompt.PromptDirective.option_spec or {}
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[raw]:
        """
        Replace placeholders with given variables.
        """
        new_content = StringList()
        existing_content = self.content
        state = self.state  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        assert isinstance(state, RSTState)
        document = state.document  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        assert isinstance(document, docutils.nodes.document)
        substitution_defs = document.substitution_defs

        for item in existing_content:
            new_item = item
            for name, value in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    replacement = value.astext()
                    new_item = new_item.replace(f"|{name}|", replacement)

            new_item_string_list = StringList(initlist=[new_item])
            new_content.extend(new_item_string_list)

        self.content = new_content
        return super().run()
