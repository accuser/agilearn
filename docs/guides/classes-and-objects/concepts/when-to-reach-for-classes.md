---
title: When to reach for classes
---

# When to reach for classes

Object-orientation gets taught early, often as the centrepiece of "real" programming, and the lesson comes through as: *if you've got a noun, write a class*. Python pushes back on that. A function and a dictionary are usually fine. The interesting question isn't whether to write a class — it's recognising the small set of situations where one genuinely earns its place.

## The default: a function and a dict

Here's a simple data-processing job: take a list of users, filter to the active ones, and email each one a report.

```python
def send_reports(users):
    for user in users:
        if user["active"]:
            send_email(user["email"], build_report(user))
```

`user` is a dict. `send_reports` is a function. There's no class anywhere, and there doesn't need to be. Dicts are fast, flexible, and serialise to JSON for free. Functions are testable in isolation. Reaching for `class User: ...` here would add ceremony without changing what the code does or how easy it is to read.

This is the default for a lot of Python code, and it's a sensible default. Most programs are made of functions calling other functions, occasionally passing dicts and lists between them. Classes appear only when there's a specific reason.

## Signal one: state and the operations on it want to live together

A `Counter` that holds a number and lets you increment it, reset it, and read it. A `Stack` with `push` and `pop`. A `Connection` that holds an open socket. The data and the operations are coupled — every operation either reads or modifies the state.

You *could* implement a counter as a global variable and three free functions. You *could* implement a stack as a list and four functions that take it as their first argument. But the connection between the data and the operations would be implicit. A class makes it explicit and gives the bundle a name. Anyone reading the code can see, from the class definition alone, what a Counter can do.

The test: can you describe the type as a noun whose verbs all act on its state? If yes, a class is probably the right shape.

## Signal two: invariants you want to enforce

You have a `Rectangle` with a `width` and a `height`. The invariant is that both must be positive. With a dict, that invariant lives nowhere — anyone can write `rect["width"] = -3` and you find out hours later when something downstream divides by it. With a class — particularly with `@property` setters or `__post_init__` — the invariant lives at the boundary, in the class itself. Bad values can't get in.

This is one of the strongest signals. If you find yourself writing the same defensive validation in three different places before passing a dict to three different functions, that validation belongs on a class, called once at construction time.

## Signal three: multiple values that always travel together

A coordinate is a pair: latitude and longitude. A money amount is a pair: a number and a currency. An order line is a triple: product, quantity, price. These bundles always travel together — passing latitude without longitude doesn't mean anything, and the moment you let them get separated you start writing functions that take five positional arguments and lose track of which is which.

A `@dataclass` (or `NamedTuple` for the small immutable case) gives the bundle a name. Reading the class definition tells you exactly which fields exist. Reading a function signature with one `Coord` parameter tells you more than the same function with `lat` and `lon` parameters that might or might not be in the right order.

## Signal four: polymorphism that isn't a giant `if`/`elif`

You have several kinds of thing — different shape variants, different payment methods, different export formats — and they all need to support the same operations but implement them differently. Without classes, you write a function with a giant `if shape_type == "circle": ... elif shape_type == "square": ...`. Every new shape adds another branch to that function, in some other module, far from the code that defines what a circle *is*.

Classes turn that into one method per shape, defined alongside the shape. Adding a new shape is one self-contained class, not surgical edits to a switch statement that lives elsewhere.

This isn't an argument for inheritance — see [composition over inheritance](composition-over-inheritance.md). It's an argument for the *interface* being explicit. `Protocol` (from the type hints guide) gives you the same benefit without requiring a class hierarchy.

## When *not* to reach for classes

A few patterns are class-shaped but shouldn't be:

- **Pure namespacing.** A class with nothing but `@staticmethod` is a module pretending. Use a module.
- **A bag of unrelated methods.** A `Utils` class with `format_date()`, `slugify()`, and `compress_image()` isn't an object — it's a junk drawer. Split it into a module per concern.
- **A "manager" or "service" with no state.** A `UserService` with one method that takes a user and does a thing is just a function with extra typing. Skip the class.
- **Wrapping a single value to add one method.** `class Email: def __init__(self, address): ...; def send(...): ...` for a single string usually wants to be a function. (Exceptions: validation matters at construction, the type matters for clarity at function boundaries.)

## The shortest summary

Classes are a tool for binding state to behaviour, enforcing invariants, naming bundles, and supporting polymorphism without giant conditionals. When you have one of those needs, reach for a class. When you don't, a function and a dict are almost always lighter, easier to test, and faster to change.

The Python standard library is a good reference. `pathlib.Path` is a class because filesystem paths benefit from operations that travel with the data. `os.path.join` is a function because the same job, done at a lower level, doesn't. Both work; the choice was deliberate.
