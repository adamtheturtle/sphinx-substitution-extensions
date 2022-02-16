Changelog
=========

.. contents::

Next
----

2022.02.16
------------

- Breaking change: The required Sphinx version is at least 4.0.
- ``sphinx-prompt`` is now an optional dependency.
  Thanks go to @dgarcia360 for this change.

2020.09.30.0
------------

2020.07.04.1
------------

- Ensure non-lower-case replacements can also be substituted in the inline substitution code role.

2020.07.04.0
------------

- Ensure non-lower-case replacements can also be substituted.
  Thanks go to @Julian for this change.

2020.05.30.0
------------

2020.05.27.0
------------

- Breaking change: Use ``:substitutions:`` option on ``code-block`` or ``prompt`` rather than new directives.

2020.05.23.0
------------

- Breaking change: Use the default Sphinx replacements, rather than a custom variable.
  Thanks go to @sbaudoin for the original code for this change.
  Please make a GitHub issue if you have a use case which this does not suit.

2020.04.05.0
------------

2020.02.21.0
------------

2019.12.28.1
------------

2019.12.28.0
------------

2019.06.15.0
------------

2019.04.04.1
------------

2019.04.04.0
------------

- Support Sphinx 2.0.0.

2018.11.12.3
------------

- Make ``substitution`` a list, not a tuple.

2018.11.12.2
------------

- Add ``substitution-code-block`` directive.

2018.11.12.0
------------

- Initial release with ``substitution-prompt``.
