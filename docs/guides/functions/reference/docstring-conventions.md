# Docstring conventions

This reference covers the conventions for writing docstrings in Python functions, including the three major styles and how to access docstrings programmatically.

## What is a docstring?

A docstring is a string literal that appears as the first statement in a function, class, module, or method body. Python stores it in the `__doc__` attribute of the object.

```python
def greet(name):
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

print(greet.__doc__)
# Return a greeting for the given name.
```

## PEP 257 summary

PEP 257 is the Python Enhancement Proposal that establishes docstring conventions. The key requirements are as follows:

- Write docstrings for all public modules, functions, classes, and methods.
- Use triple double quotes (`"""`) for all docstrings.
- The closing `"""` should be on a line by itself for multi-line docstrings.
- The first line should be a concise summary.
- Use a period at the end of the summary line.
- Write the summary as a phrase ending with a period, not as a full sentence describing the function.
- Use imperative mood for the summary ("Return a value", not "Returns a value").

## Single-line docstrings

Use a single-line docstring for simple functions where the purpose is immediately obvious.

```python
def square(n):
    """Return the square of n."""
    return n ** 2
```

Rules for single-line docstrings:

- Place everything on one line, including the triple quotes.
- Do not leave a blank line before or after the docstring.
- Write as a phrase, not a complete sentence.
- End with a period.

## Multi-line docstrings

Use multi-line docstrings when the function requires further explanation, parameter documentation, or examples.

```python
def divide(a, b):
    """Return the result of dividing a by b.

    The function performs floating-point division. If b is zero,
    a ZeroDivisionError is raised.
    """
    return a / b
```

Structure of a multi-line docstring:

1. Summary line (same line as opening `"""`).
2. Blank line.
3. Extended description (one or more paragraphs).
4. Closing `"""` on its own line.

## Google style

Google style uses indented section headers with colons. It is widely used and readable in both source code and generated documentation.

### Full example

```python
def send_message(recipient, message, priority=1, retry=True):
    """Send a message to a recipient.

    Formats the message and delivers it to the specified recipient
    through the messaging system. Messages are queued and delivered
    in order of priority.

    Args:
        recipient: The address of the message recipient.
        message: The content of the message to send.
        priority: The delivery priority from 1 (lowest) to 5
            (highest). Defaults to 1.
        retry: Whether to retry on failure. Defaults to True.

    Returns:
        A dictionary containing the delivery status with the
        following keys:
            - "status": Either "sent" or "failed".
            - "timestamp": The time the message was sent.

    Raises:
        ValueError: If priority is not between 1 and 5.
        ConnectionError: If the messaging service is unavailable.

    Examples:
        >>> send_message("alice@example.com", "Hello!")
        {'status': 'sent', 'timestamp': '2024-01-15T10:30:00'}

    Notes:
        Messages exceeding 1000 characters are automatically
        truncated before delivery.
    """
```

### Google style sections

| Section | Purpose |
|---------|---------|
| `Args:` | Document each parameter (name, description, default) |
| `Returns:` | Describe the return value and its type |
| `Raises:` | List exceptions the function may raise |
| `Examples:` | Show usage with interactive Python examples |
| `Notes:` | Additional information or caveats |
| `Attributes:` | Document class attributes (for classes) |
| `Yields:` | Describe yielded values (for generators) |
| `Todo:` | List planned changes or known issues |

## NumPy style

NumPy style uses underlined section headers. It is common in the scientific Python community and provides clear visual separation between sections.

### Full example

```python
def calculate_mean(values, weights=None):
    """Calculate the arithmetic or weighted mean of a sequence of values.

    Computes the simple arithmetic mean when no weights are provided.
    When weights are given, computes the weighted mean instead.

    Parameters
    ----------
    values : list of float
        The numerical values to average. Must not be empty.
    weights : list of float, optional
        The weight for each value. Must be the same length as
        `values`. If not provided, all values are weighted equally.

    Returns
    -------
    float
        The computed mean.

    Raises
    ------
    ValueError
        If `values` is empty.
    ValueError
        If `weights` and `values` have different lengths.

    Examples
    --------
    >>> calculate_mean([1, 2, 3])
    2.0
    >>> calculate_mean([1, 2, 3], weights=[3, 1, 1])
    1.6

    Notes
    -----
    This function does not handle NaN values. Filter them
    before passing to this function.
    """
```

### NumPy style sections

| Section | Purpose |
|---------|---------|
| `Parameters` | Document each parameter with type and description |
| `Returns` | Describe each return value with type |
| `Raises` | List exceptions with descriptions |
| `Examples` | Show usage with interactive Python examples |
| `Notes` | Additional information |
| `See Also` | Related functions or classes |
| `References` | Citations or links |
| `Yields` | Describe yielded values (for generators) |

