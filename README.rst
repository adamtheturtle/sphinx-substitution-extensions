|Build Status|

|codecov|

|requirements|

Sphinx Substitutions Extensions
===============================

Extensions for Sphinx which allow substitutions.

.. contents::

Installation
------------

Setup
~~~~~

* Add the following to ``conf.py``:

.. code:: python

   extensions += ['sphinx_substitution_extensions']

* Set the following variable in ``conf.py``:

.. code:: python

   substitutions = (
       ('|release|', '0.1'),
       ('|author|', 'Eleanor'),
   )

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Directives
----------

``substitution-prompt``
~~~~~~~~~~~~~~~~~~~~~~~

Then use the following:

.. code:: rst

   .. substitution-prompt:: bash

      echo "|author| released version |release|"

This is an extension of `sphinx-prompt`_.

``substitution-prompt`` acts similarly to `sphinx-prompt`_, and adds replacement functionality.

Credits
-------

``sphinx-prompt`` authors
~~~~~~~~~~~~~~~~~~~~~~~~~

Thanks to `@sbrunner`_ and other contributors for `sphinx-prompt`_.
``substitution-prompt`` is based on `sphinx-prompt`_.

ClusterHQ
~~~~~~~~~

This package is largely inspired by code written for Flocker by ClusterHQ.

Contributing
------------

Release Process
~~~~~~~~~~~~~~~

Outcomes
^^^^^^^^

* A new ``git`` tag available to install.
* A new package on PyPI.

Prerequisites
^^^^^^^^^^^^^

* ``python3`` on your ``PATH`` set to Python 3.6+.
* ``virtualenv``.
* Push access to this repository.
* Trust that ``master`` is ready and high enough quality for release.

Perform a Release
^^^^^^^^^^^^^^^^^

#. Install keyring

   Make sure that `keyring <https://pypi.org/project/keyring/>`__ is available on your path.

   E.g.:

   .. code:: sh

      curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
      pipsi install keyring

#. Set up PyPI credentials

Register at `PyPI <https://pypi.org>`__.

Add the following information to :file:`~/.pypirc`.

.. code:: ini

   [distutils]
    index-servers=
        pypi

    [pypi]
    username = <Your PyPI username>

Store your PyPI password:

.. code:: sh

   keyring set https://upload.pypi.org/legacy/ <Your PyPI username>

#. Get a GitHub access token:

   Follow the `GitHub instructions <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__ for getting an access token.

#. Set environment variables to GitHub credentials, e.g.:

    .. code:: sh

       export GITHUB_TOKEN=75c72ad718d9c346c13d30ce762f121647b502414
       export GITHUB_OWNER=adamtheturtle

#. Perform a release:

    .. code:: sh

       curl https://raw.githubusercontent.com/"$GITHUB_OWNER"/sphinx-substitution-extensions/master/admin/release.sh | bash


.. |Build Status| image:: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions.svg?branch=master
    :target: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions
.. _sphinx-prompt: https://github.com/sbrunner/sphinx-prompt
.. _@sbrunner: https://github.com/sbrunner
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions
.. |requirements| image:: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements.svg?branch=master
     :target: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements/?branch=master
     :alt: Requirements Status
