Samples for substitution directives
===================================

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

``prompt``
----------

.. code-block:: rst

    .. prompt:: bash

       echo "The author is |author|"

    .. prompt:: bash
       :substitutions:

       echo "The author is |author|"

=>

.. prompt:: bash

   echo "The author is |author|"

.. prompt:: bash
   :substitutions:

   echo "The author is |author|"

``code-block``
--------------

.. code-block:: rst

    .. code-block:: bash

       echo "The author is |author|"

    .. code-block:: bash
       :substitutions:

       echo "The author is |author|"

=>

.. code-block:: bash

   echo "The author is |author|"

.. code-block:: bash
   :substitutions:

   echo "The author is |author|"

Inline ``:code:``
-----------------

.. code-block:: rst

    :code:`echo "The author is |author|"`

    :substitution-code:`echo "The author is |author|"`

=>

:code:`echo "The author is |author|"`

:substitution-code:`echo "The author is |author|"`

..

  This is a test of parallel document builds. You need at least 5
  documents. See:
  https://github.com/adamtheturtle/sphinx-substitution-extensions/pull/173

.. toctree::
   :hidden:

   one
   two
   three
   four
   five
