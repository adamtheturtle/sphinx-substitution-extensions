|Build Status| |codecov| |PyPI|

Sphinx Substitution Extensions
==============================

Extensions for Sphinx which allow substitutions.

.. contents::

Installation
------------

.. code:: console

   $ pip install Sphinx-Substitution-Extensions

This supports Python 3.8+.

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

Inline ``:substitution-code:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   :substitution-code:`echo "|author| released version |release|"`

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
.. |PyPI| image:: https://badge.fury.io/py/Sphinx-Substitution-Extensions.svg
   :target: https://badge.fury.io/py/Sphinx-Substitution-Extensions
