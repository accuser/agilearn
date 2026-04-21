# Built-in exceptions reference

This reference documents the most commonly used built-in exception classes in Python, their inheritance relationships, typical scenarios where each exception is raised, and practical examples.

For the complete list, see the [official Python documentation on built-in exceptions](https://docs.python.org/3/library/exceptions.html).

## Base exception classes

### `BaseException`

The root class for all built-in exceptions. You should not handle or inherit from `BaseException` directly in most cases. It exists to provide a common base for exceptions that should not normally be handled, such as `SystemExit` and `KeyboardInterrupt`.

```python
# BaseException is the root of the hierarchy
print(issubclass(Exception, BaseException))  # True
print(issubclass(KeyboardInterrupt, BaseException))  # True
```

### `Exception`

The base class for all built-in, non-system-exiting exceptions. All user-defined exceptions should inherit from `Exception` (or one of its subclasses), not from `BaseException`.

```python
class MyCustomError(Exception):
    """A custom exception that inherits from Exception."""
    pass
```

## Arithmetic exceptions

These exceptions relate to numeric operations.

### `ArithmeticError`

The base class for arithmetic exceptions. You can handle this to catch all arithmetic-related errors at once.

| Subclass | Description |
|----------|-------------|
| `ZeroDivisionError` | Division or modulo by zero |
| `OverflowError` | Result too large to represent |
| `FloatingPointError` | Floating-point operation failure (rare) |

### `ZeroDivisionError`

Raised when the second operand of a division or modulo operation is zero.

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(e)  # division by zero
```

**Common scenarios:**

- Division: `a / 0`
- Floor division: `a // 0`
- Modulo: `a % 0`

### `OverflowError`

Raised when the result of an arithmetic operation is too large to represent.

```python
import math

try:
    result = math.exp(1000)
except OverflowError as e:
    print(e)  # math range error
```

## Lookup exceptions

These exceptions occur when a key or index is not found.

### `LookupError`

The base class for lookup exceptions. Handle this to catch both `IndexError` and `KeyError`.

| Subclass | Description |
|----------|-------------|
| `IndexError` | Sequence index out of range |
| `KeyError` | Dictionary key not found |

### `IndexError`

Raised when a sequence subscript is out of range.

```python
numbers = [1, 2, 3]

try:
    value = numbers[10]
except IndexError as e:
    print(e)  # list index out of range
```

### `KeyError`

Raised when a dictionary key is not found.

```python
data = {"name": "Alice"}

try:
    email = data["email"]
except KeyError as e:
    print(e)  # 'email'
```

**Tip:** Use `dict.get(key, default)` to avoid `KeyError` when a default value is acceptable.

```python
email = data.get("email", "not provided")
```

## Type and value exceptions

### `TypeError`

Raised when an operation or function is applied to an object of an inappropriate type.

```python
try:
    result = "hello" + 5
except TypeError as e:
    print(e)  # can only concatenate str (not "int") to str
```

**Common scenarios:**

- Unsupported operand types: `"hello" + 5`
- Wrong argument type: `len(42)`
- Wrong number of arguments: `int("1", "2", "3")`

### `ValueError`

Raised when a function receives an argument of the correct type but an inappropriate value.

```python
try:
    number = int("hello")
except ValueError as e:
    print(e)  # invalid literal for int() with base 10: 'hello'
```

**Common scenarios:**

- Invalid conversion: `int("abc")`
- Inappropriate value: `math.sqrt(-1)`
- Value out of range: `int("", base=10)`

## Attribute and name exceptions

### `AttributeError`

Raised when an attribute reference or assignment fails.

```python
try:
    "hello".nonexistent_method()
except AttributeError as e:
    print(e)  # 'str' object has no attribute 'nonexistent_method'
```

### `NameError`

Raised when a local or global name is not found.

```python
try:
    print(undefined_variable)
except NameError as e:
    print(e)  # name 'undefined_variable' is not defined
```

## Operating system exceptions

These exceptions relate to operating system operations, particularly file and network operations.

### `OSError`

The base class for operating system exceptions. In Python 3, several specific exceptions inherit from `OSError`.

| Subclass | Description |
|----------|-------------|
| `FileNotFoundError` | File or directory not found |
| `FileExistsError` | File or directory already exists |
| `PermissionError` | Insufficient permissions |
| `IsADirectoryError` | File operation on a directory |
| `NotADirectoryError` | Directory operation on a file |
| `TimeoutError` | Operation timed out |
| `ConnectionError` | Connection-related issues |

### `FileNotFoundError`

Raised when a file or directory is requested but does not exist.

```python
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError as e:
    print(e)  # [Errno 2] No such file or directory: 'nonexistent.txt'
```

### `FileExistsError`

Raised when trying to create a file or directory that already exists.

```python
import os

try:
    os.mkdir("/tmp")
except FileExistsError as e:
    print(f"Directory already exists: {e}")
```

### `PermissionError`

Raised when an operation lacks sufficient permissions.

```python
try:
    with open("/etc/shadow", "r") as f:
        content = f.read()
except PermissionError as e:
    print(f"Access denied: {e}")
```

### `ConnectionError`

The base class for connection-related exceptions.

| Subclass | Description |
|----------|-------------|
| `ConnectionRefusedError` | Connection refused by the target |
| `ConnectionResetError` | Connection reset by the peer |
| `ConnectionAbortedError` | Connection aborted |
| `BrokenPipeError` | Broken pipe |

## Import exceptions

### `ImportError`

Raised when an import statement fails.

```python
try:
    import nonexistent_module
except ImportError as e:
    print(e)  # No module named 'nonexistent_module'
```

### `ModuleNotFoundError`

A subclass of `ImportError`, raised when a module cannot be found. This was added in Python 3.6.

```python
try:
    import nonexistent_module
except ModuleNotFoundError as e:
    print(e)  # No module named 'nonexistent_module'
```

## Iteration exceptions

### `StopIteration`

Raised by the `next()` function to indicate that there are no further items to produce.

```python
iterator = iter([1, 2])
print(next(iterator))  # 1
print(next(iterator))  # 2

try:
    next(iterator)
except StopIteration:
    print("No more items")
```

## Warning categories

Warnings are not exceptions in the traditional sense, but they inherit from `Warning`, which inherits from `Exception`. Common warning categories include the following:

| Warning | Description |
|---------|-------------|
| `DeprecationWarning` | Feature will be removed in a future version |
| `FutureWarning` | Behaviour will change in a future version |
| `RuntimeWarning` | Suspicious runtime behaviour |
| `UserWarning` | User-defined warnings |

## System-exiting exceptions

These exceptions inherit from `BaseException` but **not** from `Exception`. They should not normally be handled in application code.

| Exception | Description |
|-----------|-------------|
| `SystemExit` | Raised by `sys.exit()` |
| `KeyboardInterrupt` | Raised when the user presses Ctrl+C |
| `GeneratorExit` | Raised when a generator is closed |

!!! warning
    Do not handle `SystemExit` or `KeyboardInterrupt` unless you have a specific reason and re-raise them afterwards. Handling these exceptions prevents the user from stopping your program.

## Quick lookup table

| Exception | Parent | Common cause |
|-----------|--------|--------------|
| `ZeroDivisionError` | `ArithmeticError` | `a / 0` |
| `OverflowError` | `ArithmeticError` | `math.exp(1000)` |
| `IndexError` | `LookupError` | `list[999]` |
| `KeyError` | `LookupError` | `dict["missing"]` |
| `ValueError` | `Exception` | `int("abc")` |
| `TypeError` | `Exception` | `"a" + 1` |
| `AttributeError` | `Exception` | `obj.missing_attr` |
| `NameError` | `Exception` | Using undefined variable |
| `FileNotFoundError` | `OSError` | `open("missing.txt")` |
| `PermissionError` | `OSError` | Accessing restricted file |
| `ImportError` | `Exception` | `import nonexistent` |
| `StopIteration` | `Exception` | `next()` on exhausted iterator |

## Further reading

- [Python Built-in Exceptions documentation](https://docs.python.org/3/library/exceptions.html)
- [Exception hierarchy reference](exception-hierarchy-reference.md) for a complete tree diagram
- [Try/except syntax reference](try-except-syntax-reference.md) for handling these exceptions
