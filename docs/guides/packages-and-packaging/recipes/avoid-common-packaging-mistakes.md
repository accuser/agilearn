# How to avoid common packaging mistakes

# What are the most common mistakes when packaging Python code?

Most packaging bugs come from a small, well-known set of traps. The most expensive ones are silent failures — a package that installs cleanly but quietly leaves files behind, or a release that publishes successfully but is missing a module. This is a quick reference to the patterns to watch for.

## The answer

| Trap | What happens | What to do instead |
|---|---|---|
| Hyphens in import names | `pyproject.toml` says `name = "my-package"`, but `import my-package` is a syntax error | Distribution name can have hyphens; **import name** must be a valid identifier (`my_package`) |
| Code at the top level instead of under `src/` | Tests can import from the source tree even when the install is broken; you don't notice | Use the `src/` layout |
| Bumping `version` in `pyproject.toml` but not in `__init__.py` | `your_pkg.__version__` and the package metadata disagree | Use a single source of truth (e.g. `[tool.hatch.version]` reading from `__init__.py`) |
| Forgetting to add a new dependency to `pyproject.toml` | Works on your machine; breaks for users with a clean install | Audit imports against `dependencies` before each release |
| Using `pip install` on the system Python | Pollutes the system; on Linux/macOS may break OS tools | Always work inside a venv |
| `pip install --upgrade <pkg>` without a venv | Same problem at scale — silently changes the version of something the OS depends on | Same answer — venv |
| Re-using a version number after a publish | PyPI rejects the upload | Bump the version, then publish |
| Including secrets, large data files, or `__pycache__` in the wheel | Slow installs; potential security incidents | Configure `[tool.hatch.build]` (or your backend's equivalent) to exclude them; inspect with `python -m zipfile -l dist/*.whl` |
| Pinning exact versions in a *library*'s `pyproject.toml` | Library can't be installed alongside other packages with overlapping deps | Use ranges (`>=2.30,<3`) for library deps; pin only in applications |
| Ignoring `requires-python` | Library installs into Pythons it was never tested on | Set `requires-python = ">=3.10"` to a real, tested floor |
| Uploading directly to PyPI without trying TestPyPI first | Mistakes are permanent — version 0.1.0 is forever | Always upload to TestPyPI; verify the install; *then* PyPI |
| Putting tests inside the package directory | Tests get installed as part of the package; users can `import` them by accident | Tests live in a sibling `tests/` directory, not under `src/<package>/` |

## Why it works

**Distribution name vs import name.** PyPI accepts hyphens in distribution names because it's primarily a UI for humans (`pip install my-package` reads cleanly). But hyphens are operators in Python, so `import my-package` doesn't parse. The convention — distribution `my-package`, import `my_package` — is conventional precisely so users don't have to think about it: hyphens for the install command, underscores for the `import`.

**The `src/` layout's value isn't aesthetic.** Without it, your tests can import the source tree directly, even when the install is broken — Python sees `report_tools/` in the working directory and uses it. With it, the only way `import report_tools` resolves is if the package is properly installed, so tests fail loudly when something is wrong with the install. This catches a whole class of "works for me, breaks in production" bugs at the test step instead of at deploy time.

**Version drift.** When `pyproject.toml` says `0.2.0` and `__init__.py` says `0.1.0`, every part of your release pipeline assumes a different version is current. Single source of truth — typically the version in `__init__.py`, with hatch (or whatever backend) configured to read from there — eliminates the entire class of problem.

**Library pinning.** A library's `pyproject.toml` is a constraint for everyone else's install. If your library pins `requests==2.31.0` and any other library in the same install pins a different version, `pip` can't satisfy both. Ranges leave room for the resolver. Applications, in contrast, are the *terminal* node of a dependency graph — pinning exactly is fine and often desirable.

**`requires-python`.** `pip` checks this before it even starts the install, so a clear lower bound prevents a confusing class of "imports work, then fail at runtime on `match`/`case`" errors. If your code uses 3.10 syntax, set `requires-python = ">=3.10"` — *and* test against 3.10, not just the latest.

**Test directory placement.** Tests inside `src/<package>/tests/` get included in the wheel by default. Users `pip install`ing your package end up with your test files in their environment, and worse, can `import your_package.tests`. A sibling `tests/` directory keeps tests out of the wheel without any extra configuration.

## Trade-offs

Some of these have edges worth knowing.

**The `src/` layout costs you a tiny bit of friction during ad-hoc scripts.** You can't run `python my_module.py` from inside the package any more — you have to use `python -m my_package.my_module`. For a project that's properly packaged, that's a small price. For a one-off folder of utilities, it's overhead you might not need.

**Single-source-of-truth versioning** sometimes conflicts with reproducible builds — if hatch reads the version from `__init__.py` at build time, the version isn't visible until the package is installed. Most projects don't care; if you do, set the version in `pyproject.toml` directly and accept the small duplication.

**Pinning ranges in libraries isn't free.** A range that's too loose admits future versions you haven't tested against — and which can break your library. The mitigation is honest CI: test against the upper bound you declare, not just the latest, and bump the upper bound deliberately when you've validated the new version.

## Related

- [Authoring a package](../learn/05-authoring-a-package.ipynb) — the walkthrough that builds the layout these traps assume.
- [Pin and lock dependencies](pin-and-lock-dependencies.md) — when ranges are right and when exact pins are.
- [Resolve import errors](resolve-import-errors.md) — when the trap has already caught you.
- [Project layout](../reference/project-layout.md) — `src/` vs flat, with more on the trade-offs.
