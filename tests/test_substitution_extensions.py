"""
Tests for Sphinx extensions.
"""

from collections.abc import Callable
from importlib.metadata import version
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp

import sphinx_substitution_extensions


def test_setup(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    Test that the setup function returns the expected metadata.
    """
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


def test_default_substitutions_enabled(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is set to True in conf.py, code
    blocks should apply substitutions by default without needing the
    ``:substitutions:`` flag.
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
        confoverrides={
            "extensions": ["sphinx_substitution_extensions"],
            "substitutions_default_enabled": True,
        },
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


def test_default_substitutions_disabled_with_flag(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is True but a code block has the
    ``:nosubstitutions:`` flag, substitutions should not be applied.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. code-block:: shell
           :nosubstitutions:

           $ PRE-|a|-POST
        """,
    )
    source_file.write_text(data=source_file_content)
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
        freshenv=True,
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


def test_no_substitution_literal_include(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive does not replace placeholders.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: example.txt
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


def test_substitution_literal_include(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive replaces the placeholders defined in
    ``conf.py`` as specified when the `:content-substitutions:` flag is set.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: example.txt
           :content-substitutions:
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

    include_file.write_text(
        data="Content with example_substitution placeholder"
    )

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example.txt
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


def test_substitution_literal_include_empty_file(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive handles empty files without crashing.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    # Create an empty file
    include_file = source_directory / "empty.txt"
    include_file.write_text(data="")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: empty.txt
           :content-substitutions:
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
        .. literalinclude:: empty.txt
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


def test_substitution_literal_include_multiple(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive replaces multiple placeholders.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="PRE-|a|-MID-|b|-POST")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: first_substitution
        .. |b| replace:: second_substitution

        .. literalinclude:: example.txt
           :content-substitutions:
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

    include_file.write_text(
        data="PRE-first_substitution-MID-second_substitution-POST",
    )

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example.txt
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


def test_substitution_literal_include_with_caption(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive works with captions.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: example.txt
           :caption: Example caption
           :content-substitutions:
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

    include_file.write_text(
        data="Content with example_substitution placeholder"
    )

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example.txt
           :caption: Example caption
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


def test_substitution_literal_include_in_rest_example(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive works inside rest-example.
    """
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


def test_substitution_literal_include_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive replaces placeholders in the file path
    when the `:path-substitutions:` flag is set.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    # Create a file with substitution in the name
    include_file = source_directory / "example_substitution.txt"
    include_file.write_text(data="File content")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: |a|.txt
           :path-substitutions:
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

    # Compare with directly using the filename
    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example_substitution.txt
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


def test_substitution_literal_include_both_path_and_content(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``literalinclude`` directive can use both path and content
    substitutions at the same time.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    # Create a file with substitution in the name and content
    include_file = source_directory / "example_substitution.txt"
    include_file.write_text(data="Content with |b| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution
        .. |b| replace:: test_value

        .. literalinclude:: |a|.txt
           :path-substitutions:
           :content-substitutions:
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

    # Create equivalent file with substituted content
    include_file.write_text(data="Content with test_value placeholder")

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example_substitution.txt
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

    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


def test_default_substitutions_literal_include_content(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is True, ``literalinclude`` should
    apply content substitutions by default without requiring the ``:content-
    substitutions:`` flag.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: example.txt
        """,
    )
    source_file.write_text(data=source_file_content)
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
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    include_file.write_text(
        data="Content with example_substitution placeholder"
    )

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example.txt
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


def test_default_substitutions_literal_include_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is True, ``literalinclude`` should
    apply path substitutions by default without requiring the ``:path-
    substitutions:`` flag.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example_substitution.txt"
    include_file.write_text(data="File content")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: |a|.txt
        """,
    )
    source_file.write_text(data=source_file_content)
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
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example_substitution.txt
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


def test_default_substitutions_literal_include_disabled_content(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is True but ``literalinclude`` has
    the ``:nocontent-substitutions:`` flag, content substitutions should not be
    applied.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    include_file = source_directory / "example.txt"
    include_file.write_text(data="Content with |a| placeholder")

    source_file_content = dedent(
        text="""\
        .. |a| replace:: example_substitution

        .. literalinclude:: example.txt
           :nocontent-substitutions:
        """,
    )
    source_file.write_text(data=source_file_content)
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
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        .. literalinclude:: example.txt
        """,
    )

    source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        freshenv=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (app_expected.outdir / "index.html").read_text()
    assert content_html == expected_content_html


def test_default_substitutions_literal_include_disabled_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """When ``substitutions_default_enabled`` is True but ``literalinclude``
    has the ``:nopath-substitutions:`` flag, path substitutions should not be
    applied.

    Note: This test uses MyST format with custom delimiters because the `|`
    character cannot be used in Windows file paths.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    index_source_file = source_directory / "index.rst"
    markdown_source_file = source_directory / "markdown_document.md"
    (source_directory / "conf.py").touch()

    # Use custom delimiters [[a]] instead of |a| because | is not allowed
    # in Windows file paths
    include_file = source_directory / "[[a]].txt"
    include_file.write_text(data="File content")

    index_source_file_content = dedent(
        text="""\
        .. toctree::

           markdown_document
        """,
    )
    markdown_source_file_content = dedent(
        text="""\
        # Title

        ```{literalinclude} [[a]].txt
        :nopath-substitutions:
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
            "substitutions_default_enabled": True,
        },
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "markdown_document.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        # Title

        ```{literalinclude} [[a]].txt
        ```
        """,
    )

    markdown_source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["myst_parser"]},
        freshenv=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (
        app_expected.outdir / "markdown_document.html"
    ).read_text()
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


def test_no_substitution_image(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """The ``image`` directive does not replace custom placeholders by default.

    Note: reST by default processes |substitutions| in image paths, but
    our extension adds the ability to use custom delimiters like {{var}}.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    image_file = source_directory / "test_image.png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    source_file_content = dedent(
        text="""\
        .. |a| replace:: test_image

        .. image:: test_image.png
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

    # The behavior should be the same with or without our extension
    # when not using :path-substitutions:
    assert content_html == expected_content_html


def test_substitution_image_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``image`` directive replaces placeholders in the file path when the
    ``:path-substitutions:`` flag is set.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    # Create a simple image file with substitution in the name
    image_file = source_directory / "test_image.png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    source_file_content = dedent(
        text="""\
        .. |a| replace:: test_image

        .. image:: |a|.png
           :path-substitutions:
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

    # Compare with directly using the filename
    equivalent_source = dedent(
        text="""\
        .. image:: test_image.png
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


def test_substitution_image_path_multiple(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``image`` directive replaces multiple placeholders in the file path.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    # Create an image file with multiple substitutions in the name
    image_file = source_directory / "pre_test_mid_image_post.png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    source_file_content = dedent(
        text="""\
        .. |a| replace:: test
        .. |b| replace:: image

        .. image:: pre_|a|_mid_|b|_post.png
           :path-substitutions:
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

    # Compare with directly using the filename
    equivalent_source = dedent(
        text="""\
        .. image:: pre_test_mid_image_post.png
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


def test_substitution_image_with_options(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``image`` directive works with standard image options.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    image_file = source_directory / "test_image.png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    source_file_content = dedent(
        text="""\
        .. |a| replace:: test_image

        .. image:: |a|.png
           :path-substitutions:
           :alt: Test image alt text
           :width: 100px
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
        .. image:: test_image.png
           :alt: Test image alt text
           :width: 100px
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


def test_default_substitutions_image_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    When ``substitutions_default_enabled`` is True, ``image`` should apply path
    substitutions by default without requiring the ``:path-substitutions:``
    flag.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    source_file = source_directory / "index.rst"
    (source_directory / "conf.py").touch()

    image_file = source_directory / "test_image.png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    source_file_content = dedent(
        text="""\
        .. |a| replace:: test_image

        .. image:: |a|.png
        """,
    )
    source_file.write_text(data=source_file_content)
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
    content_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        .. image:: test_image.png
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


def test_default_substitutions_image_disabled_path(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """When ``substitutions_default_enabled`` is True but ``image`` has the
    ``:nopath-substitutions:`` flag, path substitutions should not be applied.

    Note: This test uses MyST format with custom delimiters because the `|`
    character cannot be used in Windows file paths.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    index_source_file = source_directory / "index.rst"
    markdown_source_file = source_directory / "markdown_document.md"
    (source_directory / "conf.py").touch()

    # Create an image file with the literal [[a]] in the filename
    image_file = source_directory / "[[a]].png"
    png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
        b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_file.write_bytes(data=png_data)

    index_source_file_content = dedent(
        text="""\
        .. toctree::

           markdown_document
        """,
    )
    markdown_source_file_content = dedent(
        text="""\
        # Title

        ```{image} [[a]].png
        :nopath-substitutions:
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
            "substitutions_default_enabled": True,
        },
    )
    app.build()
    assert app.statuscode == 0
    content_html = (app.outdir / "markdown_document.html").read_text()
    app.cleanup()

    equivalent_source = dedent(
        text="""\
        # Title

        ```{image} [[a]].png
        ```
        """,
    )

    markdown_source_file.write_text(data=equivalent_source)
    app_expected = make_app(
        srcdir=source_directory,
        exception_on_warning=True,
        confoverrides={"extensions": ["myst_parser"]},
        freshenv=True,
    )
    app_expected.build()
    assert app_expected.statuscode == 0

    expected_content_html = (
        app_expected.outdir / "markdown_document.html"
    ).read_text()
    assert content_html == expected_content_html


class TestImageMyst:
    """
    Tests for image directive with MyST documents.
    """

    @staticmethod
    def test_myst_substitutions_image(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        MyST substitutions are respected in image paths in MyST documents.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        (source_directory / "conf.py").touch()

        # Create an image file
        image_file = source_directory / "test_image.png"
        png_data = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
            b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
            b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        image_file.write_bytes(data=png_data)

        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{image} |a|.png
            :path-substitutions:
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
                    "a": "test_image",
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

            ```{image} test_image.png
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
    def test_myst_substitutions_image_default_delimiters(
        tmp_path: Path,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """
        The default MyST substitution delimiters {{}} are respected for images.
        """
        source_directory = tmp_path / "source"
        source_directory.mkdir()
        index_source_file = source_directory / "index.rst"
        markdown_source_file = source_directory / "markdown_document.md"
        (source_directory / "conf.py").touch()

        image_file = source_directory / "test_image.png"
        png_data = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
            b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx"
            b"\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        image_file.write_bytes(data=png_data)

        index_source_file_content = dedent(
            text="""\
            .. toctree::

               markdown_document
            """,
        )
        markdown_source_file_content = dedent(
            text="""\
            # Title

            ```{image} {{a}}.png
            :path-substitutions:
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
                    "a": "test_image",
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

            ```{image} test_image.png
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
