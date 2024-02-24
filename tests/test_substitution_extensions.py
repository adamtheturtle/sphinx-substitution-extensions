"""
Tests for Sphinx extensions.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


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
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    assert "PRE-example_substitution-POST" not in content_html.read_text()
    assert (
        '</span>PRE-<span class="p">|</span>a<span class="p">|</span>-POST'
        in content_html.read_text()
    )


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
    app = make_app(srcdir=source_directory)
    app.build()
    expected = "PRE-example_substitution-POST"
    content_html = app.outdir / "index.html"
    assert expected in content_html.read_text()


def test_substitution_code_block_case_preserving(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``code-block`` directive respects the original case of replacements.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
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

    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    expected = "PRE-example_substitution-POST"
    assert expected in content_html.read_text()


def test_substitution_inline(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``substitution-code`` role replaces the placeholders defined in
    ``conf.py`` as specified.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
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
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    expected = "PRE-example_substitution-POST"
    assert expected in content_html.read_text()


def test_substitution_inline_case_preserving(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``substitution-code`` role respects the original case of replacements.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
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
    expected = "PRE-example_substitution-POST"
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    expected = "PRE-example_substitution-POST"
    assert expected in content_html.read_text()


class TestMyst:
    """
    Tests for MyST documents.
    """

    @staticmethod
    def test_myst_substitutions_ignored_given_rst_definition(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are ignored in rST documents with a rST substitution
        definition.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            """\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "myst_substitution",
            }
            rst_prolog = '''
            .. |a| replace:: rst_prolog_substitution
            '''
            """,
        )
        conf_py.write_text(conf_py_content)
        index_source_file_content = dedent(
            """\
            .. code-block:: bash
               :substitutions:

               $ PRE-|a|-POST
            """,
        )
        index_source_file.write_text(data=index_source_file_content)

        app = make_app(srcdir=source_directory)
        app.build()
        expected = "PRE-rst_prolog_substitution-POST"
        content_html = app.outdir / "index.html"
        assert expected in content_html.read_text()
        assert "myst_substitution" not in content_html.read_text()

    @staticmethod
    def test_myst_substitutions_ignored_without_rst_definition(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are ignored in rST documents with a rST substitution
        definition.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            """\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "myst_substitution",
            }
            """,
        )
        conf_py.write_text(conf_py_content)
        index_source_file_content = dedent(
            """\
            .. code-block:: bash
               :substitutions:

               $ PRE-|a|-POST
            """,
        )
        index_source_file.write_text(data=index_source_file_content)

        app = make_app(srcdir=source_directory)
        app.build()
        expected = (
            '</span>PRE-<span class="p">|</span>a<span class="p">|</span>-POST'
        )
        content_html = app.outdir / "index.html"
        assert expected in content_html.read_text()
        assert "myst_substitution" not in content_html.read_text()

    @staticmethod
    def test_myst_substitutions(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are respected in MyST documents.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            """\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(conf_py_content)
        index_source_file_content = dedent(
            """\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            """\
            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(srcdir=source_directory)
        app.build()
        expected = "PRE-example_substitution-POST"
        content_html = app.outdir / "markdown_document.html"
        assert expected in content_html.read_text()

    @staticmethod
    def test_myst_substitutions_not_enabled(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are respected in MyST documents.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            """\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(conf_py_content)
        index_source_file_content = dedent(
            """\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            """\
            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(srcdir=source_directory)
        app.build()
        content_html = app.outdir / "markdown_document.html"
        assert "PRE-example_substitution-POST" not in content_html.read_text()
        assert "PRE-|a|-POST" in content_html.read_text()

    @staticmethod
    def test_myst_substitutions_custom_markdown_suffix(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        Custom markdown suffixes are respected in MyST documents.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.txt"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            """\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            source_suffix = {
                ".rst": "restructuredtext",
                ".txt": "markdown",
            }
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(conf_py_content)
        index_source_file_content = dedent(
            """\
            .. toctree::

            markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            """\
            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(srcdir=source_directory)
        app.build()
        expected = "PRE-example_substitution-POST"
        content_html = app.outdir / "markdown_document.html"
        assert expected in content_html.read_text()
