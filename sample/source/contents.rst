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
