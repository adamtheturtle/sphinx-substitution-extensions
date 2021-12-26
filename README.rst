|Build Status| |codecov| |PyPI|

Sphinx Substitution Extensions
==============================

Extensions for Sphinx which allow substitutions within code blocks.

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

   extensions += ['sphinx_substitution_extensions']

* Set the following variable in ``conf.py``:

.. code:: python

   rst_prolog = """
   .. |release| replace:: 0.1
   .. |author| replace:: Eleanor
   """

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Optional: sphinx-prompt
~~~~~~~~~~~~~~~~~~~~~~~

Sphinx Substitution Extensions supports the third-party extension `sphinx-prompt`_.

If you have ``sphinx-prompt`` installed, make sure ``sphinx-prompt`` dependency is loaded before ``sphinx_substitution_extensions``.
For example, ``conf.py`` should look like:

.. code:: python

   # sphinx-prompt must be the first of these two.
   extensions += ['sphinx-prompt', 'sphinx_substitution_extensions']

Directives
----------

``code-block``
~~~~~~~~~~~~~~

This adds a ``:substitutions:`` option to Sphinx's built-in `code-block`_ directive.

.. code:: rst

   .. code-block:: bash
      :substitutions:

      echo "|author| released version |release|"


``prompt``
~~~~~~~~~~

This adds a ``:substitutions:`` option to `sphinx-prompt`_.

.. note:: Requires the extension `sphinx-prompt`_.

.. code:: rst

   .. prompt:: bash
      :substitutions:

      echo "|author| released version |release|"


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

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-substitution-extensions/workflows/CI/badge.svg
   :target: https://github.com/adamtheturtle/sphinx-substitution-extensions/actions
.. _sphinx-prompt: https://github.com/sbrunner/sphinx-prompt
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. _@sbrunner: https://github.com/sbrunner
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions
.. |PyPI| image:: https://badge.fury.io/py/Sphinx-Substitution-Extensions.svg
   :target: https://badge.fury.io/py/Sphinx-Substitution-Extensions
