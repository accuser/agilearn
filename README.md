# Agilearn — Python Guides

This repository is the source for **agilearn.co.uk**, a unified home for nine self-directed Python guides, migrated from their original standalone micro-sites and wrapped in a single branded MkDocs-Material site. Tutorial notebooks are made runnable in place using Thebe + Pyodide (the same stack that powers JupyterLite), with no backend.

## Status

This is a prototype. The `python-functions` guide is fully migrated. The other eight guides are present as placeholder landing pages that link to the archived standalone sites; their content migration is the Phase 2 work described in the plan document (see `../agilearn-plan.md`).

## Layout

```
agilearn/
├── mkdocs.yml                   Unified config, nav for all 9 guides
├── requirements.txt             mkdocs-material, mkdocs-jupyter
├── pyproject.toml               Installs the local notebook_link_rewriter plugin
├── overrides/                   MkDocs Material theme overrides
│   ├── main.html                "Run code in browser" button + Thebe bootstrap
│   ├── partials/logo.html       Agilearn wordmark
│   ├── assets/stylesheets/
│   │   └── agilearn.css         Brand palette, card grid, Thebe skin
│   └── assets/vendor/
│       ├── thebe/               thebe@0.9.2 (index.js + thebe.css + chunks)
│       └── thebe-lite/          thebe-lite@0.5.0 (Pyodide kernel bundle)
├── plugins/
│   └── notebook_link_rewriter.py    (lifted once from the original repos)
├── docs/
│   ├── index.md                 Landing page with the 9-guide card grid
│   ├── about.md
│   ├── service-worker.js        Copy of thebe-lite's SW (must live at site root)
│   └── guides/
│       ├── functions/           Fully migrated (Learn/Recipes/Reference/Concepts)
│       └── <other 8>/           Placeholder index.md pages
└── .github/workflows/deploy.yml GitHub Actions: MkDocs → GitHub Pages
```

## Running locally

You'll want Python 3.10+.

```bash
cd agilearn
pip install -r requirements.txt
pip install -e .                          # install the local plugin
mkdocs serve                              # http://127.0.0.1:8000
```

The in-browser Python runtime (Thebe + JupyterLite/Pyodide) is vendored as static files under `overrides/assets/vendor/`, so `mkdocs serve` gives you the full interactive experience — no extra build step. Click **Run code in browser** on any notebook page to activate.

One quirk worth knowing: `docs/service-worker.js` is a copy of `overrides/assets/vendor/thebe-lite/service-worker.js` and **must** live at the site root. JupyterLite's `PageConfig.getBaseUrl()` defaults to `/`, so the kernel tries to register the SW at `/service-worker.js`. A service worker's scope is capped by its URL path, and JupyterLite needs root scope to broker `/api/drive*` BroadcastChannel messages between the kernel and the UI. Keeping the file at `docs/service-worker.js` lets MkDocs publish it at `/` with root scope.

If you edit `overrides/main.html` or other template files, restart `mkdocs serve` — it hot-reloads Markdown but not theme overrides or CSS.

## Deploying

The included `.github/workflows/deploy.yml` builds MkDocs and publishes to GitHub Pages on every push to `main`. Enable Pages in the repository settings (Source: GitHub Actions), and for a custom domain add `CNAME` with `agilearn.co.uk` inside the `docs/` directory so MkDocs copies it into the built site.

## What the prototype demonstrates

Open `http://localhost:8000/` after `mkdocs serve` and you should see:

- The **Agilearn landing page** with the nine-guide card grid.
- The **Functions guide**, fully migrated: section names renamed from Tutorials/How-to/Reference/Explanation to **Learn/Recipes/Reference/Concepts**, all Diátaxis meta-prose removed.
- A notebook page with two action buttons in the top-right: **Download** and **Open in Lab**.
- The **Lab** page (Lab tab in the header) with the embedded JupyterLite interface, once you've done a full static build.
- Dark/light mode toggle, the indigo + gold palette, the Agilearn wordmark, and unified search.

## Migrating the remaining eight guides

The pattern is identical for every guide:

1. Copy `../<guide>/docs/<section>/` into `docs/guides/<slug>/<renamed-section>/` using the folder map:
   - `tutorials` → `learn`
   - `how-to` → `recipes`
   - `reference` → `reference`
   - `explanation` → `concepts`
2. Rewrite `guides/<slug>/index.md` (guide landing) to drop the Diátaxis meta-prose.
3. Rewrite the four `<section>/index.md` files to drop meta-prose and point at the new section names.
4. Copy the tutorial and recipe notebooks into `jupyterlite/content/guides/<slug>/<section>/`.
5. Add the guide's full nav block to `mkdocs.yml`, mirroring the `Functions:` block.
6. `mkdocs build --strict` should pass with no new warnings.

A migration script that automates steps 1, 4, and most of 3 is feasible — the file layouts are identical across the nine repos. Worth writing when Phase 2 begins.

## Things to revisit

- **Branding.** The wordmark and palette are sensible defaults, not a finished identity. Replace `overrides/partials/logo.html` with an SVG when you have a logo, and tweak the palette variables at the top of `overrides/assets/stylesheets/agilearn.css`.
- **Conditional-logic guide content.** The source repo has only one tutorial notebook. The placeholder lists what's expected when this guide is written out in full.
- **Content gaps.** See `../agilearn-plan.md` for the list of topics that arguably belong in the Agilearn collection but aren't in any of the nine current repos (modules & imports, iteration, classes, etc.).
- **Domain configuration.** The `site_url` in `mkdocs.yml` assumes `https://agilearn.co.uk/`. If the domain isn't live yet, set it to the GitHub Pages URL in the meantime — JupyterLite Lab links use `site_url` as their base.
