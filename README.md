# Agilearn — Python Guides

This repository is the source for **agilearn.co.uk**, a unified home for thirteen self-directed Python guides written for second-year data science students and anyone learning the language seriously. The site is built with MkDocs Material; tutorial notebooks are made runnable in place using Thebe + Pyodide (the same stack that powers JupyterLite), with no backend.

## Status

All nine original standalone guides have been migrated, and four further guides (Classes and objects, Dates and times, Type hints, Iterators and generators) have been written from scratch. Every guide follows the same four-part shape — **Learn**, **Recipes**, **Reference**, **Concepts** — and recipes across the site have been rewritten to a consistent task-focused template.

Active threads of work are tracked in the planning notes at `../agilearn-plan.md` and the UX/accessibility review documents in the parent directory.

## Guides

The thirteen guides, in the recommended learning order shown in the nav:

1. Conditional logic
2. Data structures
3. Functions
4. Classes and objects
5. String processing
6. Dates and times
7. Type hints
8. Iterators and generators
9. File handling
10. Error handling
11. Logging and debugging
12. Regular expressions
13. Unit testing

Each guide lives under `docs/guides/<slug>/` with `learn/`, `recipes/`, `reference/`, and `concepts/` subdirectories.

## Layout

```
agilearn/
├── mkdocs.yml                        Unified config and full nav for all 13 guides
├── requirements.txt                  mkdocs-material, mkdocs-jupyter
├── pyproject.toml                    Installs the local notebook_link_rewriter plugin
├── wrangler.toml                     Cloudflare Pages project config
├── LICENSE.md                        Dual licence (MIT for code, CC BY 4.0 for prose)
├── overrides/                        MkDocs Material theme overrides
│   ├── main.html                     "Run code in browser" button + Thebe bootstrap + skip-link wiring
│   ├── 404.html                      Friendly 404 with links to home, guides, about, search
│   ├── partials/
│   │   ├── logo.html                 Agilearn wordmark
│   │   ├── search.html               Named search dialog (a11y)
│   │   └── source.html               Repo link partial
│   ├── assets/stylesheets/
│   │   └── agilearn.css              Brand palette, typographic scale, card grid, Thebe skin
│   └── assets/vendor/
│       ├── thebe/                    thebe@0.9.2 (index.js + thebe.css + chunks)
│       └── thebe-lite/               thebe-lite@0.5.0 (Pyodide kernel bundle)
├── plugins/
│   └── notebook_link_rewriter.py     Local MkDocs plugin
├── docs/
│   ├── index.md                      Landing page with the 13-guide card grid
│   ├── about.md
│   ├── service-worker.js             Copy of thebe-lite's SW (must live at site root)
│   ├── lab/index.md                  Redirect stub (the Lab tab has been retired)
│   └── guides/<slug>/                One folder per guide: learn / recipes / reference / concepts
└── .github/workflows/deploy.yml      GitHub Actions: MkDocs → GitHub Pages
```

## Running locally

You'll want Python 3.10+ (the deploy pipeline uses 3.12).

```bash
cd agilearn
pip install -r requirements.txt
pip install -e .                          # install the local plugin
mkdocs serve                              # http://127.0.0.1:8000
```

The in-browser Python runtime (Thebe + JupyterLite/Pyodide) is vendored as static files under `overrides/assets/vendor/`, so `mkdocs serve` gives you the full interactive experience — no extra build step. Click **Run code in browser** on any notebook page to activate.

One quirk worth knowing: `docs/service-worker.js` is a copy of `overrides/assets/vendor/thebe-lite/service-worker.js` and **must** live at the site root. JupyterLite's `PageConfig.getBaseUrl()` defaults to `/`, so the kernel tries to register the SW at `/service-worker.js`. A service worker's scope is capped by its URL path, and JupyterLite needs root scope to broker `/api/drive*` BroadcastChannel messages between the kernel and the UI. Keeping the file at `docs/service-worker.js` lets MkDocs publish it at `/` with root scope.

