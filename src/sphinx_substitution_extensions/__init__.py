"""
Custom Sphinx extensions.
"""

import importlib
from typing import List

from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock

# Due to the dash in the name, we cannot import sphinx-prompt using a normal
# import.
_SPHINX_PROMPT = importlib.import_module('sphinx-prompt')
_PROMPT_DIRECTIVE = _SPHINX_PROMPT.PromptDirective  # type: ignore


class SubstitutionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces placeholders with variables.
    """

    def run(self) -> List:
        """
        Replace placeholders with given variables.
        """
        app = self.state.document.settings.env.app
        new_content = []
        self.content = self.content  # type: List[str]
        existing_content = self.content
        for item in existing_content:
            for pair in app.config.substitutions:
                original, replacement = pair
                item = item.replace(original, replacement)
            new_content.append(item)

        self.content = new_content
        return list(CodeBlock.run(self))


class SubstitutionPrompt(_PROMPT_DIRECTIVE):  # type: ignore
    """
    Similar to PromptDirective but replaces placeholders with variables.
    """

    def run(self) -> List:
        """
        Replace placeholders with given variables.
        """
        app = self.state.document.settings.env.app
        new_content = []
        self.content = (  # pylint: disable=attribute-defined-outside-init
            self.content
        )  # type: List[str]
        existing_content = self.content
        for item in existing_content:
            for pair in app.config.substitutions:
                original, replacement = pair
                item = item.replace(original, replacement)
            new_content.append(item)

        self.content = (  # pylint: disable=attribute-defined-outside-init
            new_content
        )
        return list(_PROMPT_DIRECTIVE.run(self))


def setup(app: Sphinx) -> None:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value('substitutions', [], 'html')
    app.add_directive('substitution-prompt', SubstitutionPrompt)
    app.add_directive('substitution-code-block', SubstitutionCodeBlock)
