# Exception hierarchy reference

This reference provides the full built-in exception class hierarchy in Python, showing how all exceptions relate to `BaseException` and `Exception`. Use this as a quick visual reference when deciding which exception to handle or where to place a custom exception in the hierarchy.

## Complete hierarchy diagram

The following diagram shows the complete built-in exception hierarchy in Python 3.12. Indentation indicates inheritance.

```
BaseException
├── BaseExceptionGroup
├── GeneratorExit
├── KeyboardInterrupt
├── SystemExit
└── Exception
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── AssertionError
    ├── AttributeError
    ├── BlockingIOError
    ├── BrokenPipeError
    ├── BufferError
    ├── ChildProcessError
    ├── ConnectionAbortedError
    ├── ConnectionError
    │   ├── BrokenPipeError
    │   ├── ConnectionAbortedError
    │   ├── ConnectionRefusedError
    │   └── ConnectionResetError
    ├── ConnectionRefusedError
    ├── ConnectionResetError
    ├── EOFError
    ├── EnvironmentError (alias for OSError)
    ├── ExceptionGroup
    ├── FileExistsError
    ├── FileNotFoundError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── InterruptedError
    ├── IOError (alias for OSError)
    ├── IsADirectoryError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── MemoryError
    ├── NameError
    │   └── UnboundLocalError
    ├── NotADirectoryError
    ├── NotImplementedError
    ├── OSError
    │   ├── BlockingIOError
    │   ├── ChildProcessError
    │   ├── ConnectionError
    │   │   ├── BrokenPipeError
    │   │   ├── ConnectionAbortedError
    │   │   ├── ConnectionRefusedError
    │   │   └── ConnectionResetError
    │   ├── FileExistsError
    │   ├── FileNotFoundError
    │   ├── InterruptedError
    │   ├── IsADirectoryError
    │   ├── NotADirectoryError
    │   ├── PermissionError
    │   ├── ProcessLookupError
    │   └── TimeoutError
    ├── OverflowError
    ├── PermissionError
    ├── ProcessLookupError
    ├── RecursionError
    ├── ReferenceError
    ├── RuntimeError
    │   ├── NotImplementedError
    │   └── RecursionError
    ├── StopAsyncIteration
    ├── StopIteration
    ├── SyntaxError
    │   └── IndentationError
    │       └── TabError
    ├── SystemError
    ├── TimeoutError
    ├── TypeError
    ├── UnicodeDecodeError
    ├── UnicodeEncodeError
    ├── UnicodeError
    │   ├── UnicodeDecodeError
    │   ├── UnicodeEncodeError
    │   └── UnicodeTranslateError
    ├── UnicodeTranslateError
    ├── ValueError
    │   └── UnicodeError
    │       ├── UnicodeDecodeError
    │       ├── UnicodeEncodeError
    │       └── UnicodeTranslateError
    └── Warning
        ├── BytesWarning
        ├── DeprecationWarning
        ├── EncodingWarning
        ├── FutureWarning
        ├── ImportWarning
        ├── PendingDeprecationWarning
        ├── ResourceWarning
        ├── RuntimeWarning
        ├── SyntaxWarning
        ├── UnicodeWarning
        └── UserWarning
```

## Simplified hierarchy for common use

The following simplified diagram shows only the exceptions you are most likely to encounter and handle in everyday code.

```
BaseException
├── KeyboardInterrupt          # User pressed Ctrl+C
├── SystemExit                 # sys.exit() was called
└── Exception                  # Base for all standard exceptions
    ├── ArithmeticError
    │   └── ZeroDivisionError  # Division by zero
    ├── AttributeError         # Missing attribute
    ├── ImportError             # Import failed
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError         # List index out of range
    │   └── KeyError           # Dictionary key not found
    ├── NameError              # Undefined variable
    ├── OSError
    │   ├── FileExistsError    # File already exists
    │   ├── FileNotFoundError  # File not found
    │   ├── PermissionError    # Insufficient permissions
    │   └── TimeoutError       # Operation timed out
    ├── RuntimeError           # Generic runtime error
    ├── StopIteration          # Iterator exhausted
    ├── TypeError              # Wrong type
    └── ValueError             # Wrong value
```

