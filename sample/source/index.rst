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

    .. substitution-prompt:: bash

       echo "The author is |author|"

=>

.. prompt:: bash

   echo "The author is |author|"

.. substitution-prompt:: bash

   echo "The author is |author|"

``code-block``
--------------

.. code-block:: rst

    .. code-block:: bash

       echo "The author is |author|"

    .. substitution-code-block:: bash

       echo "The author is |author|"

=>

.. code-block:: bash

   echo "The author is |author|"

.. substitution-code-block:: bash

   echo "The author is |author|"

Inline ``:code:``
-----------------

.. code-block:: rst

    :code:`echo "The author is |author|"`

    :substitution-code:`echo "The author is |author|"`

=>

:code:`echo "The author is |author|"`

:substitution-code:`echo "The author is |author|"`
