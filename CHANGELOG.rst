Changelog
=========

.. contents::

Next
----

2025.01.02
----------

- Supports situations where there is no source file name available to the extension, such as when using ``sphinx_toolbox.rest_example``.

2024.10.17
----------

- Support Python 3.13.
- In MyST documents, support the ``myst_sub_delimiters`` option.
  This means you can use the ``{{replace-me}}`` syntax in MyST documents.

2024.08.06
------------

- Bump the minimum supported version of Sphinx to 7.3.5.
- Remove support for ``sphinx-prompt``.
  Please create a GitHub issue if you have a use case for this extension which is not covered by the built-in Sphinx functionality.

2024.02.25
------------

- Add ``substitution-download`` role.

2024.02.24.1
------------

- Add support for MyST.
  Thanks to Václav Votípka (@eNcacz) for the contribution.

2024.02.24
------------

- Bump the minimum supported version of Sphinx to 7.2.0.
- Bump the minimum supported version of docutils to 0.19.
- ``sphinx-prompt`` is no longer an optional dependency, meaning you can remove the ``[prompt]`` extras dependency specification.
- Remove the need to specify the ``sphinx-prompt`` extension in ``conf.py`` in order to use the ``prompt`` directive.
- Support Python 3.12
- Drop support for Python 3.9

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