## Key groupings

### Exceptions you should not normally handle

These exceptions inherit from `BaseException` but not from `Exception`. They represent system-level events, not application errors.

| Exception | Purpose |
|-----------|---------|
| `KeyboardInterrupt` | The user pressed Ctrl+C to stop the program |
| `SystemExit` | The program called `sys.exit()` |
| `GeneratorExit` | A generator or coroutine was closed |

Using `except Exception` rather than bare `except` ensures these exceptions propagate normally.

### Arithmetic exceptions (`ArithmeticError`)

All arithmetic-related exceptions inherit from `ArithmeticError`.

| Exception | Common cause |
|-----------|-------------|
| `ZeroDivisionError` | `x / 0`, `x // 0`, `x % 0` |
| `OverflowError` | `math.exp(1000)` |
| `FloatingPointError` | Rarely raised in practice |

### Lookup exceptions (`LookupError`)

All lookup-related exceptions inherit from `LookupError`.

| Exception | Common cause |
|-----------|-------------|
| `IndexError` | Accessing a list with an out-of-range index |
| `KeyError` | Accessing a dictionary with a missing key |

### Operating system exceptions (`OSError`)

All operating system exceptions inherit from `OSError`. These are commonly encountered when working with files and network connections.

| Exception | Common cause |
|-----------|-------------|
| `FileNotFoundError` | Opening a file that does not exist |
| `FileExistsError` | Creating a file or directory that already exists |
| `PermissionError` | Accessing a file without sufficient permissions |
| `IsADirectoryError` | Performing a file operation on a directory |
| `NotADirectoryError` | Performing a directory operation on a file |
| `TimeoutError` | An operation exceeded the allowed time |
| `ConnectionError` | A network connection failed |
| `ConnectionRefusedError` | A connection attempt was refused |
| `ConnectionResetError` | A connection was reset by the remote host |

## Where custom exceptions fit

Custom exceptions should inherit from `Exception` or one of its subclasses. The most common patterns are as follows:

```
Exception
├── YourProjectError              # Base for all project exceptions
│   ├── YourSpecificError         # Specific failure mode
│   └── YourOtherError            # Another failure mode
├── ValueError                    # Inherit from ValueError if appropriate
│   └── YourCustomValueError
└── TypeError                     # Inherit from TypeError if appropriate
    └── YourCustomTypeError
```

### Guidelines for placing custom exceptions

| Inherit from | When |
|--------------|------|
| `Exception` | Most custom exceptions (the default choice) |
| `ValueError` | Your exception represents an invalid value |
| `TypeError` | Your exception represents a type mismatch |
| `RuntimeError` | Your exception represents a runtime condition |
| `OSError` | Your exception relates to operating system operations |

!!! warning
    Never inherit directly from `BaseException` unless you are creating an exception that should not be caught by `except Exception`. This is extremely rare in application code.

## Verifying the hierarchy

You can use `issubclass()` and `__mro__` to inspect the exception hierarchy at runtime.

```python
# Check if one exception is a subclass of another
print(issubclass(FileNotFoundError, OSError))       # True
print(issubclass(ZeroDivisionError, ArithmeticError))  # True
print(issubclass(KeyError, LookupError))            # True

# View the full method resolution order
print(FileNotFoundError.__mro__)
# (<class 'FileNotFoundError'>, <class 'OSError'>, <class 'Exception'>,
#  <class 'BaseException'>, <class 'object'>)
```

## Further reading

- [Built-in exceptions reference](built-in-exceptions-reference.md) for detailed descriptions of each exception type
- [Try/except syntax reference](try-except-syntax-reference.md) for handling syntax
- [Python Built-in Exceptions documentation](https://docs.python.org/3/library/exceptions.html) for the official reference
