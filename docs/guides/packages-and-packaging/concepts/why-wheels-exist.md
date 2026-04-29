# Why wheels exist

A Python package on PyPI is published as one or two files: a *sdist* (source distribution, `.tar.gz`) and one or more *wheels* (`.whl`). The sdist is the obvious one — a tarball of the project. The wheel takes a moment to motivate. This essay is about what problem wheels solve, and why your `pip install` is so much faster than it used to be.

## The problem with installing from source

Imagine PyPI as it existed before wheels (until around 2014). Every package was published as an sdist — essentially `tar -czf my-package.tar.gz my-package/`. Installing meant `pip` would:

1. Download the tarball.
2. Unpack it.
3. Run `setup.py install`.
4. Wait while `setup.py` did whatever the package author had decided to make it do — compile C extensions, generate code, query environment variables, run shell commands, anything.

That last step is the trap. `setup.py` is *executable Python code*, not metadata. Running `pip install` was equivalent to running an arbitrary script as you. It also meant **every install repeated all the build work**: if a package had a C extension, your machine compiled it, every time, with whatever compiler happened to be around.

For pure-Python packages this was slow. For packages with C extensions it was slow *and* error-prone — the wrong compiler version, missing system headers, a 32-bit vs 64-bit mismatch, and `pip install` would die in a wall of compiler errors that had nothing to do with Python.

## What a wheel is

A wheel is **a zip file with a deterministic name and layout** that contains a package already laid out the way `pip` will install it. Installing a wheel doesn't run any code: `pip` unzips it into `site-packages/`, drops a small metadata folder alongside, and is done.

The filename encodes the wheel's compatibility:

```text
numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl
^---^ ^----^ ^---^ ^---^ ^------------------------^
name  ver    py    abi   platform
```

- `cp312` — built for CPython 3.12.
- `cp312` (again) — uses CPython 3.12's C ABI.
- `manylinux_2_17_x86_64` — runs on any Linux from glibc 2.17 onwards, on x86_64.

For a pure-Python package, the same fields look like this:

```text
requests-2.31.0-py3-none-any.whl
                ^-^ ^--^ ^-^
                py  abi  platform
```

`py3` (any Python 3), `none` (no C ABI dependency), `any` (any platform). One wheel, every install.

## What changes for the user

Two things, both major.

**Installs become fast and predictable.** No build step, no compiler, no system headers. `pip install numpy` on a supported platform is a download and an unzip — seconds, not minutes.

**Installs become reproducible.** The wheel a CI machine produced and the wheel your laptop downloads are byte-identical. There's no "build environment" between the publish and the install for problems to creep into.

For pure-Python packages, wheels also fix a subtler issue: a wheel's metadata is *static*, sitting in a known location inside the zip. `pip` can read it without executing any of the package's code. Running `setup.py` to discover a package's dependencies — which used to be a frequent surprise — is gone.

## What changes for the author

A bit more work, but only at publish time. Building wheels requires running a build backend (`hatchling`, `setuptools`, etc.) over your project, producing the zip. For a pure-Python package this is one command:

```bash
python -m build
```

For a package with C extensions, the situation is more interesting: you need to produce one wheel per supported platform. The conventional answer is to build them in CI:

- **`cibuildwheel`** is the common workhorse — a CI-friendly tool that builds wheels for every Python version on every platform you care about, in a Docker container that matches the relevant `manylinux` baseline.
- **GitHub Actions matrix builds** wire it up — one build per (OS, Python version) combination, all uploaded together at release time.

The user sees one PyPI page with a dozen wheels attached and a single sdist as a fallback. Their `pip install` picks the wheel that matches their platform; the sdist only gets used on platforms with no matching wheel, in which case the old build-from-source dance kicks in.

## `manylinux` and friends

The trickiest part of cross-platform wheels is Linux, because Linux distributions disagree about everything — different glibc versions, different C++ runtimes, different package versions. The community's answer is the **manylinux** project, which defines a baseline OS (currently Debian-derived images for `manylinux_2_17`, `manylinux_2_28`, etc.) and asserts: a wheel built against this baseline will work on any Linux at least that new.

The platform tag in the wheel filename — `manylinux_2_17_x86_64` — names the baseline. `pip` checks your system's glibc version and uses the most recent compatible wheel. There are similar tags for other platforms: `macosx_11_0_x86_64`, `macosx_11_0_arm64`, `win_amd64`, and `musllinux_1_1_x86_64` for Alpine and other musl-based distros.

For pure-Python packages this is irrelevant — `none-any` works everywhere, and you don't need to think about it.

## Why pure-Python packages still need wheels

It's tempting to think *"I have no C extensions; an sdist is enough."* Three reasons to ship a wheel anyway.

**Speed.** A wheel install is a download and an unzip. An sdist install is a download, an unzip, *and* a build-backend invocation — even if the backend ends up doing very little, the JVM-of-your-day startup time is real.

**Static metadata.** The wheel's metadata is readable without running any package code. Tools like `pip` (and lock-file generators, dependency analysers, security scanners) can introspect a wheel without trusting it.

**No surprises during install.** With an sdist, the build backend gets a chance to fail. With a wheel, the only failure mode is a download or a checksum error.

`python -m build` produces both an sdist and a wheel by default. Publishing both is conventional and costs nothing.

## A quick way to inspect a wheel

A wheel is a zip; you can list its contents with the standard library:

```bash
python -m zipfile -l dist/my_package-0.1.0-py3-none-any.whl
```

The metadata lives in `<package>-<version>.dist-info/`. The actual installable code is at the top level of the zip — exactly the layout `pip` will create in `site-packages/`. Looking inside before you publish is a useful sanity check: are the modules where you expect, are tests *not* there, are data files included.

## Related

- [Building and publishing](../learn/06-building-and-publishing.ipynb) — the practical walkthrough that produces wheels and uploads them.
- [The PyPI ecosystem and trust](the-pypi-ecosystem-and-trust.md) — wheels also matter for trust, since they sidestep arbitrary build-time code execution.
- [The PyPA "What is a wheel?" guide](https://packaging.python.org/en/latest/discussions/package-formats/) — the canonical upstream explainer.
