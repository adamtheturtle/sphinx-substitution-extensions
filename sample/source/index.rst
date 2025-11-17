Samples for substitution directives and roles
=============================================

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

``code-block``
--------------

.. rest-example::

   .. code-block:: shell

      echo "The author is |author|"

   .. code-block:: shell
      :substitutions:

      echo "The author is |author|"

Inline ``:code:``
-----------------

.. rest-example::

    :code:`echo "The author is |author|"`

    :substitution-code:`echo "The author is |author|"`

Inline ``:download:``
---------------------

.. rest-example::

   .. We cannot use the substitution in the download target, because the download directive will error if the file does not exist.

   :download:`Script by |author| <../source/Eleanor.txt>`.

   :substitution-download:`Script by |author| <../source/|author|.txt>`.

``literalinclude``
------------------

Content substitutions
~~~~~~~~~~~~~~~~~~~~~

.. rest-example::

   .. literalinclude:: sample_include.txt

   .. literalinclude:: sample_include.txt
      :content-substitutions:

Path substitutions
~~~~~~~~~~~~~~~~~~

.. rest-example::

   .. literalinclude:: |author|.txt
      :path-substitutions:

``image``
---------

Path substitutions
~~~~~~~~~~~~~~~~~~

.. rest-example::

   .. image:: |author|_diagram.png
      :path-substitutions:
      :alt: Diagram for |author|

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
