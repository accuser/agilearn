# Understanding the exception model

When Python encounters an error, it does not simply stop. It initiates a structured process: creating an exception object, searching for a matching handler, and unwinding the call stack if necessary. Understanding this process helps you write better exception handling code and debug problems more effectively.

This article explains how the exception propagation model in Python works, including the call stack, tracebacks, exception chaining, and how the interpreter finds matching handlers.

## The call stack

To understand exception propagation, you first need to understand the **call stack**. Every time a function is called, Python adds a new **frame** to the call stack. Each frame records the function being executed, its local variables, and where to return when the function finishes.

Consider this sequence of calls:

```python
def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def process_data(filepath: str) -> list[int]:
    content = read_file(filepath)
    return [int(line) for line in content.splitlines()]

def main() -> None:
    result = process_data("data.txt")
    print(result)
```

When `main()` calls `process_data()`, which calls `read_file()`, the call stack looks like this:

```
[Top of stack]
  read_file()       <- currently executing
  process_data()    <- waiting for read_file to return
  main()            <- waiting for process_data to return
[Bottom of stack]
```

Each function is "stacked" on top of the one that called it. When `read_file()` finishes, its frame is removed, and execution resumes in `process_data()`.

## What happens when an exception is raised

When an exception occurs -- whether raised explicitly with `raise` or triggered automatically by Python -- the following sequence unfolds:

### Step 1: The exception object is created

Python creates an exception object of the appropriate type, with the relevant message and context.

```python
# Python creates a FileNotFoundError object internally:
# FileNotFoundError("[Errno 2] No such file or directory: 'data.txt'")
```

### Step 2: The interpreter searches for a handler

Python looks for an `except` clause that matches the exception type. It starts in the current function and works its way down the call stack.

The matching rules are straightforward:

- `except FileNotFoundError` matches `FileNotFoundError` and its subclasses
- `except OSError` matches `FileNotFoundError` (because `FileNotFoundError` is a subclass of `OSError`)
- `except Exception` matches almost all exceptions (but not `KeyboardInterrupt` or `SystemExit`)

### Step 3: If a handler is found, it runs

If Python finds a matching `except` clause, it runs that handler. After the handler completes, execution continues with the code following the `try`/`except` block.

```python
def process_data(filepath: str) -> list[int]:
    try:
        content = read_file(filepath)
    except FileNotFoundError:
        # Handler found! Execution continues here.
        print(f"File not found: {filepath}")
        return []
    return [int(line) for line in content.splitlines()]
```

### Step 4: If no handler is found, the exception propagates

If the current function has no matching handler, Python **unwinds** the call stack: it removes the current frame and checks the calling function for a handler. This continues until either a handler is found or the stack is exhausted.

```
Exception raised in read_file()
  -> No handler in read_file()        -> unwind
  -> No handler in process_data()     -> unwind
  -> No handler in main()             -> unwind
  -> No handler at the top level      -> program terminates with traceback
```

This process is called **exception propagation**. The exception "propagates" up the call stack until it is handled or reaches the top level.

## Tracebacks: reading the story of an exception

When an exception is not handled, Python prints a **traceback**. The traceback tells the complete story of where the exception originated and how it propagated.

```
Traceback (most recent call last):
  File "main.py", line 10, in main
    result = process_data("data.txt")
  File "main.py", line 6, in process_data
    content = read_file(filepath)
  File "main.py", line 2, in read_file
    with open(filepath, "r", encoding="utf-8") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
```

### Reading a traceback

Tracebacks are read from **top to bottom** for the sequence of calls, and the actual error is at the **bottom**.

1. **Top**: The outermost call (`main()` on line 10)
2. **Middle**: The intermediate calls, showing how execution reached the error
3. **Bottom**: The exact line where the exception occurred, followed by the exception type and message

The phrase "most recent call last" tells you that the most recent function call is at the bottom, closest to the error.

### The traceback object

Each exception has a `__traceback__` attribute that stores the traceback as a Python object. You can inspect this programmatically, although this is more commonly used in logging frameworks than in application code.

```python
import traceback

try:
    int("hello")
except ValueError as e:
    # Format the traceback as a string
    tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
    print("".join(tb_lines))
```

## Exception chaining

Sometimes, one exception leads to another. For example, you might handle a `FileNotFoundError` and decide to raise a different exception with more context. Python supports this through **exception chaining**.

### Explicit chaining with `from`

When you use `raise ... from ...`, you explicitly state that one exception caused another.

