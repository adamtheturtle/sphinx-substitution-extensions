Contributing
============

Contributions to this repository must pass tests and linting.

CI is the canonical source of truth.

Install contribution dependencies
---------------------------------

Install Python dependencies in a virtual environment.

.. code:: bash

   pip install --editable '.[dev]'

Spell checking requires ``enchant``.
This can be installed on macOS, for example, with `Homebrew`_:

.. code:: bash

   brew install enchant

and on Ubuntu with ``apt``:

.. code:: bash

   apt-get install -y enchant

Install ``pre-commit`` hooks:

.. code:: bash

   pre-commit install
   pre-commit install --hook-type pre-push

Linting
-------

Run lint tools either by committing, or with:

.. code:: bash

   pre-commit run --all-files --hook-stage commit --verbose
   pre-commit run --all-files --hook-stage push --verbose
   pre-commit run --all-files --hook-stage manual --verbose

.. _Homebrew: https://brew.sh

Running tests
-------------

Run ``pytest``:

.. code:: bash

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

   .. code:: bash

      $ gh workflow run release.yml --repo adamtheturtle/sphinx-substitution-extensions

.. _Install GitHub CLI: https://cli.github.com/manual/installation
