"""
Tests for extra modules.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


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
        extensions = ['sphinx_substitution_extensions']
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
        extensions = ['sphinx_substitution_extensions']
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
        extensions = ['sphinx_substitution_extensions']
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
