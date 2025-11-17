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

Inline ``:substitution-code:``
------------------------------

```{code-block} markdown

   {substitution-code}`The author is {{author}}`
```

=>

{substitution-code}`The author is {{author}}`

``substitution-download``
-------------------------

```{code-block} markdown

   {substitution-download}`Script by {{author}} <../source/Eleanor.txt>`
```

=>

{substitution-download}`Script by {{author}} <../source/Eleanor.txt>`

``literalinclude``
------------------

### Content substitutions

```{code-block} markdown

    ```{literalinclude} sample_include.txt
    ```

    ```{literalinclude} sample_include.txt
    :content-substitutions:
    ```
```

=>

```{literalinclude} sample_include.txt
```

```{literalinclude} sample_include.txt
:content-substitutions:
```

### Path substitutions

```{code-block} markdown

    ```{literalinclude} {{author}}.txt
    :path-substitutions:
    ```
```

=>

```{literalinclude} {{author}}.txt
:path-substitutions:
```

``image``
---------

### Path substitutions

```{code-block} markdown

    ```{image} {{author}}_diagram.png
    :path-substitutions:
    :alt: Diagram for {{author}}
    ```
```

=>

```{image} {{author}}_diagram.png
:path-substitutions:
:alt: Diagram for {{author}}
```
