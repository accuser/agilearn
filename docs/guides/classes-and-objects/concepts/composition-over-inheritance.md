---
title: Composition over inheritance
---

# Composition over inheritance

"Prefer composition over inheritance" is one of those design slogans that gets quoted constantly without much engagement. Like most slogans it compresses a real lesson into something easy to repeat and harder to actually follow. This essay unpacks what it means, why inheritance looks tempting when it shouldn't, and the specific failure modes composition avoids.

## The two ways to reuse code

You have a `Logger` class. You need a version that adds timestamps to every message. Two options:

**Inheritance.** `TimestampedLogger` subclasses `Logger` and overrides `log`:

```python
class TimestampedLogger(Logger):
    def log(self, level, message):
        ts = datetime.now().isoformat()
        super().log(level, f"[{ts}] {message}")
```

**Composition.** `TimestampedLogger` holds a `Logger` as a field and delegates:

```python
class TimestampedLogger:
    def __init__(self, name):
        self._logger = Logger(name)

    def log(self, level, message):
        ts = datetime.now().isoformat()
        self._logger.log(level, f"[{ts}] {message}")
```

In this example inheritance wins on ergonomics — you write a handful of lines and get the rest of `Logger`'s interface for free. In larger systems, it loses, and the reason is worth understanding.

## What inheritance actually gives you

Inheriting from `Parent` says three things at once:

1. The child **is a kind of** the parent. Anywhere the parent is expected, the child works.
2. The child gets **every method** the parent has.
3. The child is **coupled** to the parent's implementation. If the parent changes how it does something, the child comes along for the ride — sometimes helpfully, sometimes not.

All three of those are often what you want. That's why inheritance isn't wrong in principle. But all three are *bundled*. You can't opt into "is a kind of" without also accepting the whole interface and the implementation coupling.

## The is-a lie

The most common inheritance mistake is "is a"-flavoured thinking taken too literally. A `Square` *is a* `Rectangle` in geometry class. A `Dog` *is a* `Mammal`. A `ResizableImage` *is an* `Image`. The inheritance hierarchy is right there in the English sentence — surely that's the signal?

It isn't. The right question is behavioural, not ontological: can a subclass be used anywhere the parent is expected *without surprising the caller*? If a function takes a `Rectangle` and sets its width to 5, passing it a `Square` breaks — either the height silently changes too (violating the Rectangle contract that width and height are independent), or the width doesn't actually change (violating the operation the caller asked for). The English sentence says "is a"; the behaviour says "isn't really".

This is Liskov substitutability, and it's the actual test for whether inheritance is appropriate. If your subclass can't stand in for its parent without callers getting a surprise, the inheritance is lying.

## Why composition keeps its shape

Composition doesn't claim "is a". It claims "has a". A `TimestampedLogger` isn't a kind of logger — it's a thing that happens to use a logger. That distinction matters in two practical ways:

**The interface is explicit.** The composed-in logger is accessed through a field, which means every use is visible in the code. If you want the wrapper to expose `log` but not `set_level`, you only expose `log`. If the `Logger` class later gains a dozen new methods, your `TimestampedLogger`'s interface doesn't silently grow.

**The coupling is lighter.** Your `TimestampedLogger` depends on the public interface of `Logger` — the methods it actually calls. With inheritance, you inherit the implementation; any field or helper method the parent uses internally becomes something you might accidentally override or rely on. Subclasses get tied to private details without anyone intending it.

## Where inheritance still wins

Composition isn't the right answer everywhere. There are a few situations where inheritance genuinely fits:

**Framework extension points.** When a library says "subclass this base class and implement these methods," the library is handing you a structured way to slot your code in. Subclassing `torch.nn.Module` or Django's `View` is the supported path; composition would be working against the library.

**Exception hierarchies.** `class ValidationError(AppError): pass`. The `is-a` relationship is genuine — a `ValidationError` can be caught by `except AppError`, which is the whole point.

**Small mixins with one job.** A `Comparable` mixin that implements `__lt__` and friends in terms of a single abstract method. A `Serialisable` mixin that adds a `to_dict` method. Used sparingly, mixins add behaviour without deep hierarchies.

**Abstract base classes declaring a contract.** Inheriting from `collections.abc.Mapping` to declare "this is a read-only mapping" and get the default implementations that follow from that declaration.

The common thread: these are cases where the subclass really does behave as a kind of the parent, and the inheritance relationship is communicating something useful rather than just sharing implementation.

## The rule that survives

"Prefer composition over inheritance" isn't really a rule about code reuse. It's a rule about what your type declarations *mean*. Inheritance says "my type can stand in for yours, carries your interface, and shares your implementation." That's a loud statement, and it should be reserved for cases where all three parts are true. When what you actually mean is "I use yours internally," composition expresses that directly, and nothing more.

In practice this is why Python code tends to have flat hierarchies — a lot of standalone classes with a `Logger` or a `Connection` as a field, rather than tall inheritance trees. It reads easily, refactors without pulling half the codebase along, and stays decoupled from the details of whatever it delegates to. That's what the slogan is actually pointing at.
