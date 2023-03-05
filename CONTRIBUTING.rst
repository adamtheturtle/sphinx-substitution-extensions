Contributing
============

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
