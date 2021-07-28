"""
Setup script.
"""

from __future__ import annotations

from pathlib import Path

from setuptools import setup


def _get_dependencies(requirements_file: Path) -> list[str]:
    """
    Return requirements from a requirements file.

    This expects a requirements file with no ``--find-links`` lines.
    """
    lines = requirements_file.read_text().strip().split('\n')
    return [line for line in lines if not line.startswith('#')]


INSTALL_REQUIRES = _get_dependencies(
    requirements_file=Path('requirements/requirements.txt'),
)

DEV_REQUIRES = _get_dependencies(
    requirements_file=Path('requirements/dev-requirements.txt'),
)

SETUP_REQUIRES = _get_dependencies(
    requirements_file=Path('requirements/setup-requirements.txt'),
)

setup(
    use_scm_version=True,
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require={'dev': DEV_REQUIRES},
)
