# Function syntax

This reference covers the complete syntax for defining and working with functions in Python. Each section presents the syntax form, followed by a concise example.

## The `def` statement

The `def` statement creates a named function object and binds it to a name in the current scope.

```python
def function_name(parameters):
    """Optional docstring."""
    # Function body
    return value
```

The general form, including all optional components, is as follows:

```python
@decorator
def function_name(parameters) -> return_annotation:
    """Docstring."""
    statement(s)
```

Key rules:

- The function name must be a valid Python identifier.
- The colon (`:`) after the parameter list is required.
- The function body must be indented (by convention, four spaces).
- If no `return` statement executes, the function returns `None`.

## The `lambda` expression

A `lambda` expression creates a small anonymous function. It is limited to a single expression.

```python
lambda parameters: expression
```

Examples:

```python
square = lambda x: x ** 2
add = lambda a, b: a + b
greet = lambda name="World": f"Hello, {name}!"
```

**Limitations of `lambda`:**

| Feature | `def` function | `lambda` expression |
|---------|---------------|---------------------|
| Multiple statements | Yes | No |
| Docstring | Yes | No |
| Annotations | Yes | No |
| Decorators | Yes | No (directly) |
| Name in tracebacks | Function name | `<lambda>` |

## The `return` statement

The `return` statement exits the current function and optionally sends a value back to the caller.

### Single return value

```python
def double(x):
    return x * 2
```

### Multiple return values (tuple packing)

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

q, r = divide(17, 5)  # q = 3, r = 2
```

### Bare `return`

A bare `return` with no value returns `None` and exits the function immediately.

```python
def check(value):
    if value < 0:
        return
    print(value)
```

### Implicit `None`

If the function body completes without executing a `return` statement, the function returns `None`.

```python
def greet(name):
    print(f"Hello, {name}!")

result = greet("Alice")  # Prints "Hello, Alice!" and result is None
```

## Parameter types

Python supports several parameter types, each serving a different purpose.

### Positional parameters

The most common form. Arguments are matched by position.

```python
def add(a, b):
    return a + b

add(3, 5)  # a=3, b=5
```

### Default parameters

Parameters with default values. These must follow non-default parameters.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")            # "Hello, Alice!"
greet("Alice", "Howdy")   # "Howdy, Alice!"
```

**Important:** Default values are evaluated once at function definition time, not at each call. Avoid using mutable objects as defaults.

```python
# Problematic — shared mutable default
def append_item(item, items=[]):
    items.append(item)
    return items

# Correct approach
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Keyword parameters

Any parameter can be passed by name using keyword syntax at the call site.

```python
def describe(name, age, city):
    return f"{name}, age {age}, from {city}"

describe(name="Alice", city="London", age=30)
```

### `*args` (variable positional)

Collects additional positional arguments into a tuple.

```python
def total(*args):
    return sum(args)

total(1, 2, 3, 4)  # 10
```

### `**kwargs` (variable keyword)

Collects additional keyword arguments into a dictionary.

```python
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30)
```

### Combining `*args` and `**kwargs`

```python
def flexible(required, *args, **kwargs):
    print(f"Required: {required}")
    print(f"Extra positional: {args}")
    print(f"Extra keyword: {kwargs}")

flexible("hello", 1, 2, x=10, y=20)
```

### Positional-only parameters (`/`)

Parameters before the `/` separator can only be passed by position (Python 3.8 and later).

```python
def power(base, exponent, /):
    return base ** exponent

power(2, 10)          # Valid
# power(base=2, exponent=10)  # TypeError
```

### Keyword-only parameters (`*`)

Parameters after the `*` separator (or after `*args`) must be passed by name.

```python
def connect(host, port, *, timeout=30, retries=3):
    pass

connect("localhost", 8080, timeout=60)
# connect("localhost", 8080, 60)  # TypeError
```

### Full parameter order

The complete ordering of parameter types in a function definition is as follows:

```
def f(positional_only, /, positional_or_keyword, *, keyword_only, **kwargs):
```

| Position | Parameter kind | Example |
|----------|---------------|---------|
| Before `/` | Positional-only | `def f(a, b, /)` |
| Between `/` and `*` | Positional or keyword | `def f(a, b)` |
| After `*` or `*args` | Keyword-only | `def f(*, a, b)` |
| `*args` | Variable positional | `def f(*args)` |
| `**kwargs` | Variable keyword | `def f(**kwargs)` |

## Function annotations

Annotations attach metadata to parameters and the return value. They do not enforce types at runtime.

```python
def add(a: int, b: int) -> int:
    return a + b
```

Annotations are stored in the `__annotations__` attribute:

```python
add.__annotations__
# {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

Annotations can be any valid expression:

```python
def process(data: list[int], factor: float = 1.0) -> list[float]:
    return [x * factor for x in data]
```

## The `global` and `nonlocal` statements

### `global`

Declares that a name refers to a variable in the module (global) scope.

```python
counter = 0

def increment():
    global counter
    counter += 1
```

### `nonlocal`

Declares that a name refers to a variable in the nearest enclosing scope (not global).

```python
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
    inner()
    return count  # 1
```

## Nested function definitions

Functions can be defined inside other functions. The inner function has access to the enclosing scope.

```python
def make_greeter(greeting):
    def greeter(name):
        return f"{greeting}, {name}!"
    return greeter

hello = make_greeter("Hello")
hello("Alice")  # "Hello, Alice!"
```

## Decorator syntax

A decorator is a callable that takes a function and returns a modified or replacement function. The `@` syntax applies a decorator at definition time.

### Basic decorator

```python
@decorator
def function():
    pass

# Equivalent to:
def function():
    pass
function = decorator(function)
```

### Decorator with arguments

```python
@decorator(arg1, arg2)
def function():
    pass

# Equivalent to:
def function():
    pass
function = decorator(arg1, arg2)(function)
```

### Stacking decorators

Multiple decorators are applied from bottom to top (innermost first).

```python
@decorator_a
@decorator_b
def function():
    pass

# Equivalent to:
function = decorator_a(decorator_b(function))
```

### Practical example

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b):
    return a + b
```

## Quick reference table

| Syntax | Purpose | Example |
|--------|---------|---------|
| `def name():` | Define a named function | `def greet(): ...` |
| `lambda x: x` | Create an anonymous function | `lambda x: x + 1` |
| `return value` | Return a value | `return total` |
| `return` | Return `None` and exit | `return` |
| `*args` | Variable positional parameters | `def f(*args): ...` |
| `**kwargs` | Variable keyword parameters | `def f(**kwargs): ...` |
| `/` | End positional-only parameters | `def f(a, /): ...` |
| `*` | Begin keyword-only parameters | `def f(*, a): ...` |
| `-> type` | Return annotation | `def f() -> int: ...` |
| `@decorator` | Apply a decorator | `@log_calls` |
| `global x` | Reference a global variable | `global counter` |
| `nonlocal x` | Reference an enclosing variable | `nonlocal count` |
