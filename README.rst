|Build Status| |PyPI|

Sphinx Substitution Extensions
==============================

Extensions for Sphinx which allow substitutions within code blocks.

.. contents::

Installation
------------

Sphinx Substitution Extensions is compatible with Sphinx 8.2.0+ using Python |minimum-python-version|\+.

.. code-block:: console

   $ pip install Sphinx-Substitution-Extensions

rST setup
---------

1. Add the following to ``conf.py`` to enable the extension:

.. code-block:: python

   """Configuration for Sphinx."""

   extensions = ["sphinxcontrib.spelling"]  # Example existing extensions

   extensions += ["sphinx_substitution_extensions"]

2. Set the following variable in ``conf.py`` to define substitutions:

.. code-block:: python

   """Configuration for Sphinx."""

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

.. code-block:: rst

   .. code-block:: shell
      :substitutions:

      echo "|author| released version |release|"

Inline ``:substitution-code:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   :substitution-code:`echo "|author| released version |release|"`

``substitution-download``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   :substitution-download:`|author|'s manuscript <|author|_manuscript.txt>`

``literalinclude``
~~~~~~~~~~~~~~~~~~

This adds ``:content-substitutions:`` and ``:path-substitutions:`` options to Sphinx's built-in `literalinclude`_ directive.

Replace substitutions in the content of the included file:

.. code-block:: rst

   .. literalinclude:: path/to/file.txt
      :content-substitutions:

Replace substitutions in the file path:

.. code-block:: rst

   .. literalinclude:: path/to/|author|_file.txt
      :path-substitutions:

``image``
~~~~~~~~~

This adds a ``:path-substitutions:`` option to Sphinx's built-in `image`_ directive.

Replace substitutions in the image path:

.. code-block:: rst

   .. image:: path/to/|author|_diagram.png
      :path-substitutions:
      :alt: Diagram

MyST Markdown setup
-------------------

1. Add ``sphinx_substitution_extensions`` to ``extensions`` in ``conf.py`` to enable the extension:

.. code-block:: python

   """Configuration for Sphinx."""

   extensions = ["myst_parser"]  # Example existing extensions

   extensions += ["sphinx_substitution_extensions"]

2. Set the following variables in ``conf.py`` to define substitutions:

.. code-block:: python

   """Configuration for Sphinx."""

   myst_enable_extensions = ["substitution"]

   myst_substitutions = {
       "release": "0.1",
       "author": "Eleanor",
   }

This will replace ``|release|`` in the new directives with ``0.1``, and ``|author|`` with ``Eleanor``.

Enabling substitutions by default
----------------------------------

By default, you need to explicitly add the ``:substitutions:`` flag to ``code-block`` directives, and ``:content-substitutions:`` or ``:path-substitutions:`` flags to ``literalinclude`` directives.

If you want substitutions to be applied by default without needing these flags, you can set the following in ``conf.py``:

.. code-block:: python

   """Configuration for Sphinx."""

   substitutions_default_enabled = True

When this is enabled:

- All ``code-block`` directives will have substitutions applied automatically
- All ``literalinclude`` directives will have both content and path substitutions applied automatically

You can disable substitutions for specific directives when the default is enabled:

.. code-block:: rst

   .. code-block:: shell
      :nosubstitutions:

      echo "This |will| not be substituted"

   .. literalinclude:: path/to/file.txt
      :nocontent-substitutions:

   .. literalinclude:: path/to/|literal|_file.txt
      :nopath-substitutions:

Using substitutions in MyST Markdown
------------------------------------

``code-block``
~~~~~~~~~~~~~~

This adds a ``:substitutions:`` option to Sphinx's built-in `code-block`_ directive.

.. code-block:: markdown

   ```{code-block} bash
      :substitutions:

      echo "|author| released version |release|"
   ```

As well as using ``|author|``, you can also use ``{{author}}``.
This will respect the value of ``myst_sub_delimiters`` as set in ``conf.py``.

Inline ``:substitution-code:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   {substitution-code}`echo "|author| released version |release|"`

``substitution-download``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   {substitution-download}`|author|'s manuscript <|author|_manuscript.txt>`

``literalinclude``
~~~~~~~~~~~~~~~~~~

This adds ``:content-substitutions:`` and ``:path-substitutions:`` options to Sphinx's built-in `literalinclude`_ directive.

Replace substitutions in the content of the included file:

.. code-block:: markdown

   ```{literalinclude} path/to/file.txt
      :content-substitutions:
   ```

Replace substitutions in the file path:

.. code-block:: markdown

   ```{literalinclude} path/to/|author|_file.txt
      :path-substitutions:
   ```

``image``
~~~~~~~~~

This adds a ``:path-substitutions:`` option to Sphinx's built-in `image`_ directive.

Replace substitutions in the image path:

.. code-block:: markdown

   ```{image} path/to/|author|_diagram.png
      :path-substitutions:
      :alt: Diagram
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

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-substitution-extensions/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/sphinx-substitution-extensions/actions
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. _literalinclude: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude
.. _image: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-image
.. |PyPI| image:: https://badge.fury.io/py/Sphinx-Substitution-Extensions.svg
   :target: https://badge.fury.io/py/Sphinx-Substitution-Extensions
.. |minimum-python-version| replace:: 3.10
