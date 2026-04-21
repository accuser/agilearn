---
title: Gradual typing
---

# Gradual typing

Python's type system is *gradual*: you don't have to annotate everything. You can annotate some things and leave others alone, and the checker treats the unannotated parts as `Any` (don't check, don't narrow, trust the caller). This is a deliberate design choice, and understanding it explains a lot about how typing works in practice.

## What "gradual" actually means

In a fully statically typed language like Rust or Haskell, every value has a known type at compile time. The compiler refuses to compile code that doesn't type-check.

Python's type system is different. It's optional — you opt into checking by adding annotations, one function at a time. Unannotated code isn't "wrong" or "untyped", it's `Any` — the universal type that's compatible with everything. A type-checker looks at annotated code carefully and shrugs at unannotated code.

The practical consequence: you can add type hints to an existing codebase incrementally. Start with the most important module, annotate its public functions, run mypy on just that module, fix the errors. Then move to the next module. Your code continues to run the whole time — Python itself doesn't enforce anything.

## Why gradual works

A few reasons gradual typing matters for Python specifically:

**Legacy code.** Python had 20+ years of dynamically-typed code before PEP 484 introduced type hints in 2014. Demanding \"annotate or don't use\" would have excluded enormous amounts of useful code. Gradual typing meant the transition could happen one module at a time, without a flag day.

**Third-party libraries.** Not every package has type stubs. If Python demanded full annotations, you couldn't use an unannotated library without also annotating it (or waiting for someone else to). Gradual typing lets you use untyped libraries — they're just `Any` at the boundary.

**Exploratory code.** Scripts, notebooks, and early prototypes benefit from dynamic typing — you're iterating on the code shape. Annotations would be premature. Gradual typing lets you write loose code early and tighten later.

**Dynamic patterns.** Some Python idioms (metaclasses, heavy `__getattr__` use, plugin loaders) are genuinely hard to type well. Rather than excluding them, gradual typing lets you type the surrounding code and use `Any` at the dynamic bits.

## The gradient

Projects occupy a spectrum:

- **Fully untyped.** Zero annotations. mypy reports nothing.
- **Partially typed.** Some functions annotated, others not. mypy checks what's annotated, treats the rest as `Any`.
- **Mostly typed, loose.** Most functions annotated, but with `Any` used liberally. mypy catches some things, lets a lot through.
- **Mostly typed, strict.** Most functions annotated, `--strict` enforced, `Any` used sparingly. Most bugs caught.
- **Fully strict.** Every function annotated, `--strict` + `--disallow-any-explicit`, no `Any` without justification. Maximum safety.

The choice isn't binary. You can sit anywhere on the gradient and it's legitimate. Different projects land in different places, and the same project can move as priorities change.

## `Any` as the escape hatch

`Any` is what makes all of this work. It's a type that's compatible with every type in both directions — you can assign anything *to* an `Any`-typed variable, and you can assign an `Any`-typed variable to anything. No type errors propagate through an `Any`.

This is the leak in the system and it's deliberate. Without `Any`, you couldn't have gradual typing — every untyped call would be a type error. With it, untyped code is silently tolerated.

The cost: every `Any` is a place where the type-checker can't help you. Bugs slip through. The gradual-typing trade-off is "catch some bugs now, in exchange for not being able to use dynamically-typed libraries". For most teams, the trade is worth making.

**`object` is the safer alternative** for "I really don't know what type this is". Operations on `object` are type-checked — you can only call methods that every Python object has (`str()`, `repr()`, `hash()` if the concrete type is hashable, etc.) — and narrowing via `isinstance` works. `Any` says "trust the caller"; `object` says "I don't know, so nothing is safe until I narrow".

## Strategies for annotating a legacy codebase

If you're retrofitting types onto existing code:

**Start at the boundaries.** Annotate the public API — module entry points, the handful of functions that other modules call. The benefit per line of annotation is highest here.

**Work on one module at a time.** mypy errors across a whole codebase are demoralising. Pick a module, annotate it, enable strict checking for just that module in `pyproject.toml`, fix the errors. Expand outward.

**Prioritise data structures.** A `TypedDict` or dataclass for your main domain object pays off immediately — every function that takes or returns it gets typed for free.

**Accept `Any` liberally at first.** You can always tighten later. A function annotated `def f(x: Any) -> Any` is more useful than an unannotated function because future you can at least see that mypy looked at it once.

**Use `reveal_type`** to learn what mypy inferred. Often mypy figured out the shape better than you did.

## When to be strict

`--strict` turns on "annotate everything, disallow Any where possible, warn about unused ignores". It's a great default for:

- New projects (you have no legacy code to fight).
- Libraries you're publishing (your users benefit from the type safety).
- Critical code paths (financial, medical, security).

It's probably *not* the right setting for:

- Research code, notebooks, quick scripts.
- Early prototypes where the shape is in flux.
- Codebases with a huge pile of untyped legacy you can't annotate yet.

## Gradual typing isn't static typing with more steps

A subtle but important point: gradual typing and static typing are different disciplines.

A statically typed language makes types a structural part of the language — the compiler can assume types are correct and use them for optimisation. Missing types are errors.

Gradual typing, including Python's, is a layer *on top* of a dynamically-typed language. The runtime still doesn't check anything. Types are a human-and-tool aid, not a compiler optimisation. `Any` isn't "a type we haven't named yet", it's "no information, please don't check".

This is why Python type hints don't speed up your code (the runtime ignores them) and why the checker is sometimes conservative in ways a static language wouldn't be. Accepting this framing — "types are for humans and tools, not for the interpreter" — makes the behaviour of mypy and friends make sense.

## The summary

Gradual typing is what makes Python types *usable*. You can add them where they help, skip them where they don't, and the language doesn't make you choose all-or-nothing. `Any` is the mechanism that enables this. Use it deliberately, tighten when you can, and treat types as a tool rather than a religion.
