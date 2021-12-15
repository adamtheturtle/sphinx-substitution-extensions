Contributing
============

Release Process
---------------

Outcomes
~~~~~~~~

* A new ``git`` tag available to install.
* A new package on PyPI.

Prerequisites
~~~~~~~~~~~~~

* ``python3`` on your ``PATH`` set to Python 3.8+.
* ``virtualenv``.
* Push access to this repository.
* Trust that ``master`` is ready and high enough quality for release.

Perform a Release
~~~~~~~~~~~~~~~~~

#. `Install GitHub CLI`_.

#. Perform a release:

   .. code:: bash

      $ gh workflow run release.yml --repo adamtheturtle/sphinx-substitution-extensions

.. _Install GitHub CLI: https://cli.github.com/manual/installation
