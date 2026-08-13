"""Tests for Sphinx extensions."""

from collections.abc import Callable
from importlib.metadata import version
from pathlib import Path
from textwrap import dedent

import pytest
from docutils import core, nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.testing.util import SphinxTestApp

import sphinx_substitution_extensions


def test_setup(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Test that the setup function returns the expected metadata."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    app = make_app(
        srcdir=source_directory,
    )
    setup_result = sphinx_substitution_extensions.setup(app=app)
    pkg_version = version(distribution_name="sphinx-substitution-extensions")
    assert setup_result == {
        "parallel_read_safe": True,
        "version": pkg_version,
    }


def test_substitution_literal_include_in_rest_example(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """The ``literalinclude`` directive works inside rest-example."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. rest-example::

           .. literalinclude:: example.txt
              :content-substitutions:
        """,
    )
    source_file.write_text(data=source_file_content)
    app = make_app(
        srcdir=source_directory,
        warningiserror=True,
        confoverrides={
            "extensions": [
                "sphinx_substitution_extensions",
                "sphinx_toolbox.rest_example",
            ],
        },
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "index.html").read_text()
    assert "example_substitution" in content_html


class TestMyst:
    """Tests for MyST documents."""

    @staticmethod
    def test_myst_invalid_substitution_access(
        *,
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """MyST invalid substitution access does not break the build."""
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

            $ PRE-|items.99|-POST
            ```

            ```{code-block}
            :substitutions:

            $ PRE-|nonexistent.key|-POST
            ```
            """,
        )
        index_source_file.write_text(data=index_source_file_content)
        markdown_source_file.write_text(data=markdown_source_file_content)

        app = make_app(
            srcdir=source_directory,
            exception_on_warning=False,
            confoverrides={
                "extensions": [
                    "myst_parser",
                    "sphinx_substitution_extensions",
                ],
                "myst_enable_extensions": ["substitution"],
                "myst_substitutions": {
                    "items": ["a", "b"],
                },
            },
        )
        app.build()
        assert app.statuscode == 0
        content_html = (app.outdir / "markdown_document.html").read_text()
        app.cleanup()

        expected_text_in_html = [
            "$ PRE-|items.99|-POST",
            "$ PRE-|nonexistent.key|-POST",
        ]
        for text in expected_text_in_html:
            assert text in content_html

    @staticmethod
    def test_myst_substitution_key_with_dot_raises_error(
        *,
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """MyST substitution keys containing dots raise SphinxError.

        Dots are reserved for nested access notation.
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

            |key.with.dots|
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
                    "key.with.dots": "value",
                },
            },
        )

        with pytest.raises(
            expected_exception=SphinxError,
            match=r"Substitution key 'key\.with\.dots' contains a dot",
        ):
            app.build()

    @staticmethod
    def test_myst_nested_substitution_key_with_dot_raises_error(
        *,
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """MyST nested substitution keys containing dots raise SphinxError.

        Dots are reserved for nested access notation.
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

            |parent.key.with.dots|
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
                    "parent": {
                        "key.with.dots": "value",
                    },
                },
            },
        )

        with pytest.raises(
            expected_exception=SphinxError,
            match=r"Substitution key 'key\.with\.dots' contains a dot",
        ):
            app.build()


def test_no_substitution_include(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Leave an ``include`` path unchanged by default."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    (source_directory / "example.txt").write_text(data="Included content")
    (source_directory / "index.rst").write_text(
        data=".. include:: example.txt\n",
    )

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()

    assert app.statuscode == 0
    assert "Included content" in (app.outdir / "index.html").read_text()


def test_include_fragment_is_not_reported_as_unreferenced(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Register included documents with the Sphinx environment."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    (source_directory / "fragment.rst").write_text(data="Included content")
    (source_directory / "index.rst").write_text(
        data=".. include:: fragment.rst\n",
    )

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()

    assert app.statuscode == 0


def test_include_without_sphinx_environment(tmp_path: Path) -> None:
    """Support documents which have no Sphinx environment."""
    source_file = tmp_path / "index.rst"
    source_file.write_text(data=".. include:: included.rst\n")
    (tmp_path / "included.rst").write_text(data="Included content")
    directives.register_directive(
        name="include",
        directive=sphinx_substitution_extensions.SubstitutionInclude,
    )

    publish_doctree: Callable[..., nodes.document] = core.publish_doctree  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    document = publish_doctree(
        source=source_file.read_text(),
        source_path=source_file.as_posix(),
        settings_overrides={"env": None},
    )

    assert "Included content" in document.astext()


def test_substitution_include_path(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Replace placeholders in an ``include`` path when requested."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    (source_directory / "example.txt").write_text(data="Included content")
    (source_directory / "index.rst").write_text(
        data=dedent(
            text="""\
            .. |name| replace:: example

            .. include:: |name|.txt
               :path-substitutions:
            """,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.build()

    assert app.statuscode == 0
    assert "Included content" in (app.outdir / "index.html").read_text()


def test_include_read_event_with_content_substitutions(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Emit include-read and then substitute the listener's content."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    include_file = source_directory / "example.txt"
    include_file.write_text(
        data="Included |name| content",
    )
    source_file = source_directory / "index.rst"
    source_file.write_text(
        data=dedent(
            text="""\
            .. |name| replace:: original

            .. include:: example.txt
               :content-substitutions:
            """,
        ),
    )
    observed_content: list[str] = []

    def on_include_read(
        _app: Sphinx,
        _relative_path: Path,
        _parent_docname: str,
        content: list[str],
    ) -> None:
        """Record and transform the included source."""
        observed_content.append(content[0])
        content[0] = content[0].replace("Included", "Observed")

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["sphinx_substitution_extensions"]},
    )
    app.connect(event="include-read", callback=on_include_read)
    app.build()

    assert observed_content == ["Included |name| content"]
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    include_file.write_text(data="Observed original content")
    source_file.write_text(data=".. include:: example.txt\n")
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


def test_default_substitution_include_path(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Replace ``include`` path placeholders when defaults are enabled."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    (source_directory / "example.txt").write_text(data="Included content")
    (source_directory / "index.rst").write_text(
        data=dedent(
            text="""\
            .. |name| replace:: example

            .. include:: |name|.txt
            """,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={
            "extensions": ["sphinx_substitution_extensions"],
            "substitutions_default_enabled": True,
        },
    )
    app.build()

    assert app.statuscode == 0
    assert "Included content" in (app.outdir / "index.html").read_text()


def test_default_substitution_include_disabled(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Respect ``:nopath-substitutions:`` when defaults are enabled."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    (source_directory / "[[name]].txt").write_text(data="Included content")
    (source_directory / "index.rst").write_text(
        data=dedent(
            text="""\
            .. toctree::

               document
            """,
        ),
    )
    (source_directory / "document.md").write_text(
        data=dedent(
            text="""\
            # Document

            ```{include} [[name]].txt
            :nopath-substitutions:
            ```
            """,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={
            "extensions": [
                "myst_parser",
                "sphinx_substitution_extensions",
            ],
            "myst_enable_extensions": ["substitution"],
            "myst_sub_delimiters": ("[", "]"),
            "myst_substitutions": {"name": "example"},
            "substitutions_default_enabled": True,
        },
    )
    app.build()

    assert app.statuscode == 0
    assert "Included content" in (app.outdir / "document.html").read_text()
