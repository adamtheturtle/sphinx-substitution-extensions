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

#. Get a GitHub access token:

   Follow the `GitHub instructions <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__ for getting an access token.

#. Set environment variables to GitHub credentials, e.g.:

    .. code:: sh

       export GITHUB_TOKEN=75c72ad718d9c346c13d30ce762f121647b502414
       export GITHUB_OWNER=adamtheturtle
       export GITHUB_REPOSITORY_NAME=sphinx-substitution-extensions

#. Perform a release:

    .. code:: sh

       curl https://raw.githubusercontent.com/"$GITHUB_OWNER"/"$GITHUB_REPOSITORY_NAME"/master/admin/release.sh | bash
