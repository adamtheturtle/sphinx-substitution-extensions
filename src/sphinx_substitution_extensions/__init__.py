"""
Custom Sphinx extensions.
"""

from typing import Any, ClassVar

from beartype import beartype
from docutils.nodes import Element, Node, system_message
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import code_role
from docutils.parsers.rst.states import Inliner
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util.typing import ExtensionMetadata, OptionSpec

from sphinx_substitution_extensions.shared import (
    SUBSTITUTION_OPTION_NAME,
)


@beartype
class SubstitutionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    option_spec: ClassVar[OptionSpec] = CodeBlock.option_spec
    option_spec["substitutions"] = directives.flag

    def run(self) -> list[Node]:
        """
        Replace placeholders with given variables.
        """
        new_content = StringList()
        existing_content = self.content
        substitution_defs = {}

        markdown_suffixes = {
            key.lstrip(".")
            for key, value in self.config.source_suffix.items()
            if value == "markdown"
        }

        # Use `| |` on reST as it is the default substitution syntax.
        # Use `| |` on MyST for backwards compatibility as this is what we
        # originally shipped with.
        delimiter_pairs = {("|", "|")}
        parser_supported_formats = set(self.env.parser.supported)
        if parser_supported_formats.intersection(markdown_suffixes):
            if "substitution" in self.config.myst_enable_extensions:
                substitution_defs = self.config.myst_substitutions
            opening_delimiter, closing_delimiter = (
                self.config.myst_sub_delimiters
            )
            new_delimiter_pair = (
                opening_delimiter + opening_delimiter,
                closing_delimiter + closing_delimiter,
            )
            delimiter_pairs = {*delimiter_pairs, new_delimiter_pair}
        else:
            substitution_defs = {
                key: value.astext()
                for key, value in self.state.document.substitution_defs.items()
            }

        for item in existing_content:
            new_item = item
            for name, replacement in substitution_defs.items():
                if SUBSTITUTION_OPTION_NAME in self.options:
                    for delimiter_pair in delimiter_pairs:
                        opening_delimiter, closing_delimiter = delimiter_pair
                        new_item = new_item.replace(
                            f"{opening_delimiter}{name}{closing_delimiter}",
                            replacement,
                        )
            new_item_string_list = StringList(initlist=[new_item])
            new_content.extend(other=new_item_string_list)

        self.content = new_content
        return super().run()


@beartype
class SubstitutionCodeRole:
    """
    Custom role for substitution code.
    """

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
        inliner_document = inliner.document
        for name, value in inliner_document.substitution_defs.items():
            replacement = value.astext()
            text = text.replace(f"|{name}|", replacement)
            rawtext = text.replace(f"|{name}|", replacement)
            rawtext = rawtext.replace(name, replacement)

        return code_role(
            role=typ,
            rawtext=rawtext,
            text=text,
            lineno=lineno,
            inliner=inliner,
            options=options,
            content=content,
        )


@beartype
class SubstitutionXRefRole(XRefRole):
    """
    Custom role for XRefs.
    """

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
        document = self.inliner.document
        for name, value in document.substitution_defs.items():
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


@beartype
def setup(app: Sphinx) -> ExtensionMetadata:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value(name="substitutions", default=[], rebuild="html")
    directives.register_directive(
        name="code-block",
        directive=SubstitutionCodeBlock,
    )
    app.add_role(name="substitution-code", role=SubstitutionCodeRole())
    substitution_download_role = SubstitutionXRefRole(
        nodeclass=addnodes.download_reference
    )
    app.add_role(name="substitution-download", role=substitution_download_role)
    return {"parallel_read_safe": True}
