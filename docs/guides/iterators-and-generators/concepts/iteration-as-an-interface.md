---
title: Iteration as an interface
---

# Iteration as an interface

The iterator protocol is two methods: `__iter__` and `__next__`. That's it. No length, no random access, no rewind, no inspection. It's one of the smallest interfaces in the language — and yet it's the basis on which `for` loops, comprehensions, unpacking, `sum`, `max`, `in`, every standard-library combinator, and every well-behaved third-party library cooperate.

This essay is about why a deliberately small interface is so powerful, and what that pattern teaches us about API design more broadly.

## The contract

The protocol asks an object to commit to two things: "give me a way to start producing values" (`__iter__`) and "give me the next one, or tell me there are no more" (`__next__`). Anything you can describe sequentially fits — a list, a file handle, a database cursor, an HTTP response stream, a generator, a tree traversal, an infinite mathematical sequence, the network packets arriving on a socket. If you can describe it as "values, one after another, until done", you can wear the iterator hat.

The contract is *all* the protocol asks. Iterators don't have to support being read twice. They don't have to know how many values they'll produce. They don't have to be indexable. They don't have to support backtracking. They don't even have to be backed by data — they can compute values on the fly.

This is a feature, not a limitation. Every requirement you put in an interface is a requirement that excludes implementations. By keeping the protocol small, Python lets a huge variety of *kinds of thing* satisfy it.

## What you get for implementing it

Implement `__iter__` once and your type plugs into:

- `for x in obj`
- `list(obj)`, `tuple(obj)`, `set(obj)`, `dict(obj)` (when the values are key/value pairs)
- `sum(obj)`, `max(obj)`, `min(obj)`, `any(obj)`, `all(obj)`
- comprehensions: `[f(x) for x in obj]`, `{x for x in obj}`, etc
- unpacking: `a, b, c = obj`
- membership tests: `x in obj`
- the entire `itertools` module: `chain`, `groupby`, `zip`, `tee`, `accumulate`, …
- third-party libraries that follow the protocol: pandas constructors, NumPy `fromiter`, every "iterable" parameter in every library you'll ever use.

You did one small thing; you got everything that thing makes possible. This is the payoff of programming to interfaces. The work of integrating with the ecosystem is done once, by the ecosystem, against a single contract.

## The flip side — what you don't get

A consequence of the small interface: you also don't *get* anything you didn't write. An iterator doesn't know its length. It doesn't support indexing. It doesn't rewind. If you want any of those things, you implement them — but they're not part of being iterable.

This is sometimes annoying:

```python
g = (x * x for x in range(10))
len(g)       # TypeError: object of type 'generator' has no len()
g[3]         # TypeError: 'generator' object is not subscriptable
```

But it's the same thing as before, viewed from the other side. The contract doesn't require length, so a generator doesn't have to know its length, so an infinite generator can exist, so you can write `count(0)` and iterate it as long as you want. If `len(...)` were part of the protocol, infinite generators couldn't exist. Every restriction on the producer is a flexibility on the consumer.

## Duck typing and structural fit

Python doesn't ask you to *declare* that you implement the iterator protocol. There is no `IIterable` interface to inherit from (well, there's `collections.abc.Iterable`, but it's optional and mostly used for `isinstance` checks). You just define the methods, and any code that calls `iter(...)` and `next(...)` works.

This is duck typing — "if it walks like a duck and quacks like a duck, it's a duck". For iteration the duck-test is unusually clear because the protocol is unusually small. There are exactly two methods to implement; nothing is hidden in default behaviour.

The result: you can take a *third-party* library's class and make it iterable from outside. Subclass it, add `__iter__`, monkey-patch it, wrap it. The library doesn't have to know. It doesn't have to coordinate. It doesn't have to bless your wrapper. The protocol is structural — anything that fits the shape participates.

## Composability

Because every iteration-aware tool speaks the same protocol, they all combine without translation:

```python
result = sum(
    x * x
    for x in itertools.takewhile(lambda v: v < 100, generate_primes())
    if x % 4 == 1
)
```

Five layers — a custom generator, an `itertools` filter, a generator expression, another filter, a final reduction — and there is no interface impedance anywhere in the chain. Each stage produces an iterator; the next stage consumes one. They don't have to know about each other or coordinate. You can pull any stage out, put a different one in, debug by inserting a `print`, and the surrounding code doesn't notice.

Compare this with APIs where each layer has its own type — pandas `DataFrame`, NumPy `array`, Python `list`, custom `Result` objects — and the seams between them require explicit conversion. Each conversion is a place where the abstraction can leak. The iterator protocol has no such seams. The interface is so thin that there's nothing to translate.

## The lesson for API design

The iterator protocol is a textbook example of *defining the smallest interface that does the job*. There's a generation of programmers who learnt OO from books that taught the opposite — define a rich base class, expose lots of methods, hide the implementation behind a thick interface. The Python design choice shows what you give up by doing that: every method you put in the interface is a method every implementation has to honour. A rich interface excludes simple implementations; a thin interface admits them.

If you're designing an interface in your own code — whether that's an abstract base class, a protocol, a callback signature, or just an informal contract about what shape of object a function takes — the iterator protocol is the model. Ask: what is the *minimum* an implementation has to provide to be useful? Anything beyond that is something you're choosing to require, and you should have a reason. The rest can be added externally by composition: helpers like `enumerate`, `zip`, `tee` that take iterators and produce more iterators. The interface stays small; the *vocabulary* built on top of it grows without limit.

## A small protocol, a large ecosystem

Most of the standard library — and most of the third-party Python ecosystem — speaks the iterator protocol. It is the medium through which data flows between Python's parts. When you make a class iterable, you aren't adding a feature; you're connecting your code to a network of cooperating tools that has been growing since the language's earliest days.

That network exists because the protocol is small enough that every implementer can support it cheaply, and every consumer can rely on it absolutely. The smallness is the design.