```python
class ConfigurationError(Exception):
    """Raised when configuration cannot be loaded."""
    pass

try:
    with open("config.conf", "r") as f:
        config = f.read()
except FileNotFoundError as e:
    raise ConfigurationError("Could not load configuration") from e
```

The resulting traceback shows both exceptions:

```
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    with open("config.conf", "r") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'config.conf'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "example.py", line 8, in <module>
    raise ConfigurationError("Could not load configuration") from e
ConfigurationError: Could not load configuration
```

The `from e` clause sets the `__cause__` attribute on the new exception, preserving the full error chain.

### Implicit chaining

If you raise a new exception inside an `except` block without using `from`, Python automatically sets the `__context__` attribute to record the original exception.

```python
try:
    value = int("hello")
except ValueError:
    # This implicitly chains the ValueError
    raise RuntimeError("Processing failed")
```

The traceback displays this as:

```
During handling of the above exception, another exception occurred:
```

### Suppressing the chain with `from None`

Sometimes the original exception is not relevant to the caller. You can suppress the chain using `from None`.

```python
try:
    value = int(user_input)
except ValueError:
    raise ValueError("Please enter a valid number") from None
```

This produces a clean traceback without the original exception context.

## How handler matching works

When Python searches for a matching `except` clause, it uses `isinstance()` to check whether the exception matches the specified type. This is why handling a parent exception also handles all its children.

### The matching algorithm

Given a `try` block with multiple `except` clauses:

```python
try:
    operation()
except FileNotFoundError:
    handle_not_found()
except OSError:
    handle_os_error()
except Exception:
    handle_other()
```

Python checks each clause in order:

1. Is the exception an instance of `FileNotFoundError`? If yes, run that handler.
2. Is the exception an instance of `OSError`? If yes, run that handler.
3. Is the exception an instance of `Exception`? If yes, run that handler.

Only the **first matching handler** runs. This is why you should place more specific exceptions before more general ones. If `except OSError` appeared before `except FileNotFoundError`, the `FileNotFoundError` handler would never execute, because `FileNotFoundError` is a subclass of `OSError`.

### Handling multiple types in one clause

When you list multiple exception types in a tuple, Python checks each type:

```python
except (ValueError, TypeError) as e:
    # Runs if the exception is an instance of ValueError OR TypeError
    handle_error(e)
```

## The `finally` guarantee

The `finally` clause has a special position in the exception model. It runs in all of the following situations:

- The `try` block completes normally
- An exception is raised and handled by an `except` clause
- An exception is raised and **not** handled (it will still propagate after `finally` runs)
- A `return`, `break`, or `continue` statement exits the `try` or `except` block

This guarantee makes `finally` the right place for cleanup code that must execute regardless of what happens.

The context manager protocol (`with` statement) is built on this same guarantee, providing a cleaner syntax for the common pattern of setup and cleanup.

## Exception groups (Python 3.11 and later)

Python 3.11 introduced **exception groups** to handle situations where multiple exceptions occur concurrently, such as in asynchronous code.

An `ExceptionGroup` bundles multiple exceptions together:

```python
eg = ExceptionGroup("multiple errors", [
    ValueError("bad value"),
    TypeError("wrong type"),
])
```

Exception groups are handled with the `except*` syntax:

```python
try:
    raise ExceptionGroup("errors", [
        ValueError("bad value"),
        TypeError("wrong type"),
    ])
except* ValueError as eg:
    print(f"Value errors: {eg.exceptions}")
except* TypeError as eg:
    print(f"Type errors: {eg.exceptions}")
```

This is an advanced feature that is primarily relevant for concurrent programming frameworks.

## Key takeaways

Understanding the exception model helps you write better code in several ways:

- **Exception propagation** means you do not need to handle every exception locally. Exceptions naturally flow up the call stack to the most appropriate handler.

- **Tracebacks** are your primary debugging tool. Read them from bottom to top to find the actual error, and from top to bottom to understand the call sequence.

- **Exception chaining** preserves the full story of an error. Use `from` to link related exceptions, and `from None` to suppress irrelevant context.

- **Handler matching** uses `isinstance()`, so handling a parent class handles all its children. Place specific handlers before general ones.

- **The `finally` guarantee** ensures cleanup code runs in all circumstances, which is why context managers are so reliable.

With this understanding, you can make informed decisions about where to handle exceptions, how much context to preserve, and how to structure your error handling for maximum clarity and reliability.
