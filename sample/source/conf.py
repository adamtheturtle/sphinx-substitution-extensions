"""Sample ``conf.py``."""

# Sphinx requires lowercase names for its configuration settings.
# pylint: disable=invalid-name

extensions = [
    "myst_parser",
    "sphinx_substitution_extensions",
    "sphinx_toolbox.rest_example",
]

rst_prolog = """
.. |author| replace:: Eleanor
.. |MixedCaseReplacement| replace:: UnusedReplacement
"""

myst_enable_extensions = ["substitution"]
myst_substitutions = {
    "author": "Talya",
}
