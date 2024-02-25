"""
Custom Sphinx extensions.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import docutils.nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import code_role
from docutils.parsers.rst.states import Inliner
from sphinx import addnodes
from sphinx.directives.code import CodeBlock
from sphinx.roles import XRefRole

from sphinx_substitution_extensions.extras import SubstitutionPrompt
from sphinx_substitution_extensions.shared import (
    SUBSTITUTION_OPTION_NAME,
)

if TYPE_CHECKING:
    from docutils.nodes import Element, Node, system_message
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

LOGGER = logging.getLogger(__name__)


class SubstitutionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    option_spec = CodeBlock.option_spec
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[Node]:
        """
        Replace placeholders with given variables.
        """
        self.option_spec["substitutions"] = directives.flag

        new_content: list[str] = []
        self.content: list[str] = self.content
        existing_content = self.content
        substitution_defs = {}
        source_file, _ = self.get_source_info()
        markdown_suffixes = {
            key
            for key, value in self.config.source_suffix.items()
            if value == "markdown"
        }

        if Path(source_file).suffix in markdown_suffixes:
            if "substitution" in self.config.myst_enable_extensions:
                substitution_defs = self.config.myst_substitutions
        else:
            substitution_defs = {
                key: value.astext()
                for key, value in self.state.document.substitution_defs.items()
            }

        for item in existing_content:
            new_item = item
            for name, replacement in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    new_item = new_item.replace(f"|{name}|", replacement)
            new_content.append(new_item)

        self.content = new_content
        return super().run()


class _PostParseInliner(Inliner):
    """``Inliner.document`` is set in ``Inliner.parse``."""

    document: docutils.nodes.document


class SubstitutionCodeRole:
    """Custom role for substitution code."""

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
        # The ``inliner`` type is, in Sphinx, typed as ``Inliner``.
        inliner: _PostParseInliner,
        # We allow mutable defaults as the Sphinx implementation requires it.
        options: dict[Any, Any] = {},  # noqa: B006
        content: list[str] = [],  # noqa: B006
    ) -> tuple[list[Node], list[system_message]]:
        """
        Replace placeholders with given variables.
        """
        inliner_document = inliner.document
        for name, value in inliner_document.substitution_defs.items():
            assert isinstance(name, str)
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


class SubstitutionXRefRole(XRefRole):
    """Custom role for XRefs."""

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        # We allow a boolean-typed positional argument as we are matching the
        # method signature of the parent class.
        has_explicit_title: bool,  # noqa: FBT001
        title: str,
        target: str,
    ) -> tuple[str, str]:
        """
        Override parent method to replace placeholders with given variables.
        """
        document = self.inliner.document  # type: ignore[attr-defined]
        assert isinstance(document, docutils.nodes.document)
        for name, value in document.substitution_defs.items():
            assert isinstance(name, str)
            replacement = value.astext()
            title = title.replace(f"|{name}|", replacement)
            target = target.replace(f"|{name}|", replacement)

        # Use the default implementation to process the link
        # as it handles whitespace in target text.
        return super().process_link(
            env=env,
            refnode=refnode,
            has_explicit_title=has_explicit_title,
            title=title,
            target=target,
        )


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value("substitutions", [], "html")
    directives.register_directive("code-block", SubstitutionCodeBlock)
    app.setup_extension("sphinx-prompt")
    directives.register_directive("prompt", SubstitutionPrompt)
    app.add_role("substitution-code", SubstitutionCodeRole())
    substitution_download_role = SubstitutionXRefRole(
        nodeclass=addnodes.download_reference
    )
    app.add_role("substitution-download", substitution_download_role)
    return {"parallel_read_safe": True}
