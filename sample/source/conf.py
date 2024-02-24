"""
Sample ``conf.py``.
"""

extensions = [
    "myst_parser",
    "sphinx_substitution_extensions",
]

rst_prolog = """
.. |author| replace:: Eleanor
.. |MixedCaseReplacement| replace:: UnusedReplacement
"""

myst_enable_extensions = ["substitution"]
myst_substitutions = {
    "author": "Talya",
}
