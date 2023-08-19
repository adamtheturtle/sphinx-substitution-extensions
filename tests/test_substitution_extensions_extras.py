"""
Tests for extra modules.
"""

import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def test_substitution_prompt(tmp_path: Path) -> None:
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
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected in content_html.read_text()


def test_substitution_prompt_is_case_preserving(tmp_path: Path) -> None:
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
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected in content_html.read_text()


def test_no_substitution_prompt(tmp_path: Path) -> None:
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
    destination_directory = tmp_path / "destination"
    args = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        # Directory containing source and configuration files.
        str(source_directory),
        # Directory containing build files.
        str(destination_directory),
        # Source file to process.
        str(source_file),
    ]
    subprocess.check_output(args=args)
    expected = "PRE-example_substitution-POST"
    content_html = Path(str(destination_directory)) / "index.html"
    assert expected not in content_html.read_text()
