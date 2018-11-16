|Build Status| |codecov| |requirements| |PyPI|

Sphinx Substitution Extensions
==============================

Extensions for Sphinx which allow substitutions.

.. contents::

Installation
------------

.. code:: console

   $ pip install Sphinx-Substitution-Extensions

This supports Python 3.5+.

Setup
~~~~~

* Add the following to ``conf.py``:

.. code:: python

   extensions += ['sphinx-prompt', 'sphinx_substitution_extensions']

* Set the following variable in ``conf.py``:

.. code:: python

   substitutions = [
       ('|release|', '0.1'),
       ('|author|', 'Eleanor'),
   ]

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Directives
----------

``substitution-code-block``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. substitution-code-block:: bash

      echo "|author| released version |release|"

This is an extension of Sphinx's built-in `code-block`_ directive, and adds replacement functionality.

``substitution-prompt``
~~~~~~~~~~~~~~~~~~~~~~~

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

ClusterHQ Developers
~~~~~~~~~~~~~~~~~~~~

This package is largely inspired by code written for Flocker by ClusterHQ.
Developers of the relevant code include, at least, Jon Giddy and Tom Prince.

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions.svg?branch=master
    :target: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions
.. _sphinx-prompt: https://github.com/sbrunner/sphinx-prompt
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. _@sbrunner: https://github.com/sbrunner
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions
.. |requirements| image:: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements.svg?branch=master
     :target: https://requires.io/github/adamtheturtle/sphinx-substitution-extensions/requirements/?branch=master
     :alt: Requirements Status
.. |PyPI| image:: https://badge.fury.io/py/Sphinx-Substitution-Extensions.svg
    :target: https://badge.fury.io/py/Sphinx-Substitution-Extensions
