"""Configuration for pytest."""

# Pytest requires this lowercase module variable for plugin discovery.
pytest_plugins = "sphinx.testing.fixtures"  # pylint: disable=invalid-name
