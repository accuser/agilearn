---
title: Learn
---

# Learn: Packages and packaging

Six short tutorials that take you from `import math` to publishing your own package on PyPI. Each one is a Jupyter notebook — read it in the browser, and edit and run any code cell directly on the page.

The tutorials build on each other, so working through them in order is the fastest path. Each takes roughly fifteen to twenty minutes.

## The sequence

1. **[Modules and imports](01-modules-and-imports.ipynb)** — what `import` actually does; `sys.modules`, `sys.path`, and `__name__`.
2. **[Packages and namespaces](02-packages-and-namespaces.ipynb)** — directories with `__init__.py`, sub-packages, and absolute vs relative imports.
3. **[Installing third-party packages](03-installing-third-party-packages.ipynb)** — `pip`, PyPI, pinning versions, and `requirements.txt`.
4. **[Virtual environments](04-virtual-environments.ipynb)** — `python -m venv`, activation, and the per-project workflow.
5. **[Authoring a package](05-authoring-a-package.ipynb)** — the `src/` layout, `pyproject.toml`, and editable installs.
6. **[Building and publishing](06-building-and-publishing.ipynb)** — `python -m build`, TestPyPI, and PyPI.

## A note on running the code

Tutorials 1, 2, and 5 use Python you can run directly on the page. Tutorials 3, 4, and 6 cover tools that live outside Python — `pip`, `venv`, `python -m build`, and friends — which need a real terminal. Where a code block is shell-only, it's flagged with a callout; copy the commands into your shell to follow along.

## Before you start

You'll get more from these if you're already comfortable with Python functions, modules, and basic file I/O. If you've not yet worked through the [Functions](../../functions/) and [File handling](../../file-handling/) guides, those are good warm-ups.
