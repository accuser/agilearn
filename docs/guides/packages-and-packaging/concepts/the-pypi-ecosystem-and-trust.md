# The PyPI ecosystem and trust

The Python Package Index — PyPI — is the centre of gravity for third-party Python. It's also an open package index, which means anyone with an email address can publish to it. That openness is responsible for both the size of the ecosystem and its riskiest sharp edges. This essay is about the trust model PyPI ships with, and what to do about it.

## What PyPI is

PyPI is a public registry of Python packages, accessible at [pypi.org](https://pypi.org). When you `pip install requests`, `pip` queries PyPI for the package, downloads the most appropriate file (a wheel if one matches your platform, otherwise the sdist), verifies the checksum the index provided, and installs.

The numbers, last time anyone counted: hundreds of thousands of packages, hundreds of millions of downloads a day. A non-trivial portion of the world's Python is held together by PyPI being available.

The service is run by the Python Packaging Authority (PyPA), a working group under the Python Software Foundation. It's free to use, both for publishers and consumers.

## The trust model: open by default

Anyone can publish a package, which is both PyPI's strength and the source of the risks below. There's no editorial review. There's no manual vetting before a package goes live. The first time you `pip install some-name`, you're trusting:

- **The package author.** Whoever pushed `some-name`'s code is the same kind of stranger as anyone else with internet access. Verified GitHub-style authorship doesn't exist in the protocol.
- **The package author's account.** If someone reuses a weak password or gets phished, malicious uploads can appear from a previously trustworthy account.
- **PyPI itself.** The index is operated reliably, but it's still a single point of trust — if it were compromised, malicious packages could be served under legitimate names.
- **Every transitive dependency** of the package, recursively. A package with a thousand-line tree of dependencies is a thousand lines of code from a thousand authors.

For most uses, this trust is well-placed. Popular packages are watched by enough people that malicious changes are spotted quickly, and PyPI itself is operated to a high security standard. But the *default* — install anything, run all of its code — is permissive in a way most users don't think about until they have to.

## The categories of risk

There's no need to be paranoid, but knowing what can go wrong is the foundation of knowing what to do.

**Typosquatting.** Someone publishes `requests-py` (or `reqests`, or `python-requests`) hoping you'll install it by accident. The package, once installed, executes whatever code its author put in it. Real, ongoing — PyPI removes squats when it spots them, but the rate of new ones is non-trivial.

**Account takeover.** A legitimate package's account is compromised, and a malicious version is published. Users who run `pip install --upgrade` get the malicious version. The chain-reaction risk is highest for low-popularity packages with high-popularity dependants.

**Confused-deputy / dependency confusion.** A company has a *private* package called `internal-tools`. An attacker publishes a package with the same name to public PyPI at a higher version. The company's `pip install` — if not configured carefully — pulls the public one, executes its code inside the company network.

**Build-time execution.** An sdist is allowed to run arbitrary code at install time via `setup.py`. A malicious sdist can do anything the user running `pip install` can. (Wheels avoid this — they don't execute code at install — which is one of the reasons wheels matter.)

**Supply-chain compromises further down.** Even if every direct dependency is trustworthy, *their* dependencies might not be. Compromise propagates through the import graph.

## What to actually do

This isn't theoretical, but the mitigations are mostly easy and cumulative — most projects can adopt all of them without much friction.

### Pin and lock

Pinning gives you a *snapshot* of what's known to work. A lock file pins not just your direct dependencies but every transitive one, with hashes:

```bash
pip-compile --generate-hashes requirements.in
pip install --require-hashes -r requirements.txt
```

`--require-hashes` refuses to install any file whose downloaded bytes don't match the expected hash. This means even if PyPI is compromised between your `pip-compile` and your `pip install`, the install will fail rather than silently substitute a different file.

This is by some distance the highest-leverage thing you can do. See [Pin and lock dependencies](../recipes/pin-and-lock-dependencies.md) for the full workflow.

### Read what you install

Before adding a new dependency, especially a small one:

- Look at the project on PyPI. How long has it existed? How many releases? Who maintains it?
- Look at the source repository (linked from the PyPI page). Is it active? Does the code look reasonable? Are there issues and PRs from real-looking people?
- For small packages, *read the source*. A 200-line package takes ten minutes; a malicious 200-line package usually has a giveaway.

### Use trusted publishing or scoped tokens

When you publish, don't ship account passwords:

- **API tokens** scoped to a single project mean a leaked token can't be used to upload to anything else.
- **Trusted publishing** ([docs.pypi.org/trusted-publishers](https://docs.pypi.org/trusted-publishers/)) lets PyPI accept uploads from a specific GitHub Actions workflow without any secret at all — no credential to leak.

For projects released from public repositories, trusted publishing is the recommended default. Configure it once; you stop thinking about secret rotation forever.

### Use a private index for private code

Don't rely on the company name alone to keep `internal-tools` out of attackers' reach. If a package is private, host it in a private index — Artifactory, devpi, AWS CodeArtifact, GitHub Packages — and configure `pip` to consult that index instead of (or alongside) PyPI:

```bash
pip install --index-url https://internal-pypi.example.com/simple/ internal-tools
```

If you must mix public and private dependencies, **`--extra-index-url` is dangerous** without further controls — it creates the dependency-confusion vulnerability. Tools like `pip`'s `--index-strategy unsafe-best-match`/`--index-strategy first-index` (in newer versions) let you say "private index always wins on name collisions"; configure it explicitly.

### Think about updates as security events

`pip install --upgrade` isn't a free action — it's a moment when new code starts running on your machine. For libraries you depend on heavily, watch the release notes. For applications, prefer regenerating your lock file as a deliberate, reviewed step rather than auto-updating in CI.

For a periodic sweep of known vulnerabilities, [pip-audit](https://github.com/pypa/pip-audit) cross-references your installed packages against the [Python Packaging Advisory Database](https://github.com/pypa/advisory-database):

```bash
pip install pip-audit
pip-audit
```

Run it in CI. Treat findings the way you'd treat any other CI failure.

## What PyPI does on its end

PyPI isn't passive. The platform has invested heavily in defences:

- **Mandatory two-factor authentication** for all maintainers.
- **Provenance attestations** for trusted publishers, recording which workflow produced each upload.
- **Project quarantine and removal** for confirmed malicious uploads.
- **Account compromise detection** by monitoring for suspicious patterns.

These are real protections, and they raise the floor. They don't replace the user-side mitigations above; they complement them.

## In practice

For most projects, the right baseline is:

1. Use a venv per project. (Already covered in [Virtual environments](../learn/04-virtual-environments.ipynb).)
2. Pin direct dependencies in `pyproject.toml` or `requirements.in`.
3. Lock the full graph with hashes for deployment.
4. Run `pip-audit` in CI.
5. Use trusted publishing for releases.

That's not paranoid; it's hygiene. The PyPI ecosystem is open by design, and the price of that openness is being deliberate about what you trust. The good news is that the deliberate part is mostly a one-time setup; once it's in place, you can install almost anything almost anywhere with reasonable confidence.

## Related

- [Pin and lock dependencies](../recipes/pin-and-lock-dependencies.md) — the practical "how" for pinning, locking, and hashing.
- [Building and publishing](../learn/06-building-and-publishing.ipynb) — where trusted publishing fits.
- [Why wheels exist](why-wheels-exist.md) — wheels also reduce trust surface by removing arbitrary install-time code execution.