If you edit `overrides/main.html` or other template files, restart `mkdocs serve` — it hot-reloads Markdown but not theme overrides or CSS.

A strict build is the same one CI runs:

```bash
mkdocs build --strict
```

## Deploying

Two deploy paths are configured; pick whichever matches where the site is currently published:

- **GitHub Pages** via `.github/workflows/deploy.yml` — builds MkDocs and publishes on every push to `main`. Enable Pages in the repository settings (Source: GitHub Actions). For a custom domain, add a `CNAME` file containing `agilearn.co.uk` inside `docs/` so MkDocs copies it into the built site.
- **Cloudflare Pages** via `wrangler.toml` — the project name is `agilearn` and the build output directory is `site/`. The build command (`pip install -r requirements.txt && pip install -e . && mkdocs build --strict`) and the `PYTHON_VERSION = 3.12` build environment variable must also be set in the Cloudflare dashboard under Workers & Pages → agilearn → Settings → Build configuration; `wrangler.toml` only carries the project-level settings and the output directory.

`site_url` in `mkdocs.yml` is set to `https://agilearn.co.uk/`. JupyterLite Lab links use `site_url` as their base, so update it if you publish under a different host while the custom domain isn't live.

## What you'll see locally

Open `http://localhost:8000/` after `mkdocs serve` and you should see:

- The **Agilearn landing page** with the thirteen-guide card grid.
- Any guide rendered in the four-section shape (Learn / Recipes / Reference / Concepts), with notebook tutorials that run in the browser.
- Notebook pages with two action buttons in the top-right: **Download** and **Open in Lab**.
- Dark/light mode toggle, the indigo + ochre palette, IBM Plex Sans / IBM Plex Mono typography, the Agilearn wordmark, and unified search.
- Breadcrumbs above the page title and prev/next links at the foot of every page.
- A friendly 404 at any unknown URL.

The **Lab** tab has been retired. Every tutorial cell now has its own **Run** button, so the standalone JupyterLite tab no longer earns its keep; `docs/lab/index.md` remains as a meta-refresh stub for any old links.

## Licensing

The repository is dual-licensed — see `LICENSE.md` for the full text:

- **Code** (`.py` files, code cells in `.ipynb`, fenced and inline code in `.md`) — MIT.
- **Prose** (markdown cells in `.ipynb`, prose in `.md`, all written content) — Creative Commons Attribution 4.0 International (CC BY 4.0).

The file-type rules in `LICENSE.md` are authoritative. In mixed-content files, the licence is determined per block, not by the file extension.

## Accessibility

The site has been through a UX/accessibility review (see `../ux-a11y-review.md` and follow-up notes in the parent directory). Concrete changes already merged include the named search dialog, contrast and focus-visible fixes across both palettes, ARIA-friendly Thebe failure messaging, deduplicated nav landmarks, the custom 404, breadcrumbs, prev/next, and a robust skip-link target wired through `overrides/main.html`. Keep an eye on those documents before making theme or template changes.

## Things to revisit

- **Branding.** The 2026 refresh refined the indigo + ochre identity, the IBM Plex type pairing, the modular type scale and the warm-grey neutrals — but the wordmark in `overrides/partials/logo.html` is still text-only. Replace it with an SVG when there's a finished logo, and tweak the palette variables at the top of `overrides/assets/stylesheets/agilearn.css` if needed.
- **Content gaps.** See `../agilearn-plan.md` for the running list of topics that arguably belong in the Agilearn collection but aren't yet covered.
- **Recipe template consistency.** Recipes have been rewritten to a task-focused template; new recipes should follow the same shape rather than the older Diátaxis-flavoured how-to format.
- **Deploy target.** Both `deploy.yml` and `wrangler.toml` are present; if only one platform is actually serving the site, retire the other to avoid confusion.
