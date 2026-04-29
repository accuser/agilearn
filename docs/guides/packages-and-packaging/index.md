---
title: Packages and packaging
---

# Packages and packaging

When your code outgrows a single file, packaging is the answer. This guide covers both halves of the topic: the consumer side — `import`, `pip`, virtual environments, and where third-party code comes from — and the author side — laying out a project, writing a `pyproject.toml`, and publishing your work. By the end, you should understand the import system well enough to diagnose the trickiest `ModuleNotFoundError`, and feel confident shipping a package of your own.

## Start here

If imports beyond `from collections import Counter` still feel a little mysterious, work through the [**Learn**](learn/) section in order — six short notebooks taking you from imports through to publishing.

If you're already comfortable with `pip` and `venv` and just want to ship a package, jump ahead to *Authoring a package* and *Building and publishing* in the [Learn](learn/) section, or skip to the [**Recipes**](recipes/) for task-focused walkthroughs.

## What this guide covers

**[Learn](learn/)** — modules and imports, packages and namespaces, installing third-party code, virtual environments, authoring your own package, and publishing it.

**[Recipes](recipes/)** — pinning dependencies, turning a script folder into a package, adding console-script entry points, resolving import errors, and the mistakes worth avoiding.

**[Reference](reference/)** — `import` statement forms, `pip` commands, `pyproject.toml` fields, and the canonical project layout.

**[Concepts](concepts/)** — how Python's import system actually works, why wheels exist, and the PyPI ecosystem.

## A note on running the code

Several notebooks in this guide cover tools that live outside Python — `pip`, `venv`, `python -m build`, and so on. These run in your terminal, not in the browser-based Python kernel that powers the rest of Agilearn. Where a code block won't run on the page, it's flagged with a callout; copy the commands into a real shell to follow along.
