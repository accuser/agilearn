# pyproject.toml field reference

Every field you'll commonly use in a `pyproject.toml`, with notes on the values each accepts.

A `pyproject.toml` typically has three top-level tables: `[build-system]` (which build backend to use), `[project]` (the package's metadata), and `[tool.<name>]` (configuration for individual tools). The first two are standardised; the third is per-tool.

## `[build-system]`

Defines how `pip` should build your package. PEP 517.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

| Field | Type | Description |
|---|---|---|
| `requires` | list of strings | Packages needed *to build* (not to use) the package. `pip` installs these in an isolated environment before invoking the backend. |
| `build-backend` | string | Dotted path to the backend's build-API entry point. |
| `backend-path` | list of strings | Optional. Paths added to `sys.path` for in-tree backends. Rare. |

Common backend choices:

| Backend | `build-backend` | Notes |
|---|---|---|
| hatchling | `hatchling.build` | Modern, low-config; the recommended default for new projects. |
| setuptools | `setuptools.build_meta` | The classic; pair with `requires = ["setuptools>=61"]` for `pyproject.toml` support. |
| flit-core | `flit_core.buildapi` | Minimal, opinionated; good for pure-Python single-module packages. |
| poetry-core | `poetry.core.masonry.api` | Used by Poetry projects. |
| pdm-backend | `pdm.backend` | Used by PDM projects. |

## `[project]`

The package's metadata. PEP 621.

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "A short, one-line summary."
readme = "README.md"
requires-python = ">=3.10"
authors = [{ name = "Ada Lovelace", email = "ada@example.com" }]
maintainers = [{ name = "Grace Hopper", email = "grace@example.com" }]
license = { text = "MIT" }
keywords = ["greeting", "example"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = [
    "requests>=2.30",
    "click~=8.1",
]
```

### Required fields

| Field | Type | Description |
|---|---|---|
| `name` | string | The distribution name on PyPI. May contain hyphens. |
| `version` | string | A PEP 440 version string, or omitted with `dynamic = ["version"]` and the value sourced elsewhere. |

### Common metadata

| Field | Type | Description |
|---|---|---|
| `description` | string | One-line summary, shown in `pip show` and on PyPI. |
| `readme` | string or table | Path to the README, or a table specifying file and content type. |
| `requires-python` | string | A PEP 440 version specifier; the Python versions your package supports. |
| `authors`, `maintainers` | list of tables | Each `{ name = "...", email = "..." }`. Either field is optional in each entry. |
| `license` | table | `{ text = "MIT" }` for an SPDX expression, or `{ file = "LICENSE" }` to point at a file. |
| `keywords` | list of strings | Free-form keywords for PyPI search. |
| `classifiers` | list of strings | Standardised tags from [pypi.org/classifiers](https://pypi.org/classifiers/). |

### Dependencies

| Field | Type | Description |
|---|---|---|
| `dependencies` | list of strings | Runtime dependencies, each in PEP 508 spec format (`"requests>=2.30"`). |
| `optional-dependencies` | table | Named groups of optional dependencies. Install with `pip install ".[group]"`. |
| `dynamic` | list of strings | Names of fields the build backend will fill in (e.g. `["version"]`). |

### URLs

```toml
[project.urls]
Homepage = "https://example.com/my-package"
Documentation = "https://example.com/my-package/docs"
Repository = "https://github.com/example/my-package"
Issues = "https://github.com/example/my-package/issues"
Changelog = "https://github.com/example/my-package/blob/main/CHANGELOG.md"
```

Each link appears on the package's PyPI page.

### Entry points

```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

| Table | Purpose |
|---|---|
| `[project.scripts]` | Console-script entry points: a command on the user's `PATH` that calls a function. |
| `[project.gui-scripts]` | Like `scripts`, but invoked without a console window on Windows. |
| `[project.entry-points."<group>"]` | Plugin-style registration — packages declare callables under named groups, and other packages discover them with `importlib.metadata.entry_points`. |

## `[tool.<name>]` — backend and tool configuration

This table is the per-tool playground. Each tool defines its own subsection.

### Hatchling examples

```toml
[tool.hatch.version]
path = "src/my_package/__init__.py"   # read version from __init__.py
```

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]         # explicit, but hatchling auto-detects too
```

### Setuptools examples

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### Other tools you'll commonly see

`[tool.ruff]`, `[tool.black]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]` — each tool documents its own keys.

## A worked minimal `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "report-tools"
version = "0.1.0"
description = "Internal tools for the weekly report."
readme = "README.md"
requires-python = ">=3.10"
authors = [{ name = "Ada Lovelace" }]
license = { text = "MIT" }
dependencies = [
    "requests>=2.30",
    "pandas>=2.0",
]

[project.optional-dependencies]
test = ["pytest>=7", "pytest-cov"]
dev = ["mypy", "ruff"]

[project.scripts]
report-tools = "report_tools.cli:main"

[project.urls]
Repository = "https://github.com/example/report-tools"
```

## Related

- [Authoring a package](../learn/05-authoring-a-package.ipynb) — the walkthrough that builds one of these from scratch.
- [Project layout](project-layout.md) — where the package code goes alongside this file.
- [PyPA `pyproject.toml` guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) — the canonical upstream reference.
