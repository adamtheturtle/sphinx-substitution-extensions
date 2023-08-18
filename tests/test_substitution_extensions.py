"""
Tests for Sphinx extensions.
"""

import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from typing import Callable

from sphinx.testing.util import SphinxTestApp
from sphinx_substitution_extensions import _exists_dependency


def test_no_substitution_code_block(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``code-block`` directive does not replace the placeholders defined in
    ``conf.py`` when not specified.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. code-block:: bash

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    tmp_path / "destination"
    app = make_app(srcdir=source_directory)
    app.build()
    build_directory = source_directory / "_build"
    expected = "PRE-example_substitution-POST"
    content_html = build_directory / "html" / "index.html"
    assert expected not in content_html.read_text()


def test_substitution_code_block(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``code-block`` directive replaces the placeholders defined in
    ``conf.py`` as specified.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. code-block:: bash
           :substitutions:

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    tmp_path / "destination"
    app = make_app(srcdir=source_directory)
    app.build()
    build_directory = source_directory / "_build"
    expected = "PRE-example_substitution-POST"
    content_html = build_directory / "html" / "index.html"
    assert expected in content_html.read_text()


def test_substitution_code_block_case_preserving(tmp_path: Path) -> None:
    """
    The ``code-block`` directive respects the original case of replacements.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |aBcD_eFgH| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. code-block:: bash
           :substitutions:

           $ PRE-|aBcD_eFgH|-POST
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected in content_html.read_text()


def test_substitution_inline(tmp_path: Path) -> None:
    """
    The ``substitution-code`` role replaces the placeholders defined in
    ``conf.py`` as specified.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        Example :substitution-code:`PRE-|a|-POST`
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected in content_html.read_text()


def test_substitution_inline_case_preserving(tmp_path: Path) -> None:
    """
    The ``substitution-code`` role respects the original case of replacements.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |aBcD_eFgH| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        Example :substitution-code:`PRE-|aBcD_eFgH|-POST`
        """,
    )
    source_file.write_text(source_file_content)
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected in content_html.read_text()


def test_exists_dependency() -> None:
    """
    Test exist_dependency function.
    """
    dependency = "sphinx_substitution_extensions"
    assert _exists_dependency(dependency) is True


def test_does_not_exists_dependency() -> None:
    """
    Test exist_dependency function.
    """
    dependency = "fake_sphinx_substitution_extensions"
    assert _exists_dependency(dependency) is False
