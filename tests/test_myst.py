"""Tests for MyST documents."""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from beartype.roar import BeartypeCallHintParamViolation
from sphinx.errors import SphinxError
from sphinx.testing.util import SphinxTestApp


def test_myst_unsupported_substitution_value_raises_error(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """Reject unsupported substitution values."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    _ = (source_directory / "index.md").write_text(
        data=dedent(
            text="""\
                # Title

                ```{code-block}
                :substitutions:

                |unsupported|
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
            "myst_substitutions": {"unsupported": None},
        },
    )

    with pytest.raises(
        expected_exception=BeartypeCallHintParamViolation,
        match="substitutions",
    ):
        app.build()


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
    _ = index_source_file.write_text(data=index_source_file_content)
    _ = markdown_source_file.write_text(data=markdown_source_file_content)

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
    _ = index_source_file.write_text(data=index_source_file_content)
    _ = markdown_source_file.write_text(data=markdown_source_file_content)

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
    _ = index_source_file.write_text(data=index_source_file_content)
    _ = markdown_source_file.write_text(data=markdown_source_file_content)

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
