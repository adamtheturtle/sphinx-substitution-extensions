"""
Custom Sphinx extensions.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import code_role
from sphinx.directives.code import CodeBlock

from sphinx_substitution_extensions.extras import SubstitutionPrompt
from sphinx_substitution_extensions.shared import (
    SUBSTITUTION_OPTION_NAME,
)

if TYPE_CHECKING:
    from docutils.nodes import Node, literal_block, system_message
    from docutils.parsers.rst.states import Inliner
    from sphinx.application import Sphinx

LOGGER = logging.getLogger(__name__)


class SubstitutionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    option_spec = CodeBlock.option_spec
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[literal_block]:
        """
        Replace placeholders with given variables.
        """
        self.option_spec["substitutions"] = directives.flag

        new_content = []
        self.content: list[str] = self.content
        existing_content = self.content
        substitution_defs = self.state.document.substitution_defs
        for item in existing_content:
            new_item = item
            for name, value in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    replacement = value.astext()
                    new_item = new_item.replace(f"|{name}|", replacement)
            new_content.append(new_item)

        self.content = new_content
        return list(super().run())


class SubtitutionCodeRole:
    options: ClassVar[dict[str, Any]] = {
        "class": directives.class_option,
        "language": directives.unchanged,
    }

    def __call__(  # pylint: disable=dangerous-default-value
        self,
        typ: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        # We allow mutable defaults as the Sphinx implementation requires it.
        options: dict[Any, Any] = {},  # noqa: B006
        content: list[str] = [],  # noqa: B006
    ) -> tuple[list[Node], list[system_message]]:
        """
        Replace placeholders with given variables.
        """
        # We ignore this type error as "document" is not defined in the ``Inliner``
        # constructor but it is set by the time we get here.
        document = inliner.document  # type: ignore[attr-defined]
        for name, value in document.substitution_defs.items():
            replacement = value.astext()
            text = text.replace(f"|{name}|", replacement)
            rawtext = text.replace(f"|{name}|", replacement)
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


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value("substitutions", [], "html")
    directives.register_directive("code-block", SubstitutionCodeBlock)
    app.setup_extension("sphinx-prompt")
    directives.register_directive("prompt", SubstitutionPrompt)
    app.add_role("substitution-code", SubtitutionCodeRole())
    return {"parallel_read_safe": True}
