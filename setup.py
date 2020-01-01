"""
Setup script.
"""

from pathlib import Path
from typing import List

from setuptools import setup


def _get_dependencies(requirements_file: Path) -> List[str]:
    """
    Return requirements from a requirements file.

    This expects a requirements file with no ``--find-links`` lines.
    """
    lines = requirements_file.read_text().strip().split('\n')
    return [line for line in lines if not line.startswith('#')]


_DIRECT_REQUIRES = _get_dependencies(
    requirements_file=Path('requirements.txt'),
)

_INDIRECT_REQUIRES = _get_dependencies(
    requirements_file=Path('indirect-requirements.txt'),
)

INSTALL_REQUIRES = _DIRECT_REQUIRES + _INDIRECT_REQUIRES
DEV_REQUIRES = _get_dependencies(
    requirements_file=Path('dev-requirements.txt'),
)
PACKAGING_REQUIRES = _get_dependencies(
    requirements_file=Path('packaging-requirements.txt'),
)

setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    install_requires=INSTALL_REQUIRES,
    extras_require={'dev': DEV_REQUIRES},
)
