"""Run declarative Sphinx build-equivalence cases."""

import base64
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import pytest
from beartype.door import TypeHint
from sphinx.testing.util import SphinxTestApp
from typing_extensions import TypeIs


@dataclass(frozen=True, slots=True)
class Build:
    """Inputs for one side of an equivalence case."""

    files: dict[str, str]
    binary_files: dict[str, str]
    confoverrides: dict[str, object]
    exception_on_warning: bool


@dataclass(frozen=True, slots=True)
class Case:
    """Two Sphinx builds whose selected HTML output must match."""

    id: str
    description: str
    output: str
    actual: Build
    expected: Build


def _is_mapping(value: object, /) -> TypeIs[dict[str, object]]:
    """Return whether a parser value is a string-keyed mapping."""
    return TypeHint(hint=dict[str, object]).is_bearable(obj=value)


def _is_list(value: object, /) -> TypeIs[list[object]]:
    """Return whether a parser value is a list."""
    return isinstance(value, list)


def _mapping(value: object, *, context: str) -> dict[str, object]:
    """Validate and narrow a TOML table."""
    # Only the checked-in, collection-time validated manifest reaches tests.
    if not _is_mapping(value):  # pragma: no cover
        msg = f"{context} must be a table"
        raise TypeError(msg)
    return value


def _string(value: object, *, context: str) -> str:
    """Validate and narrow a TOML string."""
    # Only the checked-in, collection-time validated manifest reaches tests.
    if not isinstance(value, str):  # pragma: no cover
        msg = f"{context} must be a string"
        raise TypeError(msg)
    return value


def _string_mapping(value: object, *, context: str) -> dict[str, str]:
    """Validate and narrow a table whose values are strings."""
    table = _mapping(value=value, context=context)
    return {
        key: _string(value=item, context=f"{context}.{key}")
        for key, item in table.items()
    }


def _check_keys(data: dict[str, object], *, context: str) -> None:
    """Reject unknown keys left after parsing a table."""
    # Unknown manifest keys fail during collection, before any test can run.
    if len(data) > 0:  # pragma: no cover
        unknown_keys = ", ".join(sorted(data))
        msg = f"Unknown keys in {context}: {unknown_keys}"
        raise ValueError(msg)


def _parse_build(value: object, *, context: str) -> Build:
    """Parse one build table."""
    data = _mapping(value=value, context=context)
    files = _string_mapping(
        value=data.pop("files", {}),
        context=f"{context}.files",
    )
    binary_files = _string_mapping(
        value=data.pop("binary_files", {}),
        context=f"{context}.binary_files",
    )
    confoverrides = _mapping(
        value=data.pop("confoverrides", {}),
        context=f"{context}.confoverrides",
    )
    exception_on_warning = data.pop("exception_on_warning", False)
    # The checked-in manifest is validated at collection and contains a
    # Boolean.
    if not isinstance(exception_on_warning, bool):  # pragma: no cover
        msg = f"{context}.exception_on_warning must be a boolean"
        raise TypeError(msg)
    _check_keys(data=data, context=context)
    return Build(
        files=files,
        binary_files=binary_files,
        confoverrides=confoverrides,
        exception_on_warning=exception_on_warning,
    )


def _parse_case(value: object, *, index: int) -> Case:
    """Parse one equivalence case table."""
    context = f"cases[{index}]"
    data = _mapping(value=value, context=context)
    case = Case(
        id=_string(value=data.pop("id", None), context=f"{context}.id"),
        description=_string(
            value=data.pop("description", None),
            context=f"{context}.description",
        ),
        output=_string(
            value=data.pop("output", None),
            context=f"{context}.output",
        ),
        actual=_parse_build(
            value=data.pop("actual", None),
            context=f"{context}.actual",
        ),
        expected=_parse_build(
            value=data.pop("expected", None),
            context=f"{context}.expected",
        ),
    )
    _check_keys(data=data, context=context)
    return case


def _load_cases() -> list[Case]:
    """Load and validate all equivalence cases."""
    cases_path = Path(__file__).with_name(name="equivalence_cases.toml")
    with cases_path.open(mode="rb") as cases_file:
        data = _mapping(value=tomllib.load(cases_file), context="root")
    schema_version = data.pop("schema_version", None)
    # Tests run only after the checked-in version-one manifest is collected.
    if schema_version != 1:  # pragma: no cover
        msg = f"Unsupported schema version: {schema_version!r}"
        raise ValueError(msg)
    raw_cases = data.pop("cases", None)
    # The checked-in manifest's cases table is validated during collection.
    if not _is_list(raw_cases):  # pragma: no cover
        msg = "cases must be an array of tables"
        raise TypeError(msg)
    _check_keys(data=data, context="root")
    cases = [
        _parse_case(value=raw_case, index=index)
        for index, raw_case in enumerate(iterable=raw_cases)
    ]
    ids = [case.id for case in cases]
    # Duplicate IDs are a collection error in the checked-in manifest.
    if len(ids) != len(set(ids)):  # pragma: no cover
        msg = "Equivalence case IDs must be unique"
        raise ValueError(msg)
    return cases


def _destination(*, source_directory: Path, relative_path: str) -> Path:
    """Resolve and validate a case file path."""
    path = PurePosixPath(relative_path)
    # Unsafe checked-in fixture paths fail collection before tests can run.
    if path.is_absolute() or ".." in path.parts:  # pragma: no cover
        msg = (
            "Case file path must stay within its source directory: "
            f"{relative_path}"
        )
        raise ValueError(msg)
    return source_directory.joinpath(*path.parts)


def _write_build(*, source_directory: Path, build: Build) -> None:
    """Materialize one build's files."""
    overlap = build.files.keys() & build.binary_files.keys()
    # Overlapping text and binary paths fail manifest collection.
    if len(overlap) > 0:  # pragma: no cover
        msg = f"Files cannot be both text and binary: {sorted(overlap)}"
        raise ValueError(msg)
    for relative_path, content in build.files.items():
        destination = _destination(
            source_directory=source_directory,
            relative_path=relative_path,
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        _ = destination.write_text(data=content)
    for relative_path, content in build.binary_files.items():
        destination = _destination(
            source_directory=source_directory,
            relative_path=relative_path,
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        _ = destination.write_bytes(
            data=base64.b64decode(s=content, validate=True),
        )


def _build_html(
    *,
    source_directory: Path,
    build: Build,
    output: str,
    make_app: Callable[..., SphinxTestApp],
) -> str:
    """Build one side and return its selected HTML output."""
    _write_build(source_directory=source_directory, build=build)
    app = make_app(
        srcdir=source_directory,
        exception_on_warning=build.exception_on_warning,
        confoverrides=build.confoverrides,
    )
    app.build()
    assert app.statuscode == 0
    content = (app.outdir / output).read_text()
    app.cleanup()
    return content


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_load_cases(),
    ids=lambda case: case.id,
)
def test_equivalent_builds(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    case: Case,
) -> None:
    """Match an extension build to its hand-expanded equivalent."""
    actual_html = _build_html(
        source_directory=tmp_path / "actual",
        build=case.actual,
        output=case.output,
        make_app=make_app,
    )
    expected_html = _build_html(
        source_directory=tmp_path / "expected",
        build=case.expected,
        output=case.output,
        make_app=make_app,
    )
    assert actual_html == expected_html, case.description
