# First-class functions in Python

When people say that functions in Python are "first-class", they mean that functions are treated the same as any other object. You can assign them to variables, pass them as arguments, return them from other functions, and store them in data structures. This is not a minor technicality. It is one of the features that makes Python expressive and flexible.

## What "first-class" means

In programming language theory, a value is first-class if it can be:

- Assigned to a variable.
- Passed as an argument to a function.
- Returned as a value from a function.
- Stored in a data structure.

In Python, functions meet all four criteria. A function created with `def` or `lambda` is an object of type `function`, and you can do anything with it that you can do with an integer, a string, or a list.

## Assigning functions to variables

When you define a function, the name you give it is simply a variable that refers to a function object. You can assign that same object to another name:

```python
def shout(text):
    return text.upper()

yell = shout
print(yell("hello"))  # HELLO
```

The name `yell` now refers to the same function object as `shout`. There is nothing special happening here. Python is just assigning one object to another name, exactly as it would with `x = 42`.

This also means you can delete the original name without affecting the other:

```python
del shout
print(yell("hello"))  # Still works: HELLO
```

## Passing functions as arguments

Because functions are objects, you can pass them as arguments to other functions. A function that takes another function as a parameter is called a **higher-order function**.

```python
def apply(func, value):
    return func(value)

def double(n):
    return n * 2

result = apply(double, 5)  # 10
```

This pattern is everywhere in Python. The built-in `sorted()`, `map()`, `filter()`, and `max()` functions all accept functions as arguments. When you write `sorted(names, key=str.lower)`, you are passing the `str.lower` function as an argument.

## Returning functions from functions

Functions can create and return other functions. This is the foundation of factory functions and decorators.

```python
def make_multiplier(factor):
    def multiplier(n):
        return n * factor
    return multiplier

triple = make_multiplier(3)
print(triple(10))  # 30
```

Here, `make_multiplier` returns a new function each time it is called. The returned function remembers the value of `factor` from the enclosing scope. This is a **closure**, and it is one of the most powerful consequences of first-class functions.

## Storing functions in data structures

You can put functions in lists, dictionaries, sets, and any other container.

```python
operations = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
}

result = operations["multiply"](4, 5)  # 20
```

This pattern is useful for dispatch tables, plugin systems, and command processors. Instead of writing a long chain of `if`/`elif` statements, you can look up the right function in a dictionary and call it.

## How this enables powerful patterns

First-class functions are the foundation for several important programming patterns in Python.

**Callbacks** are functions passed as arguments to be called later, commonly used in event-driven programming and asynchronous code.

**Decorators** are functions that take a function and return a modified version of it. The `@decorator` syntax is merely convenient shorthand for passing a function to another function and reassigning the result.

**Higher-order functions** like `map()`, `filter()`, and `sorted()` rely entirely on the ability to pass functions as arguments. Without first-class functions, these patterns would not exist in their current form.

## Comparison with other languages

Not all languages treat functions as first-class objects. In older versions of Java (before Java 8), for example, you could not pass a function directly as an argument. Instead, you had to wrap it in an object that implemented a specific interface. This required significantly more code for something Python handles naturally.

Languages like C allow function pointers, which provide some of the same capabilities, but with a more cumbersome syntax and without the flexibility of closures.

Python, along with languages like JavaScript, Ruby, and Haskell, treats functions as fully first-class. This makes certain patterns natural and concise.

## The `callable()` built-in and the `__call__` method

Python provides the `callable()` built-in to check whether an object can be called like a function:

```python
callable(print)       # True
callable(42)          # False
callable(lambda: 0)   # True
```

Any object that defines a `__call__` method is callable. This means you can make your own objects behave like functions:

```python
class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting

    def __call__(self, name):
        return f"{self.greeting}, {name}!"

hello = Greeter("Hello")
print(hello("Alice"))  # Hello, Alice!
print(callable(hello)) # True
```

This blurs the line between functions and objects, and it is by design. In Python, the distinction is less important than the interface: if something is callable, you can call it.

## Practical implications

Understanding first-class functions changes how you write Python. You start seeing opportunities to pass behaviour as data, to build flexible APIs that accept functions as parameters, and to write less code by composing small functions instead of writing large, monolithic ones.

When you write a function that takes a `key` parameter, or a `callback` parameter, or a `validator` parameter, you are designing for first-class functions. You are saying to the caller: "You decide the behaviour. Just give me a function."

This is a powerful way to write flexible, reusable code. It moves decisions to the caller, keeps your functions general, and makes your programmes easier to adapt as requirements change.
