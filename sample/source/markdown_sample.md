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
```

=>

```{code-block} markdown

    echo "The author is |author|"
```

```{code-block} markdown
    :substitutions:

    echo "The author is |author|"
```
