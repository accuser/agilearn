---
title: When type hints help
---

# When type hints help

Type hints aren't universally worth it. They take time to write, can clutter simple code, and sometimes the cost-benefit isn't there. This essay is about reading the situation — where annotations genuinely catch bugs and save time, where they're mostly noise, and how to decide for a given bit of code.

## Where type hints clearly help

**Long-lived codebases.** A function gets refactored. Its signature changes. Every caller that still passes the old arguments is now broken — and without type checks, you won't know until someone runs the broken path. Type hints catch this at build time, across the whole project, at once. The longer the code lives and the more people touch it, the more this pays off.

**Public APIs and library code.** Anything your future self or your colleagues or your users will call from outside is exactly the boundary where types pay back fastest. A function's signature is its contract; annotations document it and make it enforceable.

**Data structures that travel.** JSON payloads, config dicts, function return values that get handed around. A `TypedDict` makes "what keys does this have and what type is each value" machine-checkable — very often the thing that was documented only in someone's head.

**Code you'll refactor.** Any time you're about to change a function signature, remove a field from a data structure, or rename a type — type-checked code makes the scope of the change visible instantly.

**Working with `None`.** The single biggest category of bugs that types catch. `Optional[X]` forces the caller to handle both cases, and the type-checker complains if they don't.

**Onboarding.** New people reading typed code get more information faster. They can follow data flow without having to run the code or trace through call sites.

## Where type hints help less — or not at all

**Short scripts.** A 50-line analysis script that runs once and gets thrown away. The type annotations would take longer to write than the bugs they'd catch.

**Exploratory notebooks.** You're iterating on the code shape itself. Locking down types while you're still figuring out what the function should do slows you down. Annotate later, if at all.

**Highly dynamic code.** Code that builds types dynamically (metaclasses, `__getattr__` magic, plugin-loading systems) is exactly the part that's hardest to type well. You can usually *describe* the types with `Protocol` and `Any`, but the annotations get hairy fast. Sometimes it's not worth it.

**Tests.** Test code benefits less than production code — the data is under your control, the call patterns are narrow. Many teams skip annotations in tests to reduce friction.

**Trivial functions.** `def add(a: int, b: int) -> int: return a + b` is more noise than signal. The reader infers the types from the body instantly; the annotation adds nothing.

## The cost dimensions

When you're deciding whether to annotate, the cost is:

- **Time to write.** A few seconds per simple function; minutes for tricky generics.
- **Cognitive load.** Complex types (`Callable[[dict[str, list[T]]], ...]`) can be harder to read than the code they describe.
- **Maintenance.** Types drift from reality if you don't keep them accurate — a misleading annotation is worse than no annotation.
- **Tool learning curve.** mypy has quirks; understanding why it's rejecting valid code takes time up-front.

The benefit is:

- **Bugs caught early.** The ones that would have shown up as runtime errors, now visible at build time.
- **Editor help.** Better autocomplete, jump-to-definition, rename-symbol.
- **Documentation.** The signature tells you what a function does without reading the body.
- **Refactor confidence.** Change something, run mypy, see everything that's now broken.

For long-lived, multi-person codebases, the benefit clearly wins. For a throwaway script, it doesn't.

## A practical split

One good rule of thumb: **annotate the boundaries, be lazy in the middle**.

- Annotate public function signatures — parameters and returns.
- Annotate data structures that travel between functions or modules.
- Don't feel obliged to annotate every local variable — mypy infers most of them correctly.
- Don't feel obliged to annotate private helpers unless they're non-trivial or you want the documentation.

This buys you most of the benefit (type-checked function calls, typed data-flow) without the cost of annotating every last line.

## Evolving over time

A useful mental model: types aren't all-or-nothing. Gradual typing is a real feature — see the [gradual typing essay](gradual-typing.md). Start with the critical path, expand over time as the cost-benefit becomes clearer.

If you're starting a new project, start strict. If you're annotating a legacy codebase, start with the most-called functions and the most-important data structures, and expand outwards.

## The honest meta-question

Type hints are a tool with real costs. If in doubt, ask: "will this code live long enough, and be touched by enough people, that bugs caught at build time matter more than the friction of annotating?" If yes, annotate. If no, don't.

The worst outcome isn't "no types"; it's "wrong types". A misleading annotation — one that drifted from reality and now claims a return type the function doesn't actually return — is worse than no annotation, because it's actively wrong. Keep them accurate, or don't write them.
