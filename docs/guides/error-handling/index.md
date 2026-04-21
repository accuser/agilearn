---
title: Error handling
---

# Error handling

Things go wrong. Files don't exist, networks drop, users type nonsense. Python's exception system is how your program responds to those moments — by recovering cleanly, by failing loudly, or by passing the problem up to someone who can do something about it. This guide takes you from your first `try`/`except` to writing your own exception types, and to the trickier question of when *not* to catch.

## Start here

If exceptions are new to you, work through the [**Learn**](learn/) section in order — four short notebooks, around fifteen minutes each. Every code cell can be edited and run in place, directly on the page; no install required.

If you already know the basics and are looking for a specific technique, jump to the [**Recipes**](recipes/) section, or scan the [**Reference**](reference/) for syntax and the built-in exception hierarchy.

## What this guide covers

**[Learn](learn/)** — your first exception, exception types, raising exceptions, cleanup with `finally`.

**[Recipes](recipes/)** — handling multiple exceptions, custom exceptions, context managers, common mistakes to avoid.

**[Reference](reference/)** — `try`/`except` syntax, built-in exceptions, the exception hierarchy.

**[Concepts](concepts/)** — why error handling matters, how exceptions propagate through the call stack.
