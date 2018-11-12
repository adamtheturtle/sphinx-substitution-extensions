"""
Custom Sphinx extensions.
"""

from typing import List

from sphinx.application import Sphinx

# Due to the dash in the name, we cannot import sphinx-prompt using a normal
# import.
_SPHINX_PROMPT = __import__('sphinx-prompt')


class SubstitutionPrompt(_SPHINX_PROMPT.PromptDirective):  # type: ignore
    """
    Similar to PromptDirective but replaces placeholders with variables.

    Set the ``conf.py`` variable ``substitutions`` to a tuple of pairs, such
    as:

    .. code:: python

       substitutions = (
           ('|release|', release),
           ('|author|', 'Eleanor'),
       )

    Then use:

    .. code:: rst

       .. substitution-prompt:: bash

          echo "|author| released version |release|"
    """

    def run(self) -> List:
        """
        Replace the release placeholder with the release version.
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
        return list(_SPHINX_PROMPT.PromptDirective.run(self))


def setup(app: Sphinx) -> None:
    """
    Add the custom directives to Sphinx.
    """
    app.add_config_value('substitutions', (), 'html')
    app.add_directive('substitution-prompt', SubstitutionPrompt)