## Sphinx (reStructuredText) style

Sphinx style uses reStructuredText field list syntax. It integrates directly with the Sphinx documentation generator.

### Full example

```python
def find_element(collection, predicate, default=None):
    """Find the first element matching a predicate.

    Iterates through the collection and returns the first element
    for which the predicate function returns ``True``.

    :param collection: The iterable to search through.
    :type collection: list
    :param predicate: A function that takes an element and returns
        ``True`` or ``False``.
    :type predicate: callable
    :param default: The value to return if no match is found.
        Defaults to ``None``.
    :type default: object, optional
    :returns: The first matching element, or `default` if no match
        is found.
    :rtype: object
    :raises TypeError: If `predicate` is not callable.

    .. code-block:: python

        >>> find_element([1, 2, 3, 4], lambda x: x > 2)
        3
        >>> find_element([1, 2], lambda x: x > 5, default=-1)
        -1
    """
```

### Sphinx style fields

| Field | Purpose |
|-------|---------|
| `:param name:` | Describe a parameter |
| `:type name:` | Specify the type of a parameter |
| `:returns:` | Describe the return value |
| `:rtype:` | Specify the return type |
| `:raises ExceptionType:` | Document an exception |

## Comparison of styles

| Feature | Google | NumPy | Sphinx |
|---------|--------|-------|--------|
| Readability in source | Excellent | Good | Moderate |
| Visual separation | Indentation | Underlines | Field markers |
| Tool support | Sphinx (Napoleon), MkDocs | Sphinx (Napoleon), MkDocs | Sphinx (native) |
| Verbosity | Low | Medium | Medium |
| Common in | General Python, web development | Scientific Python, data science | Older Python projects |
| Type in docstring | Optional (inline) | Alongside parameter name | Separate `:type:` field |

**Recommendation:** Google style is a good default choice for most projects. It balances readability with completeness and is supported by all major documentation tools.

## Accessing docstrings programmatically

### The `__doc__` attribute

Every function, class, and module has a `__doc__` attribute containing its docstring (or `None` if no docstring is present).

```python
def add(a, b):
    """Return the sum of a and b."""
    return a + b

print(add.__doc__)
# Return the sum of a and b.
```

### The `help()` function

The `help()` built-in displays formatted documentation, including the docstring, in an interactive session.

```python
help(add)
# Help on function add in module __main__:
#
# add(a, b)
#     Return the sum of a and b.
```

### `inspect.getdoc()`

The `inspect.getdoc()` function retrieves the docstring with leading whitespace cleaned up and tabs expanded.

```python
import inspect

def example():
    """
    This docstring has inconsistent
        indentation that getdoc will clean up.
    """
    pass

print(inspect.getdoc(example))
# This docstring has inconsistent
#     indentation that getdoc will clean up.
```

### `inspect.cleandoc()`

For more aggressive cleaning (removing leading blank lines and uniform indentation), use `inspect.cleandoc()`.

```python
import inspect

raw = """
    First line.
    Second line.
    Third line.
"""

print(inspect.cleandoc(raw))
# First line.
# Second line.
# Third line.
```

## Docstrings and type hints together

When using type hints in the function signature, avoid duplicating type information in the docstring.

### Without type hints (types in docstring)

```python
def repeat(text, count):
    """Repeat a string a given number of times.

    Args:
        text (str): The text to repeat.
        count (int): The number of repetitions.

    Returns:
        str: The repeated text.
    """
    return text * count
```

### With type hints (types omitted from docstring)

```python
def repeat(text: str, count: int) -> str:
    """Repeat a string a given number of times.

    Args:
        text: The text to repeat.
        count: The number of repetitions.

    Returns:
        The repeated text.
    """
    return text * count
```

When type hints are present in the signature, keeping types out of the docstring avoids duplication and reduces the risk of the two falling out of sync.

## Best practices checklist

- Write a docstring for every public function, class, and module.
- Use triple double quotes (`"""`) for all docstrings.
- Start with a concise summary line in imperative mood.
- End the summary line with a period.
- Separate the summary from the body with a blank line.
- Document all parameters, including defaults and constraints.
- Document the return value and its type (or rely on type hints).
- Document any exceptions the function may raise.
- Include examples for functions with non-obvious behaviour.
- Choose one style (Google, NumPy, or Sphinx) and use it consistently throughout the project.
- Do not duplicate type information when type hints are present in the signature.
- Keep docstrings up to date when the function changes.
- Verify docstrings render correctly with your documentation tool.
