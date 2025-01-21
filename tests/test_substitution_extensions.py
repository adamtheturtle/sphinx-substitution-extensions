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
    The ``code-block`` directive does not replace placeholders.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. code-block:: shell

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        freshenv=True,
    )

    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()

    assert content_html == expected_content_html


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
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. code-block:: shell
           :substitutions:

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        .. code-block:: shell

            $ PRE-example_substitution-POST
        """,
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


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
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |aBcD_eFgH| replace:: example_substitution

        .. code-block:: shell
           :substitutions:

           $ PRE-|aBcD_eFgH|-POST
        """,
    )
    source_file.write_text(data=source_file_content)

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        .. code-block:: shell

            $ PRE-example_substitution-POST
        """,
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


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
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        Example :substitution-code:`PRE-|a|-POST`
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        Example :code:`PRE-example_substitution-POST`
        """,
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


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
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |aBcD_eFgH| replace:: example_substitution

        Example :substitution-code:`PRE-|aBcD_eFgH|-POST`
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        Example :code:`PRE-example_substitution-POST`
        """,
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


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
    (source_directory / "conf.py").touch()

    # Importantly we have a non-space whitespace character in the target name.
    downloadable_file = (
        source_directory / "tgt_pre-example_substitution-tgt_post .py"
    )
    downloadable_file.write_text(data="Sample")
    source_file_content = dedent(
        # Importantly we have a substitution in the download text and the
        # target.
        text="""\
    .. |a| replace:: example_substitution

    :substitution-download:`txt_pre-|a|-txt_post <tgt_pre-|a|-tgt_post\t.py>`
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        :download:`txt_pre-example_substitution-txt_post <tgt_pre-example_substitution-tgt_post\t.py>`
        """,  # noqa: E501
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


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
        source_file = source_directory / "index.rst"
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. |a| replace:: rst_prolog_substitution

            .. code-block:: shell
               :substitutions:

               $ PRE-|a|-POST
            """,
        )
        source_file.write_text(data=index_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "myst_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "index.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            .. code-block:: shell

               $ PRE-rst_prolog_substitution-POST
            """,
        )

        source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "index.html"
        ).read_text()
        assert content_html == expected_content_html

    @staticmethod
    def test_myst_substitutions_ignored_without_rst_definition(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are ignored in rST documents without a rST
        substitution definition.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        source_file = source_directory / "index.rst"
        (source_directory / "conf.py").touch()
        source_file_content = dedent(
            text="""\
            .. code-block:: shell
               :substitutions:

               $ PRE-|a|-POST
            """,
        )
        source_file.write_text(data=source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "myst_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "index.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            .. code-block:: shell

               $ PRE-|a|-POST
            """,
        )

        source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "index.html"
        ).read_text()
        assert content_html == expected_content_html

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
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            ```{code-block}

            $ PRE-example_substitution-POST
            ```
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

    @staticmethod
    def test_myst_substitutions_not_enabled(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are not respected in MyST documents when
        ``myst_enable_extensions`` does not contain ``substitutions``.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            ```{code-block}

            $ PRE-|a|-POST
            ```
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

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
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. toctree::

                markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{code-block}
            :substitutions:

            $ PRE-|a|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
                "source_suffix": {
                    ".rst": "restructuredtext",
                    ".txt": "markdown",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            ```{code-block}

            $ PRE-example_substitution-POST
            ```
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": ["myst_parser"],
                "source_suffix": {
                    ".rst": "restructuredtext",
                    ".txt": "markdown",
                },
            },
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

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
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{code-block}
            :substitutions:

            $ PRE-{{a}}-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            ```{code-block}

            $ PRE-example_substitution-POST
            ```
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

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
        (source_directory / "conf.py").touch()
        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{code-block}
            :substitutions:

            $ PRE-[[a]]-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
                "myst_sub_delimiters": ("[", "]"),
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            ```{code-block}

            $ PRE-example_substitution-POST
            ```
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

    @staticmethod
    def test_substitution_code_role(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        The ``substitution-code`` role replaces the placeholders defined in
        ``conf.py`` as specified.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        (source_directory / "conf.py").touch()

        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            Example {substitution-code}`PRE-|a|-POST`
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)
        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            Example {code}`PRE-example_substitution-POST`
            """,
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html

    @staticmethod
    def test_substitution_download(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        The ``substitution-download`` role replaces the placeholders defined in
        ``conf.py`` as specified.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        (source_directory / "conf.py").touch()

        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
    # Title

    {substitution-download}`txt_pre-|a|-txt_post <tgt_pre-|a|-tgt_post\t.py>`
            """,
        )
        # Importantly we have a non-space whitespace character in the target
        # name.
        downloadable_file = (
            source_directory / "tgt_pre-example_substitution-tgt_post .py"
        )
        downloadable_file.write_text(data="Sample")
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)
        app = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "a": "example_substitution",
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        equivalent_source = dedent(
            text="""\
            # Title

            {download}`txt_pre-example_substitution-txt_post <tgt_pre-example_substitution-tgt_post\t.py>`
            """,  # noqa: E501
        )

        markdown_source_file.write_text(data=equivalent_source)
        app_expected = make_app(
            srcdir=source_directory,
            exception_on_warning=True,
            confoverrides={"extensions": ["myst_parser"]},
        )
        app_expected.build()
        assert app_expected.statuscode == 0

        expected_content_html = (
            app_expected.outdir / "markdown_document.html"
        ).read_text()
        assert content_html == expected_content_html
