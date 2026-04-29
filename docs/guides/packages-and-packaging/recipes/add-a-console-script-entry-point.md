# How to add a console-script entry point

# How do I turn a function in my package into a command on the user's `PATH`?

A console-script entry point tells `pip` to install a small launcher executable when your package is installed. Anyone who `pip install`s your package gets a real command they can run from any shell.

## The answer

Add a `[project.scripts]` table to `pyproject.toml`:

```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

The left side is the **command name** users will type. The right side is `module_path:function_name` — the function `pip` should call when the command runs.

Reinstall:

```bash
pip install -e .
```

That's it. `which my-tool` now finds the launcher; `my-tool --help` runs your function.

## A worked example

Given this `cli.py` inside `src/my_package/`:

```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Greet someone.")
    parser.add_argument("name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")
```

And this in `pyproject.toml`:

```toml
[project.scripts]
greet = "my_package.cli:main"
```

After `pip install -e .`, this works:

```bash
$ greet Ada
Hello, Ada!
```

`pip` installs a tiny script in the venv's `bin/` (or `Scripts/` on Windows) that imports `my_package.cli` and calls `main()`. No shebang gymnastics, no manual chmod.

## Why it works

`[project.scripts]` is part of the standard project metadata defined in PEP 621. Build backends (hatchling, setuptools, flit) all understand it. When your package is installed, the backend writes a small launcher script per entry — typically a Python file that does the import and call, with the right shebang for the venv's interpreter — and puts it in `<venv>/bin/`. Activating the venv then adds that directory to `PATH`, so the command is available.

Because the launcher imports your package rather than executing source files, **it works the same way for an editable install and a wheel install**. Users who `pip install your-package` from PyPI get the same command as you do during development.

The function pointed to should take no required arguments. By convention it's named `main`, but it doesn't have to be — `[project.scripts]` accepts any callable. If your function accepts arguments, parse them from `sys.argv` (usually via `argparse` or `click`); the launcher just calls the function and exits with whatever it returns.

## Multiple entry points

A package can register more than one command:

```toml
[project.scripts]
my-tool = "my_package.cli:main"
my-tool-debug = "my_package.cli:debug_main"
```

Group them logically by user-facing task, not by internal module structure. Two commands that share an implementation file is fine; one command that calls into three modules is also fine.

## Trade-offs

A few things to know before you scatter entry points everywhere.

**Entry points are per-environment.** The launcher script lives in the venv's `bin/`, so users still need the package installed in the venv they're using. For tools that should be available globally regardless of which venv is active, [pipx](https://pipx.pypa.io) is the conventional answer — it installs each application into its own private venv and exposes the entry-point command on the user's `PATH`.

**Name collisions are first-come-first-served on a given machine.** If two packages both register `greet`, whichever `pip install`s second wins. Pick command names that are reasonably specific to your project — `acme-greet` is safer than `greet`.

**Console scripts have a small startup cost.** The launcher imports your top-level package on every invocation, so anything heavy in `__init__.py` becomes startup overhead. Keep `__init__.py` light, especially for any package whose CLI users are likely to call in tight loops.

**Don't forget Windows.** The launcher works on all platforms, but command names that include characters Windows can't put in a filename will break the install. Stick to lowercase ASCII letters, digits, and hyphens.

## Related

- [Authoring a package](../learn/05-authoring-a-package.ipynb) — the broader walkthrough; entry points are part of the `pyproject.toml` it builds.
- [pyproject.toml field reference](../reference/pyproject-toml-field-reference.md) — the full set of `[project.*]` tables, including `gui-scripts` for GUI launchers and `[project.entry-points]` for plugin-style registration.
