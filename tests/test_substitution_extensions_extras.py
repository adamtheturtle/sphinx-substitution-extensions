"""
Tests for extra modules.
"""

import logging
from pathlib import Path
from textwrap import dedent
from typing import Callable

import pytest
from sphinx.testing.util import SphinxTestApp
from sphinx_substitution_extensions import _exists_dependency

_EXISTS_PROMPT_EXTENSION = _exists_dependency("sphinx-prompt")
_REASON = "requires sphinx-prompt to be installed"

pytestmark = [pytest.mark.skipif(not _EXISTS_PROMPT_EXTENSION, reason=_REASON)]


def test_prompt_specified_late(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    caplog,
) -> None:
    """
    If sphinx-prompt is not specified in extensions before Sphinx substitution
    extensions, an warning is given.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx_substitution_extensions', 'sphinx-prompt']
        """,
    )
    conf_py.write_text(conf_py_content)
    app = make_app(srcdir=source_directory, freshenv=True)
    app.build()
    assert app.statuscode == 0  # Do not raise an error

    expected_message = (
        "sphinx-prompt must be in the conf.py extensions list before "
        "sphinx_substitution_extensions"
    )

    assert caplog.record_tuples == [
        ("sphinx_substitution_extensions", logging.WARNING, expected_message),
    ]


def test_prompt_not_specified(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    caplog,
) -> None:
    """
    If sphinx-prompt is not specified in extensions but is installed,
    a warning is given.
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
        """,
    )
    conf_py.write_text(conf_py_content)
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0  # Do not raise an error

    expected_message = (
        "sphinx-prompt must be in the conf.py extensions list before "
        "sphinx_substitution_extensions"
    )

    assert caplog.record_tuples == [
        ("sphinx_substitution_extensions", logging.WARNING, expected_message),
    ]


def test_substitution_prompt(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``prompt`` directive replaces the placeholders defined in ``conf.py``
    when requested.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx-prompt', 'sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. prompt:: bash $
           :substitutions:

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    app = make_app(srcdir=source_directory)
    app.build()
    expected = "PRE-example_substitution-POST"
    content_html = app.outdir / "index.html"
    assert expected in content_html.read_text()


def test_substitution_prompt_is_case_preserving(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``prompt`` directive respects the original case of replacements.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx-prompt', 'sphinx_substitution_extensions']
        rst_prolog = '''
        .. |aBcD_eFgH| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. prompt:: bash $
           :substitutions:

           $ PRE-|aBcD_eFgH|-POST
        """,
    )
    source_file.write_text(source_file_content)
    app = make_app(srcdir=source_directory)
    app.build()
    expected = "PRE-example_substitution-POST"
    content_html = app.outdir / "index.html"
    assert expected in content_html.read_text()


def test_no_substitution_prompt(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``prompt`` directive does not replace the placeholders defined in
    ``conf.py`` when that is not requested.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py.touch()
    source_file.touch()
    conf_py_content = dedent(
        """\
        extensions = ['sphinx-prompt', 'sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(conf_py_content)
    source_file_content = dedent(
        """\
        .. prompt:: bash $

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(source_file_content)
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    expected = "PRE-example_substitution-POST"
    assert expected not in content_html.read_text()
