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

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions.svg?branch=master
    :target: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions
.. _sphinx-prompt: https://github.com/sbrunner/sphinx-prompt
.. _@sbrunner: https://github.com/sbrunner
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions
.. |requirements| image:: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements.svg?branch=master
     :target: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements/?branch=master
     :alt: Requirements Status
