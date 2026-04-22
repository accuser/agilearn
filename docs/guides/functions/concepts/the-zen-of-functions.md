# The Zen of functions

The Zen of Python (`import this`) offers a set of guiding principles for writing good Python code. Many of these principles apply directly to the art of writing functions. This page explores what it means to write functions that are clear, focused, and well-designed.

## Do one thing well

The single responsibility principle, borrowed from software engineering, states that a function should have one reason to exist and one reason to change. A function called `calculate_tax` should calculate tax. It should not also format the result, log it to a file, and send an email notification.

When a function tries to do too much, it becomes harder to name, harder to test, and harder to reuse. If you struggle to describe what a function does without using the word "and", that is a sign it should be two functions.

```python
# Too many responsibilities
def process_order(order):
    total = sum(item.price for item in order.items)
    tax = total * 0.20
    send_email(order.customer, total + tax)
    log_to_database(order, total, tax)
    return total + tax

# Better: each function does one thing
def calculate_total(items):
    return sum(item.price for item in items)

def calculate_tax(amount, rate=0.20):
    return amount * rate
```

Small, focused functions are easier to understand individually and more flexible when composed together.

## Explicit is better than implicit

A function should be honest about what it needs and what it provides. Its parameters should clearly state what inputs it requires, and its return value should clearly communicate what it produces.

Hidden dependencies &ndash; like reading from global variables, relying on external state, or producing side effects that the caller does not expect &ndash; make functions unpredictable. A function that quietly depends on a global configuration variable is harder to test and harder to reason about than one that accepts the configuration as a parameter.

```python
# Implicit: depends on global state
tax_rate = 0.20

def calculate_tax(amount):
    return amount * tax_rate

# Explicit: everything is in the signature
def calculate_tax(amount, rate=0.20):
    return amount * rate
```

The explicit version is self-contained. You can read the function in isolation and understand exactly what it does.

## Readability counts

The name of a function is arguably its most important feature. A well-chosen name eliminates the need to read the function body to understand what it does. Aim for names that describe the function's purpose, not its implementation.

Some guidelines for naming functions:

- Use verbs for functions that perform actions: `calculate_total`, `send_message`, `validate_email`.
- Use `is_` or `has_` prefixes for functions that return booleans: `is_valid`, `has_permission`.
- Avoid vague names like `process`, `handle`, `do_stuff`, or `run`. These tell the reader nothing about what the function actually does.
- Be specific. `get_user_by_email` is more helpful than `get_user`, which is more helpful than `get`.

PEP 8 specifies that function names should use `lowercase_with_underscores`. This convention is universal in Python and breaking it will confuse other programmers.

## Simple is better than complex

There is a strong correlation between function length and function quality. Short functions tend to be easier to understand, easier to test, and less likely to contain bugs. This is not a rule about counting lines, but a principle: if a function is long, it is probably doing too much.

A good guideline is that a function should fit on a single screen. If you have to scroll to read it, consider whether it can be broken into smaller pieces.

That said, simplicity is not about making everything as short as possible. A function that is too cleverly compressed can be harder to read than a slightly longer, more straightforward version. The goal is clarity, not brevity.

## Errors should never pass silently

A function should fail loudly and clearly when something goes wrong. Returning `None` to signal an error, or silently ignoring invalid inputs, leads to bugs that are difficult to track down.

```python
# Silent failure: the caller might not notice the None
def divide(a, b):
    if b == 0:
        return None
    return a / b

# Explicit failure: the problem is immediately visible
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Exceptions are Python's way of communicating errors. Use them. Document the exceptions your function may raise so that callers know what to expect.

## There should be one obvious way to do it

When designing a function's interface, aim for one clear way to use it. If a function accepts arguments in three different formats, or if there are multiple ways to achieve the same result, the interface is probably too flexible.

Default arguments and keyword-only arguments help you create interfaces that guide the caller towards correct usage:

```python
def connect(host: str, port: int, *, timeout: int = 30) -> None:
    """Connect to a server."""
    pass
```

The `*` forces `timeout` to be passed as a keyword argument, making calls self-documenting:

```python
connect("localhost", 8080, timeout=60)
```

## If the implementation is hard to explain, it is a bad idea

This principle is a useful test for function design. If you cannot explain what a function does in a sentence or two, it is probably too complex. If the docstring is longer than the function body, something might be wrong.

When a function becomes hard to explain, the right response is usually to refactor. Break it into smaller functions, each of which is easy to explain on its own. Then compose them.

## The art of good function signatures

A function signature is the first thing a reader sees. A well-designed signature communicates intent clearly.

**Parameter order matters.** Put the most important parameters first. Required parameters come before optional ones. The data being operated on typically comes before configuration options.

**Use defaults wisely.** Default arguments should represent the most common case. A function with good defaults can often be called with minimal arguments while still supporting advanced use cases.

**Use keyword-only arguments for clarity.** When a function has boolean flags or configuration options, making them keyword-only prevents ambiguous positional calls:

```python
# Unclear at the call site
process_data(data, True, False, 10)

# Clear at the call site
process_data(data, normalise=True, verbose=False, max_retries=10)
```

**Limit the number of parameters.** A function with more than five or six parameters is often a sign that it is doing too much, or that some of the parameters should be grouped into a data structure.

## When to break the rules

All of these principles are guidelines, not laws. There are times when a function genuinely needs to do two things, or when a global variable is the simplest solution, or when a longer function is clearer than several shorter ones.

The mark of an experienced programmer is not rigid adherence to rules but the judgement to know when an exception is justified. The Zen of Python itself acknowledges this: "Special cases are not special enough to break the rules. Although practicality beats purity."

Write functions that are easy to read, easy to test, and easy to change. When the principles help you do that, follow them. When they do not, use your judgement.
