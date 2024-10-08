"""
Configuration for pytest.
"""

import pytest
from beartype import beartype

pytest_plugins = "sphinx.testing.fixtures"  # pylint: disable=invalid-name


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    Apply the beartype decorator to all collected test functions.
    """
    for item in items:
        # All our tests are functions, for now
        assert isinstance(item, pytest.Function)
        item.obj = beartype(obj=item.obj)
