# pip command quick reference

The handful of `pip` commands you'll actually use, with the flags that matter.

`pip` and `python -m pip` do the same thing, but `python -m pip` guarantees you're using the `pip` that belongs to the currently-active Python — useful when multiple Pythons are in your `PATH`. Most of the examples below use the bare form for brevity; substitute `python -m pip` where you need the certainty.

## Installing

### `pip install <package>`

Install the latest release of a package and its dependencies from PyPI.

```bash
pip install requests
```

### `pip install <package>==<version>`

Install a specific version. Use `==`, `>=`, `<`, `~=` to express ranges.

```bash
pip install "requests==2.31.0"
pip install "requests>=2.30,<3"
pip install "requests~=2.31.0"     # patch updates only
```

Quote the spec — your shell may treat `<` and `>` as redirection.

### `pip install -r <file>`

Install everything listed in a requirements file.

```bash
pip install -r requirements.txt
```

### `pip install -e <path>`

Editable install — install a package from a local directory by linking, so source edits are picked up without re-installing.

```bash
pip install -e .              # current directory
pip install -e ./my-package   # a sibling directory
```

### `pip install ".[extra1,extra2]"`

Install a package with one or more optional-dependency groups.

```bash
pip install ".[test]"
pip install ".[test,dev]"
```

### `pip install --upgrade <package>`

Upgrade an installed package to the latest version.

```bash
pip install --upgrade requests
pip install -U requests        # short form
```

### `pip install --index-url <url>`

Use a non-default package index — TestPyPI, a private mirror, or a wheelhouse.

```bash
pip install --index-url https://test.pypi.org/simple/ my-package
```

### `pip install --require-hashes -r <file>`

Refuse to install any package whose downloaded hash doesn't match the one in the requirements file. The standard guard for production deploys.

```bash
pip install --require-hashes -r requirements.txt
```

## Inspecting

### `pip list`

Show installed packages and their versions.

```bash
pip list
pip list --outdated         # only those with newer releases available
pip list --format=freeze    # in requirements.txt format
```

### `pip show <package>`

Show metadata for one package: version, location, dependencies, and dependants.

```bash
pip show requests
```

### `pip freeze`

List installed packages in `requirements.txt` format. Useful for snapshotting a working environment, but includes transitive dependencies — usually you want a hand-curated `requirements.in` instead.

```bash
pip freeze > requirements.txt
```

### `pip check`

Verify that all installed packages have compatible dependencies. Reports conflicts but doesn't fix them.

```bash
pip check
```

## Uninstalling

### `pip uninstall <package>`

Remove a package. **Does not** remove its dependencies — those stay behind. Use a fresh venv when you need a clean slate.

```bash
pip uninstall requests
pip uninstall -y requests        # don't prompt for confirmation
```

## Useful flags

| Flag | Purpose |
|---|---|
| `--user` | Install into the user's site-packages instead of the system or venv. Use a venv instead. |
| `--no-deps` | Install only the named package; skip its dependencies. |
| `--no-build-isolation` | Build in the current environment instead of an isolated one. Faster but rare. |
| `--dry-run` | Resolve and report what would be installed; install nothing. |
| `--pre` | Allow pre-releases in version resolution. |
| `--no-cache-dir` | Don't read or write the local download cache. |
| `-v`, `-vv`, `-vvv` | Increasingly verbose output; useful when an install is doing something unexpected. |

## Building (requires the `build` package)

Strictly speaking these aren't `pip` commands, but they pair with it.

```bash
pip install build
python -m build         # builds sdist + wheel into dist/
python -m build --sdist
python -m build --wheel
```

## Publishing (requires `twine`)

```bash
pip install twine
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

## Related

- [Installing third-party packages](../learn/03-installing-third-party-packages.ipynb) — the tutorial walkthrough.
- [Pin and lock dependencies](../recipes/pin-and-lock-dependencies.md) — when to use ranges, exact pins, and lock files.
- [Building and publishing](../learn/06-building-and-publishing.ipynb) — what the build and upload commands actually do.
