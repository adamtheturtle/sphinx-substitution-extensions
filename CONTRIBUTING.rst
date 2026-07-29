Contributing
============

Contributions to this repository must pass tests and linting.

CI is the canonical source of truth.

Install contribution dependencies
---------------------------------

Install Python dependencies in a virtual environment.

.. code-block:: shell

   pip install --editable '.[dev]'

Spell checking requires ``enchant``.
This can be installed on macOS, for example, with `Homebrew`_:

.. code-block:: shell

   brew install enchant

and on Ubuntu with ``apt``:

.. code-block:: shell

   apt-get install -y enchant

Install ``pre-commit`` hooks:

.. code-block:: shell

   prek install

Linting
-------

Run lint tools either by committing, or with:

.. code-block:: shell

   prek run --all-files --hook-stage pre-commit --verbose
   prek run --all-files --hook-stage pre-push --verbose
   prek run --all-files --hook-stage manual --verbose

The development dependencies include `doc8-custom-ignores`_. The plugin is
discovered automatically by doc8 and reads additional ignores from
``pyproject.toml``:

.. code-block:: toml

   [tool.doc8]
   ignore-messages = [
       """Error in "include" directive:
   unknown option: "content-substitutions".""",
       """Error in "include" directive:
   unknown option: "path-substitutions".""",
   ]

This ignores diagnostics for ``include``'s ``:content-substitutions:`` and
``:path-substitutions:`` options. Plain docutils does not know about those
options, but this extension adds them when Sphinx builds the documentation.
Keep these as exact-message ignores so other ``D000`` diagnostics remain
visible.

.. _Homebrew: https://brew.sh
.. _doc8-custom-ignores: https://adamtheturtle.github.io/doc8-custom-ignores/

Running tests
-------------

Run ``pytest``:

.. code-block:: shell

   pytest

Continuous integration
----------------------

Tests are run on GitHub Actions.
The configuration for this is in ```.github/workflows/``.

Release Process
---------------

Outcomes
~~~~~~~~

* A new ``git`` tag available to install.
* A new package on PyPI.

Perform a Release
~~~~~~~~~~~~~~~~~

#. `Install GitHub CLI`_.

#. Perform a release:

   .. code-block:: shell

      $ gh workflow run release.yml --repo adamtheturtle/sphinx-substitution-extensions

.. _Install GitHub CLI: https://cli.github.com/manual/installation
