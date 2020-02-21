"""
Tests for Sphinx extensions.
"""

import subprocess
from pathlib import Path
from textwrap import dedent


def test_substitution_prompt(tmp_path: Path) -> None:
    """
    The ``substitution-prompt`` directive replaces the placeholders defined in
    ``conf.py`` as specified.
    """
    source_directory = tmp_path / 'source'
    source_directory.mkdir()
    source_file = source_directory / 'index.rst'
    conf_py = source_directory / 'conf.py'
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        substitutions = [
            ('|a|', 'example_substitution'),
        ]
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. substitution-prompt:: bash $

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / 'destination'
    args = [
        'sphinx-build',
        '-b',
        'html',
        '-W',
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = 'PRE-example_substitution-POST'
    content_html = Path(str(destination_directory)) / 'index.html'
    assert expected in content_html.read_text()


def test_substitution_code_block(tmp_path: Path) -> None:
    """
    The ``substitution-code-block`` directive replaces the placeholders
    defined in ``conf.py`` as specified.
    """
    source_directory = tmp_path / 'source'
    source_directory.mkdir()
    source_file = source_directory / 'index.rst'
    conf_py = source_directory / 'conf.py'
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        substitutions = [
            ('|a|', 'example_substitution'),
        ]
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. substitution-code-block:: bash

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / 'destination'
    args = [
        'sphinx-build',
        '-b',
        'html',
        '-W',
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = 'PRE-example_substitution-POST'
    content_html = Path(str(destination_directory)) / 'index.html'
    assert expected in content_html.read_text()


def test_substitution_inline(tmp_path: Path) -> None:
    """
    The ``substitution-code-block`` directive replaces the placeholders
    defined in ``conf.py`` as specified.
    """
    source_directory = tmp_path / 'source'
    source_directory.mkdir()
    source_file = source_directory / 'index.rst'
    conf_py = source_directory / 'conf.py'
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        substitutions = [
            ('|a|', 'example_substitution'),
        ]
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        Example :substitution-code:`PRE-|a|-POST`
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / 'destination'
    args = [
        'sphinx-build',
        '-b',
        'html',
        '-W',
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = 'PRE-example_substitution-POST'
    content_html = Path(str(destination_directory)) / 'index.html'
    assert expected in content_html.read_text()
