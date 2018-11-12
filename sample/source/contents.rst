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

       echo "|example_original|"

    .. substitution-prompt:: bash

       echo "|example_original|"

=>

.. prompt:: bash

   echo "|example_original|"

.. substitution-prompt:: bash

   echo "|example_original|"
