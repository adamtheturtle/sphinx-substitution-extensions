"""
Custom lint tests.
"""

from pathlib import Path


def test_init_files() -> None:
    """
    ``__init__`` files exist where they should do.

    If ``__init__`` files are missing, linters may not run on all files that
    they should run on.
    """
    directories = (Path('src'), Path('tests'))

    for directory in directories:
        files = directory.glob('**/*.py')
        for python_file in files:
            parent = python_file.parent
            expected_init = parent / '__init__.py'
            assert expected_init.exists()
