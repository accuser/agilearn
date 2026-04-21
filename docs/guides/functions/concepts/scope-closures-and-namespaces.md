# Scope, closures, and namespaces

Every time you use a variable name in Python, the interpreter has to figure out what that name refers to. This process is governed by rules about scope, namespaces, and name resolution. Understanding these rules is essential for writing correct functions, especially when functions are nested inside other functions.

## What is a namespace?

A namespace is a mapping from names to objects. You can think of it as a dictionary where the keys are variable names and the values are the objects those names refer to.

Python uses namespaces everywhere. When you write `x = 10`, you are adding (or updating) an entry in a namespace. When you write `print(x)`, Python looks up the name `x` in one or more namespaces to find the object it refers to.

## The four namespaces

Python organises names into four namespaces, each with a different lifetime and scope.

**Built-in namespace** contains names that are always available: `print`, `len`, `int`, `True`, `None`, and so on. This namespace is created when the Python interpreter starts and is never deleted.

**Global namespace** (also called module namespace) contains names defined at the top level of a module or script. Each module has its own global namespace. It is created when the module is imported or when the script starts running.

**Enclosing namespace** (also called nonlocal namespace) exists when functions are nested. It contains names from the enclosing function. There can be multiple enclosing namespaces if functions are nested several levels deep.

**Local namespace** contains names defined inside the current function. It is created when the function is called and discarded when the function returns.

## The LEGB rule

When Python encounters a name, it searches for it in a specific order, commonly known as the **LEGB rule**:

1. **Local** -- Names defined in the current function.
2. **Enclosing** -- Names in enclosing functions, from inner to outer.
3. **Global** -- Names at the module level.
4. **Built-in** -- Names in the built-in namespace.

Python checks each scope in order and uses the first match it finds. If the name is not found in any scope, Python raises a `NameError`.

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # "local" -- found in Local scope

    inner()

outer()
```

If you remove the assignment in `inner`, Python moves to the next scope:

```python
def outer():
    x = "enclosing"

    def inner():
        print(x)  # "enclosing" -- found in Enclosing scope

    inner()
```

## Variable shadowing

When a name in an inner scope has the same name as one in an outer scope, the inner name **shadows** the outer one. The outer name still exists, but it is hidden within the inner scope.

```python
value = 100

def example():
    value = 42  # Shadows the global "value"
    print(value)  # 42

example()
print(value)  # 100 -- the global is unchanged
```

Shadowing is not an error, but it can be confusing. If a reader expects `value` inside the function to refer to the global, they will be surprised. Be deliberate about choosing names, and avoid shadowing unless you have a clear reason.

## Why `global` exists (and why to avoid it)

The `global` statement tells Python that a name inside a function refers to the global namespace, allowing you to read and modify global variables.

```python
counter = 0

def increment():
    global counter
    counter += 1
```

While this works, experienced Python programmers use `global` sparingly. Functions that modify global state are harder to reason about, harder to test, and more likely to cause bugs. A function that takes inputs as parameters and communicates results through return values is much easier to understand and reuse.

If you find yourself reaching for `global`, consider whether the function should accept the value as a parameter and return the modified result instead:

```python
def increment(counter):
    return counter + 1

counter = 0
counter = increment(counter)
```

This version is explicit about its inputs and outputs, making it easier to test and less likely to introduce subtle bugs.

## Closures

A closure is a function that remembers the values from its enclosing scope, even after that scope has finished executing. Closures arise naturally when an inner function references a variable from an outer function.

```python
def make_counter(start=0):
    count = start

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

my_counter = make_counter()
print(my_counter())  # 1
print(my_counter())  # 2
print(my_counter())  # 3
```

When `make_counter()` returns, its local variable `count` would normally be discarded. But because `counter()` still references it, Python keeps the variable alive in a closure. The returned function carries its enclosing environment with it.

## Late binding: the common gotcha

Closures capture variables by reference, not by value. This leads to a well-known surprise when creating closures inside loops:

```python
functions = []
for i in range(3):
    functions.append(lambda: i)

print(functions[0]())  # 2 (not 0!)
print(functions[1]())  # 2 (not 1!)
print(functions[2]())  # 2
```

All three functions share the same reference to `i`, and by the time they are called, `i` has its final value of `2`. This is called **late binding**.

The standard workaround is to capture the current value using a default argument:

```python
functions = []
for i in range(3):
    functions.append(lambda i=i: i)

print(functions[0]())  # 0
print(functions[1]())  # 1
print(functions[2]())  # 2
```

The default argument `i=i` evaluates at definition time, capturing the current value.

## Practical uses of closures

### Factory functions

Closures are perfect for creating families of related functions:

```python
def make_formatter(prefix, suffix):
    def formatter(text):
        return f"{prefix}{text}{suffix}"
    return formatter

bold = make_formatter("<b>", "</b>")
italic = make_formatter("<i>", "</i>")

print(bold("hello"))    # <b>hello</b>
print(italic("hello"))  # <i>hello</i>
```

### Maintaining state

Closures can hold private state without the overhead of defining a class:

```python
def make_accumulator():
    total = 0
    def add(value):
        nonlocal total
        total += value
        return total
    return add

acc = make_accumulator()
print(acc(10))  # 10
print(acc(20))  # 30
print(acc(5))   # 35
```

### Data hiding

Because the enclosed variables are not accessible from outside, closures provide a form of data hiding. There is no way to access `total` directly in the example above; you can only interact with it through the `add` function.

## Closures and objects

There is a well-known saying: "Objects are poor man's closures. Closures are poor man's objects." The two are, in many ways, equivalent. A closure is a function bundled with some state. An object is state bundled with some functions. You can often choose either approach.

For simple cases with one or two pieces of state and one function, a closure is usually cleaner. For more complex situations with multiple pieces of state and several related functions, a class is usually a better choice.

The important thing is to recognise that closures and objects solve similar problems. Understanding both gives you more tools to choose from and helps you pick the right approach for each situation.
