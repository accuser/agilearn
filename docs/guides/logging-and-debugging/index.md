---
title: Logging and debugging
---

# Logging and debugging

When a program does the wrong thing, you need two tools: a way to see what it was doing (logging) and a way to stop it and poke around (debugging). Python gives you a surprisingly capable version of each in the standard library — `logging` for structured, level-aware observability, and `pdb` for interactive stepping. This guide covers both, and the judgement calls for when to reach for which.

## Start here

If logging or `pdb` is new to you, work through the [**Learn**](learn/) section in order — four short notebooks, around fifteen minutes each. Every code cell can be edited and run in place, directly on the page; no install required.

If you already know the basics and are looking for a specific technique, jump to the [**Recipes**](recipes/) section, or scan the [**Reference**](reference/) for `logging` methods and `pdb` commands.

## What this guide covers

**[Learn](learn/)** — your first log message, log levels and formatting, logging to files, debugging with `pdb`.

**[Recipes](recipes/)** — project-wide logging configuration, custom handlers, effective breakpoints, common mistakes to avoid.

**[Reference](reference/)** — `logging` module API, log-format directives, `pdb` command list.

**[Concepts](concepts/)** — understanding log levels, and why logging beats `print` for anything beyond a scratch script.
