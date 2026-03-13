"""Property-based tests for substitution logic."""

import tempfile
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from hypothesis import HealthCheck, assume, given, settings
from hypothesis.strategies import (
    booleans,
    dictionaries,
    frozensets,
    just,
    text,
    tuples,
)
from sphinx.testing.util import SphinxTestApp

from sphinx_substitution_extensions import (
    _apply_substitutions,  # pyright: ignore[reportPrivateUsage]
)

# Strategy for placeholder names: non-empty text without pipe characters
# to avoid ambiguous delimiter overlap.
_placeholder_names = text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-",
    min_size=1,
    max_size=20,
)

# Strategy for replacement values: arbitrary text without pipe characters,
# so replacements do not introduce new placeholder syntax.
_safe_replacement_values = text(
    alphabet="abcdefghijklmnopqrstuvwxyz 0123456789._-/",
    max_size=50,
)

_delimiter_pairs = frozensets(
    elements=tuples(just(value="|"), just(value="|")),
    min_size=1,
    max_size=1,
)

_substitution_defs = dictionaries(
    keys=_placeholder_names,
    values=_safe_replacement_values,
    max_size=5,
)


class TestApplySubstitutionsProperties:
    """Property-based tests for ``_apply_substitutions``."""

    @given(input_text=text(), delimiter_pairs=_delimiter_pairs)
    def test_empty_substitutions_is_identity(
        self,
        *,
        input_text: str,
        delimiter_pairs: frozenset[tuple[str, str]],
    ) -> None:
        """With no substitution definitions, output equals input."""
        result = _apply_substitutions(
            text=input_text,
            substitution_defs={},
            delimiter_pairs=set(delimiter_pairs),
        )
        assert result == input_text

    @given(
        name=_placeholder_names,
        value=_safe_replacement_values,
    )
    def test_all_occurrences_replaced(
        self,
        *,
        name: str,
        value: str,
    ) -> None:
        """Every ``|name|`` in the text is replaced with the value."""
        placeholder = f"|{name}|"
        input_text = f"before {placeholder} middle {placeholder} after"
        result = _apply_substitutions(
            text=input_text,
            substitution_defs={name: value},
            delimiter_pairs={("|", "|")},
        )
        assert placeholder not in result
        assert result == f"before {value} middle {value} after"

    @given(
        input_text=text(
            alphabet="abcdefghijklmnopqrstuvwxyz 0123456789._-/\n",
            max_size=100,
        ),
        substitution_defs=_substitution_defs,
    )
    def test_no_placeholder_in_text_is_identity(
        self,
        *,
        input_text: str,
        substitution_defs: dict[str, str],
    ) -> None:
        """Text without any delimited keys is unchanged."""
        assume(
            condition=not any(
                f"|{name}|" in input_text for name in substitution_defs
            ),
        )

        result = _apply_substitutions(
            text=input_text,
            substitution_defs=substitution_defs,
            delimiter_pairs={("|", "|")},
        )
        assert result == input_text

    @given(
        name=_placeholder_names,
        value=_safe_replacement_values,
    )
    def test_no_leftover_placeholders(
        self,
        *,
        name: str,
        value: str,
    ) -> None:
        """After substitution, the placeholder pattern is gone.

        This holds when the replacement value does not itself contain
        the placeholder pattern.
        """
        placeholder = f"|{name}|"
        input_text = f"x {placeholder} y"
        result = _apply_substitutions(
            text=input_text,
            substitution_defs={name: value},
            delimiter_pairs={("|", "|")},
        )
        # The replacement values strategy excludes "|", so the
        # placeholder cannot reappear.
        assert placeholder not in result

    @given(
        name=_placeholder_names,
        value=_safe_replacement_values,
    )
    def test_myst_delimiters(
        self,
        *,
        name: str,
        value: str,
    ) -> None:
        """Substitution works with MyST ``{{ }}`` delimiters."""
        placeholder = f"{{{{{name}}}}}"
        input_text = f"pre {placeholder} post"
        result = _apply_substitutions(
            text=input_text,
            substitution_defs={name: value},
            delimiter_pairs={("{{", "}}")},
        )
        assert placeholder not in result
        assert result == f"pre {value} post"

    @given(
        name=_placeholder_names,
        value=_safe_replacement_values,
    )
    def test_multiple_delimiter_pairs(
        self,
        *,
        name: str,
        value: str,
    ) -> None:
        """Both RST and MyST delimiters are replaced in one call."""
        rst_placeholder = f"|{name}|"
        myst_placeholder = f"{{{{{name}}}}}"
        input_text = f"{rst_placeholder} and {myst_placeholder}"
        result = _apply_substitutions(
            text=input_text,
            substitution_defs={name: value},
            delimiter_pairs={("|", "|"), ("{{", "}}")},
        )
        assert rst_placeholder not in result
        assert myst_placeholder not in result
        assert result == f"{value} and {value}"


class TestShouldApplySubstitutionsProperties:
    """Property-based tests for substitution flag behavior."""

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(default_enabled=booleans())
    def test_nosubstitutions_flag_prevents_replacement(
        self,
        *,
        default_enabled: bool,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """``:nosubstitutions:`` prevents replacement.

        Regardless of the ``substitutions_default_enabled`` config.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            source_directory = Path(tmp_dir) / "source"
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
                    "substitutions_default_enabled": default_enabled,
                },
            )
            app.build()
            assert app.statuscode == 0
            content_html = (app.outdir / "index.html").read_text()
            app.cleanup()

            # The substitution value should NOT appear.
            assert "example_substitution" not in content_html

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(default_enabled=booleans())
    def test_substitutions_flag_forces_replacement(
        self,
        *,
        default_enabled: bool,
        make_app: Callable[..., SphinxTestApp],
    ) -> None:
        """``:substitutions:`` forces replacement.

        Regardless of the ``substitutions_default_enabled`` config.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            source_directory = Path(tmp_dir) / "source"
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
                confoverrides={
                    "extensions": ["sphinx_substitution_extensions"],
                    "substitutions_default_enabled": default_enabled,
                },
            )
            app.build()
            assert app.statuscode == 0
            content_html = (app.outdir / "index.html").read_text()
            app.cleanup()

            # The placeholder SHOULD be replaced.
            assert "PRE-example_substitution-POST" in content_html
            assert "PRE-|a|-POST" not in content_html
