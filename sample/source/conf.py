"""
Sample ``conf.py``.
"""

extensions = [
    'sphinx-prompt',
    'sphinx_substitution_extensions',
]

rst_prolog = """
.. |author| replace:: Eleanor
.. |MixedCaseReplacement| replace:: UnusedReplacement
"""
