Samples for substitution directives in Markdown
===============================================

Configuration
-------------

```{literalinclude} conf.py
:language: python
```

``code-block``
--------------

```{code-block} markdown

    ```{code-block} markdown

       echo "The author is |author|"
    ```

    ```{code-block} markdown
    :substitutions:

       echo "The author is |author|"
    ```

    or, with the value of the `myst_sub_delimiters` `conf.py` setting:

    ```{code-block} markdown

       echo "The author is {{author}}"
    ```

    ```{code-block} markdown
    :substitutions:

       echo "The author is {{author}}"
    ```
```

=>

```{code-block} markdown

    echo "The author is |author|"
```

```{code-block} markdown
    :substitutions:

    echo "The author is |author|"
```

```{code-block} markdown

    echo "The author is {{author}}"
```

```{code-block} markdown
    :substitutions:

    echo "The author is {{author}}"
```
