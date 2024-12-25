"""
Tests for Sphinx extensions.
"""

import re
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
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    source_file_content = dedent(
        text="""\
        .. code-block:: shell

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(data=source_file_content)
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
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    source_file_content = dedent(
        text="""\
        .. code-block:: shell
           :substitutions:

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(data=source_file_content)
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
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |aBcD_eFgH| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    source_file_content = dedent(
        text="""\
        .. code-block:: shell
           :substitutions:

           $ PRE-|aBcD_eFgH|-POST
        """,
    )
    source_file.write_text(data=source_file_content)

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
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    source_file_content = dedent(
        text="""\
        Example :substitution-code:`PRE-|a|-POST`
        """,
    )
    source_file.write_text(data=source_file_content)
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
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |aBcD_eFgH| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    source_file_content = dedent(
        text="""\
        Example :substitution-code:`PRE-|aBcD_eFgH|-POST`
        """,
    )
    source_file.write_text(data=source_file_content)
    expected = "PRE-example_substitution-POST"
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    expected = "PRE-example_substitution-POST"
    assert expected in content_html.read_text()


def test_substitution_download(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``substitution-download`` role replaces the placeholders defined in
    ``conf.py`` as specified in both the download text and the download target.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    conf_py = source_directory / "conf.py"
    conf_py_content = dedent(
        text="""\
        extensions = ['sphinx_substitution_extensions']
        rst_prolog = '''
        .. |a| replace:: example_substitution
        '''
        """,
    )
    conf_py.write_text(data=conf_py_content)
    # Importantly we have a non-space whitespace character in the target name.
    downloadable_file = (
        source_directory / "tgt_pre-example_substitution-tgt_post .py"
    )
    downloadable_file.write_text(data="Sample")
    source_file_content = (
        # Importantly we have a substitution in the download text and the
        # target.
        ":substitution-download:"
        "`txt_pre-|a|-txt_post <tgt_pre-|a|-tgt_post\t.py>`"
    )
    source_file.write_text(data=source_file_content)
    app = make_app(srcdir=source_directory)
    app.build()
    content_html = app.outdir / "index.html"
    # We use a pattern here because the download target is not predictable.
    expected_pattern = re.compile(
        pattern="<p>"
        '<a class="reference download internal" download="" '
        'href="_downloads/.*/tgt_pre-example_substitution-tgt_post%20.py">'
        "<code "
        'class="xref substitution-download docutils literal notranslate"'
        ">"
        '<span class="pre">'
        "txt_pre-example_substitution-txt_post"
        "</span>"
        "</code>"
        "</a>"
        "</p>"
    )
    content_html_text = content_html.read_text()
    assert expected_pattern.search(string=content_html_text) is not None


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
            text="""\
            extensions = ["myst_parser", "sphinx_substitution_extensions"]
            myst_enable_extensions = ["substitution"]
            myst_substitutions = {
                "a": "myst_substitution",
            }
            rst_prolog = '''
            .. |a| replace:: rst_prolog_substitution
            '''
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. code-block:: shell
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
            text="""\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "myst_substitution",
            }
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. code-block:: shell
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
            text="""\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
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
            text="""\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
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
            text="""\
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
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. toctree::

            markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
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
    def test_default_myst_sub_delimiters_code_block(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        The default MyST substitution delimiters are respected.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            text="""\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "example_substitution",
            }
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            ```{code-block}
            :substitutions:

            $ PRE-{{a}}-POST
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
    def test_custom_myst_sub_delimiters_code_block(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        Custom MyST substitution delimiters are respected.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        conf_py = source_directory / "conf.py"
        conf_py_content = dedent(
            text="""\
            extensions = ['myst_parser', 'sphinx_substitution_extensions']
            myst_enable_extensions = ['substitution']
            myst_substitutions = {
                "a": "example_substitution",
            }
            myst_sub_delimiters = ("[", "]")
            """,
        )
        conf_py.write_text(data=conf_py_content)
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            ```{code-block}
            :substitutions:

            $ PRE-[[a]]-POST
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
