Samples for substitution directives and roles
=============================================

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

Inline ``:download:``
---------------------

.. code-block:: rst


    .. We cannot use the substitution in the download target, because
    .. the download directive will error if the file does not exist.
    :download:`Script by |author| <../source/Eleanor.txt>`.

    :substitution-download:`Script by |author| <../source/|author|.txt>`.

=>

:download:`Script by |author| <../source/Eleanor.txt>`.

:substitution-download:`Script by |author| <../source/|author|.txt>`.


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


.. toctree::
   markdown_sample
