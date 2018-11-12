|Build Status|

# Sphinx Substitutions Extensions

Extensions for Sphinx which allow substitutions.

## Installation

## Setup

* Add the following to ``conf.py``: ``extensions += ['sphinx_substitution_extensions']``

* Set the following variable in ``conf.py``:

.. code:: python

   smart_prompt_placeholder_replace_pairs = (
       ('|release|', '0.1'),
       ('|author|', 'Eleanor'),
   )

This will replace ``|release|`` in the new directives

## Directives

Then use the following:

.. code:: rst

   .. smart-prompt:: bash

      echo "|author| released version |release|"

## Credits

### ``sphinx-prompt`` authors

Thanks to @sbrunner and other contributors for `sphinx-prompt <https://github.com/sbrunner/sphinx-prompt>`_.

### ClusterHQ

This package is largely inspired by code written for Flocker by ClusterHQ.

.. |Build Status| image:: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions.svg?branch=master
    :target: https://travis-ci.com/adamtheturtle/sphinx-substitution-extensions
