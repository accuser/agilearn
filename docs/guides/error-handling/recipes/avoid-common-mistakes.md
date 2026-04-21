# Avoid common error handling mistakes

Error handling code that is poorly written can introduce subtle bugs, hide real problems, and make your code harder to debug. This guide identifies the most common anti-patterns in exception handling and shows you how to avoid them.

## The problem

Many developers, especially those new to Python, fall into common traps when writing exception handling code. These mistakes can lead to silent failures, lost error information, and code that is difficult to maintain.

## Mistake 1: Using bare `except`

A bare `except` clause (without specifying an exception type) catches **everything**, including `KeyboardInterrupt` and `SystemExit`. This prevents users from stopping your program with Ctrl+C and can mask serious errors.

**Do not do this:**

```python
try:
    result = process_data(data)
except:
    print("Something went wrong")
```

**Do this instead:**

```python
try:
    result = process_data(data)
except ValueError:
    print("Invalid data format")
except TypeError:
    print("Unexpected data type")
```

If you genuinely need to handle all standard exceptions, use `except Exception` rather than a bare `except`. This still allows `KeyboardInterrupt` and `SystemExit` to propagate normally.

```python
try:
    result = process_data(data)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## Mistake 2: Swallowing exceptions silently

Handling an exception without logging, re-raising, or otherwise responding to it hides errors and makes debugging nearly impossible.

**Do not do this:**

```python
try:
    config = load_config("settings.conf")
except FileNotFoundError:
    pass  # Silently ignore the missing file
```

**Do this instead:**

```python
import logging

logger = logging.getLogger(__name__)

try:
    config = load_config("settings.conf")
except FileNotFoundError:
    logger.warning("Configuration file not found, using defaults")
    config = DEFAULT_CONFIG
```

If you must ignore an exception, add a comment explaining why it is safe to do so.

```python
try:
    os.remove(temp_file)
except FileNotFoundError:
    # The file was already deleted by another process; this is expected
    pass
```

## Mistake 3: Catching too broadly

Handling `Exception` when you only expect specific exceptions hides bugs in your code.

**Do not do this:**

```python
def get_user_age(data: dict) -> int:
    """Extract the user age from a data dictionary."""
    try:
        return int(data["age"])
    except Exception:
        return 0
```

This hides `KeyError` (if `"age"` is missing), `TypeError` (if `data` is not a dictionary), and any other unexpected exceptions.

**Do this instead:**

```python
def get_user_age(data: dict) -> int:
    """Extract the user age from a data dictionary."""
    try:
        return int(data["age"])
    except KeyError:
        print("Age field is missing from the data")
        return 0
    except ValueError:
        print(f"Age value is not a valid integer: {data['age']!r}")
        return 0
```

## Mistake 4: Using exceptions for flow control

Exceptions should represent exceptional conditions, not expected program flow. Using them as a substitute for `if`/`else` statements makes code harder to read and slower to execute.

**Do not do this:**

```python
def is_positive(number: float) -> bool:
    """Check whether a number is positive."""
    try:
        if number <= 0:
            raise ValueError("Not positive")
        return True
    except ValueError:
        return False
```

**Do this instead:**

```python
def is_positive(number: float) -> bool:
    """Check whether a number is positive."""
    return number > 0
```

However, there are cases where using exceptions is the Pythonic approach. The "easier to ask for forgiveness than permission" (EAFP) pattern is appropriate when the exceptional case is genuinely rare.

```python
# EAFP style: appropriate when the key usually exists
def get_cached_value(cache: dict, key: str) -> str | None:
    """Get a value from the cache."""
    try:
        return cache[key]
    except KeyError:
        return None
```

## Mistake 5: Putting too much code in the `try` block

A `try` block should contain only the code that might raise the exception you are handling. Including unrelated code makes it harder to identify the source of an exception.

**Do not do this:**

```python
try:
    filepath = build_filepath(name)
    content = read_file(filepath)
    data = parse_content(content)
    result = process_data(data)
    save_result(result)
except FileNotFoundError:
    print("File not found")
```

If `parse_content` or `process_data` accidentally raises `FileNotFoundError`, this code would incorrectly report "File not found" when the real problem is elsewhere.

**Do this instead:**

```python
filepath = build_filepath(name)

try:
    content = read_file(filepath)
except FileNotFoundError:
    print(f"File not found: {filepath}")
    content = ""

if content:
    data = parse_content(content)
    result = process_data(data)
    save_result(result)
```

## Mistake 6: Losing the original exception context

When raising a new exception inside an `except` block, use exception chaining (`raise ... from ...`) to preserve the original exception information.

**Do not do this:**

```python
try:
    value = int(raw_input)
except ValueError:
    raise RuntimeError("Invalid input")
```

This discards the original `ValueError`, making it harder to debug.

**Do this instead:**

```python
try:
    value = int(raw_input)
except ValueError as e:
    raise RuntimeError("Invalid input") from e
```

The `from e` clause preserves the original exception as the `__cause__` attribute, so the full chain of errors is visible in the traceback.

## Mistake 7: Not cleaning up resources

Failing to release resources (files, connections, locks) when exceptions occur leads to resource leaks.

**Do not do this:**

```python
f = open("data.txt", "r", encoding="utf-8")
data = f.read()
f.close()  # This line never runs if f.read() raises an exception
```

**Do this instead:**

```python
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()
# The file is closed automatically, even if an exception occurs
```

Always use context managers (the `with` statement) for resources that need cleanup. See the [Use context managers](use-context-managers.ipynb) guide for more details.

## Quick reference: dos and do-nots

| Do | Do not |
|----|--------|
| Handle specific exception types | Use bare `except` |
| Log or respond to handled exceptions | Swallow exceptions silently |
| Keep `try` blocks small and focused | Wrap large blocks of code in `try` |
| Use context managers for resources | Rely on manual cleanup after `try` |
| Use exception chaining (`from e`) | Discard original exception context |
| Use exceptions for exceptional conditions | Use exceptions for normal flow control |
| Add descriptive error messages | Raise exceptions without messages |

## Related guides

- [Create custom exceptions](create-custom-exceptions.ipynb) for building your own exception classes
- [Handle multiple exceptions](handle-multiple-exceptions.ipynb) for working with different exception types
- [Use context managers](use-context-managers.ipynb) for reliable resource cleanup
