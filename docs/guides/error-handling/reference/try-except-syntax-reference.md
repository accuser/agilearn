# Try/except syntax reference

This reference covers the complete syntax for `try`/`except`/`else`/`finally` blocks in Python, including all valid forms, clause ordering, and usage patterns.

## Basic syntax

### `try`/`except`

The simplest form handles a specific exception type.

```python
try:
    result = int("hello")
except ValueError:
    print("Conversion failed")
```

### `try`/`except` with exception variable

Use `as` to bind the exception object to a variable.

```python
try:
    result = int("hello")
except ValueError as e:
    print(f"Conversion failed: {e}")
```

The variable `e` is only available inside the `except` block. Python automatically deletes it when the block ends.

## Clause ordering

The clauses must appear in the following order:

```python
try:
    # Required: code that might raise an exception
    pass
except SomeException:
    # Optional: handle specific exceptions (one or more except clauses)
    pass
else:
    # Optional: runs only if no exception occurred in try
    pass
finally:
    # Optional: always runs, regardless of exceptions
    pass
```

### Valid combinations

| Combination | Use case |
|-------------|----------|
| `try`/`except` | Handle specific exceptions |
| `try`/`except`/`else` | Handle exceptions and run success code |
| `try`/`except`/`finally` | Handle exceptions with guaranteed cleanup |
| `try`/`except`/`else`/`finally` | Full exception handling with cleanup |
| `try`/`finally` | Guaranteed cleanup without handling exceptions |

!!! note
    You must have at least one `except` or `finally` clause. A `try` block on its own is a syntax error.

## The `except` clause

### Handling a single exception type

```python
try:
    value = my_dict["key"]
except KeyError:
    value = "default"
```

### Handling multiple exception types (tuple)

List exception types in a tuple to handle them identically.

```python
try:
    result = float(value)
except (ValueError, TypeError):
    result = 0.0
```

### Multiple `except` clauses

Use separate clauses to handle different exception types differently. Python checks each clause in order and executes the first match.

```python
try:
    data = load_and_parse(filepath)
except FileNotFoundError:
    print("File not found")
    data = {}
except ValueError as e:
    print(f"Invalid data: {e}")
    data = {}
except PermissionError:
    print("Access denied")
    data = {}
```

### Ordering of `except` clauses

Place more specific exception types before more general ones. Python uses the first matching clause, so a parent class placed first will handle all its child exceptions.

```python
# Correct: specific before general
try:
    result = operation()
except FileNotFoundError:
    print("File not found")
except OSError:
    print("OS error (not FileNotFoundError)")
except Exception:
    print("Some other exception")
```

```python
# Incorrect: OSError catches FileNotFoundError before the specific clause
try:
    result = operation()
except OSError:
    print("This handles FileNotFoundError too!")
except FileNotFoundError:
    # This clause is unreachable
    print("Never reached")
```

### Bare `except` (not recommended)

A bare `except` clause handles all exceptions, including `KeyboardInterrupt` and `SystemExit`.

```python
# Not recommended: catches everything
try:
    result = operation()
except:
    print("Something went wrong")
```

!!! warning
    Avoid bare `except` clauses. They catch `KeyboardInterrupt` and `SystemExit`, preventing the user from stopping the program. Use `except Exception` if you need a broad handler.

### Handling `Exception` as a fallback

Use `except Exception` as a last resort to handle unexpected exceptions whilst still allowing `KeyboardInterrupt` and `SystemExit` to propagate.

```python
try:
    result = operation()
except ValueError:
    print("Expected error")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")
```

## The `else` clause

The `else` clause runs only if the `try` block completed without raising an exception. This is useful for separating the code that might raise an exception from the code that should only run on success.

```python
try:
    value = int(user_input)
except ValueError:
    print("Invalid input")
else:
    print(f"You entered: {value}")
```

### Why use `else` instead of putting code in `try`?

Code in the `else` block is not protected by the `except` clause. This prevents accidentally handling exceptions raised by the success code.

```python
# With else: exceptions from process() are NOT caught
try:
    data = load(filepath)
except FileNotFoundError:
    data = {}
else:
    result = process(data)  # If this raises FileNotFoundError, it propagates

# Without else: exceptions from process() ARE caught (possibly incorrectly)
try:
    data = load(filepath)
    result = process(data)  # A FileNotFoundError here would be caught below
except FileNotFoundError:
    data = {}
```

## The `finally` clause

The `finally` clause always runs, regardless of whether an exception occurred, whether it was handled, or whether a `return` statement was executed.

```python
f = open("data.txt", "r", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()
```

### `finally` behaviour with `return`

If both a `try` (or `except`) block and the `finally` block contain `return` statements, the `finally` return value takes precedence.

```python
def example() -> str:
    """Demonstrate that finally overrides other return values."""
    try:
        return "from try"
    finally:
        return "from finally"  # This value is returned

# Returns "from finally"
```

!!! warning
    Avoid placing `return` statements inside `finally` blocks. This overrides any return value from `try` or `except`, which can lead to confusing behaviour.

### `try`/`finally` without `except`

You can use `try`/`finally` without any `except` clause to guarantee cleanup without handling the exception.

```python
resource = acquire_resource()
try:
    use_resource(resource)
finally:
    release_resource(resource)
```

If an exception occurs in `use_resource()`, the `finally` block runs and then the exception propagates to the caller.

## The `raise` statement

### Raising an exception

```python
raise ValueError("Age must be positive")
```

### Re-raising the current exception

Inside an `except` block, a bare `raise` re-raises the current exception.

```python
try:
    result = operation()
except ValueError as e:
    log_error(e)
    raise  # Re-raises the same ValueError
```

### Exception chaining with `from`

Use `raise ... from ...` to indicate that one exception was caused by another.

```python
try:
    value = int(raw_input)
except ValueError as e:
    raise RuntimeError("Failed to process input") from e
```

The original exception is stored in the `__cause__` attribute of the new exception and is displayed in the traceback.

### Suppressing exception context with `from None`

Use `from None` to suppress the implicit exception context.

```python
try:
    value = int(raw_input)
except ValueError:
    raise RuntimeError("Invalid input") from None
```

## Exception attributes

All exceptions have the following attributes:

| Attribute | Description |
|-----------|-------------|
| `args` | Tuple of arguments passed to the exception constructor |
| `__cause__` | The explicit cause (set by `raise ... from ...`) |
| `__context__` | The implicit context (set when raising during exception handling) |
| `__traceback__` | The traceback object associated with the exception |
| `__suppress_context__` | Whether to suppress the implicit context in display |

```python
try:
    int("hello")
except ValueError as e:
    print(f"args: {e.args}")
    print(f"__cause__: {e.__cause__}")
    print(f"__context__: {e.__context__}")
```

## The `assert` statement

The `assert` statement raises `AssertionError` if a condition is false. It is primarily used for debugging and testing.

```python
def calculate_discount(price: float, percentage: float) -> float:
    """Calculate a discounted price."""
    assert 0 <= percentage <= 100, f"Percentage must be 0-100, got {percentage}"
    return price * (1 - percentage / 100)
```

!!! warning
    Do not use `assert` for input validation in production code. Assertions can be disabled by running Python with the `-O` (optimise) flag, which would skip your validation entirely.

## Further reading

- [Built-in exceptions reference](built-in-exceptions-reference.md) for details on specific exception types
- [Exception hierarchy reference](exception-hierarchy-reference.md) for the complete class hierarchy
- [Python Errors and Exceptions tutorial](https://docs.python.org/3/tutorial/errors.html) in the official documentation
