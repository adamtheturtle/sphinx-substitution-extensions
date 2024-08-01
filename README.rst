|Build Status| |codecov| |PyPI|

Sphinx Substitution Extensions
==============================

Extensions for Sphinx which allow substitutions within code blocks.

.. contents::

Installation
------------

Sphinx Substitution Extensions is compatible with Sphinx 7.2.0+ using Python 3.10+.

.. code:: console

   $ pip install Sphinx-Substitution-Extensions

rST setup
---------

1. Add the following to ``conf.py`` to enable the extension:

.. code:: python

   extensions += ['sphinx_substitution_extensions']

2. Set the following variable in ``conf.py`` to define substitutions:

.. code:: python

   rst_prolog = """
   .. |release| replace:: 0.1
   .. |author| replace:: Eleanor
   """

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Using substitutions in rST documents
------------------------------------

``code-block``
~~~~~~~~~~~~~~

This adds a ``:substitutions:`` option to Sphinx's built-in `code-block`_ directive.

.. code:: rst

   .. code-block:: bash
      :substitutions:

      echo "|author| released version |release|"

Inline ``:substitution-code:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   :substitution-code:`echo "|author| released version |release|"`

``substitution-download``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   :substitution-download:`|author|'s manuscript <|author|_manuscript.txt>`


MyST Markdown setup
-------------------

1. Add the following to ``conf.py`` to enable the extension:

.. code:: python

   extensions += ['sphinx_substitution_extensions']

2. Set the following variables in ``conf.py`` to define substitutions:

.. code:: python

   myst_enable_extensions += ['substitution']
   myst_substitutions = {
         "release": "0.1",
         "author": "Eleanor",
   }

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Using substitutions in MyST Markdown
------------------------------------

``code-block``
~~~~~~~~~~~~~~

This adds a ``:substitutions:`` option to Sphinx's built-in `code-block`_ directive.

.. code:: markdown

   ```{code-block} bash
      :substitutions:

      echo "|author| released version |release|"
   ```

Credits
-------

ClusterHQ Developers
~~~~~~~~~~~~~~~~~~~~

This package is largely inspired by code written for Flocker by ClusterHQ.
Developers of the relevant code include, at least, Jon Giddy and Tom Prince.

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-substitution-extensions/workflows/CI/badge.svg
   :target: https://github.com/adamtheturtle/sphinx-substitution-extensions/actions
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-substitution-extensions
.. |PyPI| image:: https://badge.fury.io/py/Sphinx-Substitution-Extensions.svg
   :target: https://badge.fury.io/py/Sphinx-Substitution-Extensions
