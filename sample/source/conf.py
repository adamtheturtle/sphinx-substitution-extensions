"""
Sample ``conf.py``.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

extensions = [
    'sphinx-prompt',
    'sphinx_substitution_extensions',
]

rst_prolog = """
.. |author| replace:: Eleanor
.. |MixedCaseReplacement| replace:: UnusedReplacement
"""
