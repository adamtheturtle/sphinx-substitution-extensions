"""
Tests for Sphinx extensions.
"""

import subprocess
from pathlib import Path
from textwrap import dedent

# See https://github.com/PyCQA/pylint/issues/1536 for details on why the errors
# are disabled.
from py.path import local  # pylint: disable=no-name-in-module, import-error


def test_smart_prompt(tmpdir: local) -> None:
    """
    The ``smart-prompt`` directive replaces the placeholders defined in
    ``conf.py`` as specified.
    """
    source_directory = tmpdir.mkdir('source')
    source_file = source_directory.join('contents.rst')
    conf_py = source_directory.join('conf.py')
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        smart_prompt_placeholder_replace_pairs = (
            ('|a|', 'example_substitution'),
        )
        """,
    )
    conf_py.write(conf_py_content)
    source_file_content = dedent(
        """\
        .. smart-prompt:: bash $

           $ PRE-|a|-POST
        """,
    )
    source_file.write(source_file_content)
    destination_directory = tmpdir.mkdir('destination')
    args = [
        'sphinx-build',
        '-b',
        'html',
        # Directory containing source and config files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = 'PRE-example_substitution-POST'
    content_html = Path(str(destination_directory)) / 'contents.html'
    assert expected in content_html.read_text()
