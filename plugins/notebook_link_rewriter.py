"""
MkDocs plugin to rewrite relative links in Jupyter notebooks to absolute URLs.

This plugin processes copied Jupyter notebooks in the site output directory,
converting relative links to absolute URLs pointing to the published site.
This ensures that downloaded notebooks retain working links back to the site.
"""

import json
import logging
import os
import re
from pathlib import Path

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

log = logging.getLogger("mkdocs.plugins.notebook_link_rewriter")


class NotebookLinkRewriterPlugin(BasePlugin):
    """Plugin to rewrite relative links in notebooks to absolute URLs."""

    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
        ("site_url", config_options.Type(str, default="")),
    )

    def on_post_build(self, config):  # type: ignore[override]
        """
        Run after the site is built to rewrite links in notebooks and HTML.

        This hook processes all .ipynb and .html files in the site directory,
        rewriting relative links with file extensions to clean directory URLs.

        Args:
            config: The MkDocs configuration object
        """
        if not self.config["enabled"]:
            log.info("Notebook link rewriter plugin is disabled")
            return

        # Get site URL from plugin config or mkdocs config
        site_url = self.config.get("site_url") or config.get("site_url", "")

        if not site_url:
            log.warning(
                "No site_url configured. Notebook links will not be rewritten. "
                "Set site_url in mkdocs.yml or plugin config."
            )
            return

        # Remove trailing slash from site_url
        site_url = site_url.rstrip("/")

        site_dir = Path(config["site_dir"])

        # Process notebook files (.ipynb) - rewrite to absolute URLs
        notebook_files = list(site_dir.rglob("*.ipynb"))
        log.info(f"Processing {len(notebook_files)} notebook files...")

        notebook_processed = 0
        for notebook_path in notebook_files:
            if self._rewrite_notebook_links(notebook_path, site_url, site_dir):
                notebook_processed += 1

        # Process HTML files - rewrite to clean relative URLs
        html_files = list(site_dir.rglob("*.html"))
        log.info(f"Processing {len(html_files)} HTML files...")

        html_processed = 0
        for html_path in html_files:
            if self._rewrite_html_links(html_path, site_dir):
                html_processed += 1

        log.info(
            f"Notebook link rewriter: Processed {notebook_processed} notebooks, "
            f"{html_processed} HTML files"
        )

    def _rewrite_notebook_links(self, notebook_path: Path, site_url: str, site_dir: Path) -> bool:
        """
        Rewrite relative links in a single notebook file.

        Args:
            notebook_path: Path to the .ipynb file
            site_url: Base URL of the published site
            site_dir: Path to the site output directory

        Returns:
            True if notebook was modified, False otherwise
        """
        try:
            # Read the notebook
            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)

            # Track if any changes were made
            modified = False

            # Get the notebook's directory relative to site root
            # E.g., site/tutorials/01-your-first-test/notebook.ipynb -> tutorials/01-your-first-test
            notebook_dir = notebook_path.parent.relative_to(site_dir)

            # Process each cell
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "markdown":
                    source = cell.get("source", [])

                    # Handle both list and string formats
                    if isinstance(source, list):
                        new_source = []
                        for line in source:
                            new_line = self._rewrite_links_in_text(
                                line, site_url, notebook_dir
                            )
                            new_source.append(new_line)
                            if new_line != line:
                                modified = True
                        cell["source"] = new_source
                    elif isinstance(source, str):
                        new_source = self._rewrite_links_in_text(
                            source, site_url, notebook_dir
                        )
                        if new_source != source:
                            cell["source"] = new_source
                            modified = True

            # Write back if modified
            if modified:
                with open(notebook_path, "w", encoding="utf-8") as f:
                    json.dump(notebook, f, ensure_ascii=False, indent=1)
                log.debug(f"Rewrote links in {notebook_path.name}")
                return True

            return False

        except Exception as e:
            log.error(f"Error processing {notebook_path}: {e}")
            return False

    def _rewrite_links_in_text(
        self, text: str, site_url: str, notebook_dir: Path
    ) -> str:
        """
        Rewrite relative markdown links in text to absolute URLs.

        Args:
            text: The markdown text to process
            site_url: Base URL of the published site
            notebook_dir: Directory of the notebook relative to site root

        Returns:
            Text with rewritten links
        """
        # Pattern to match markdown links: [text](url)
        # We only want to rewrite relative links (starting with ../ or not http/https)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)

            # Skip absolute URLs (http://, https://, mailto:, etc.)
            if re.match(r'^[a-z]+://', link_url):
                return match.group(0)

            # Skip anchors
            if link_url.startswith('#'):
                return match.group(0)

            # Remove trailing slash if present
            link_url = link_url.rstrip('/')

            # Strip .md and .ipynb extensions for clean URLs
            # MkDocs creates directory-style URLs without extensions
            if link_url.endswith('.md') or link_url.endswith('.ipynb'):
                link_url = link_url.rsplit('.', 1)[0]

            # Convert relative link to absolute URL
            # Source notebooks use single ../ for editor navigation (from docs/section/)
            # But built notebooks are at site/section/notebook-name/ (extra directory level)
            # So we need to add an extra ../ to compensate
            import os.path

            # Start from the notebook's directory in the built site
            notebook_dir_str = str(notebook_dir).replace("\\", "/")

            # Add ../ to account for MkDocs creating an extra directory level
            # This transforms paths from source context to built context
            adjusted_link = '../' + link_url

            # Join and normalize the path
            combined_path = os.path.normpath(
                os.path.join(notebook_dir_str, adjusted_link)
            ).replace("\\", "/")

            # Build absolute URL from site root
            absolute_url = f"{site_url}/{combined_path}"

            return f"[{link_text}]({absolute_url})"

        return link_pattern.sub(replace_link, text)

    def _rewrite_html_links(self, html_path: Path, site_dir: Path) -> bool:
        """
        Rewrite relative links in HTML files to clean directory URLs.

        This fixes links that mkdocs-jupyter rendered incorrectly by:
        1. Stripping .md and .ipynb extensions
        2. Adjusting relative paths to account for MkDocs directory structure

        Args:
            html_path: Path to the HTML file
            site_dir: Path to the site output directory

        Returns:
            True if HTML was modified, False otherwise
        """
        try:
            # Read the HTML file
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Track if any changes were made
            modified = False

            # Pattern to match relative links with .md or .ipynb extensions
            # Matches: href="../path/file.md" or href="path/file.ipynb"
            # But not: href="http://..." or href="https://..." or GitHub edit links
            link_pattern = re.compile(
                r'href="((?!http://|https://|https://github\.com)[^"]*?)(\.md|\.ipynb)"'
            )

            def fix_link(match):
                nonlocal modified
                link_url = match.group(1)
                extension = match.group(2)
                full_match = match.group(0)

                # Skip GitHub edit links
                if 'github.com' in link_url or '/edit/' in link_url:
                    return full_match

                # Skip download button links (they need the .ipynb extension to download)
                # Look for the link in context to check if it's a download button
                # Download buttons have: title="Download Notebook" and class="md-content__button"
                start_pos = html_content.rfind('<a ', 0, match.start())
                end_pos = html_content.find('</a>', match.end())
                if start_pos != -1 and end_pos != -1:
                    link_tag = html_content[start_pos:end_pos + 4]
                    if 'Download Notebook' in link_tag or 'md-content__button' in link_tag:
                        return full_match

                # For links starting with ../
                if link_url.startswith('../'):
                    # Add an extra ../ to compensate for MkDocs directory structure
                    # ../explanation/file -> ../../explanation/file
                    fixed_url = '../' + link_url
                else:
                    # For same-directory links (no ../)
                    # file -> ../file (add ../ for sibling directory)
                    fixed_url = '../' + link_url

                modified = True
                return f'href="{fixed_url}"'

            html_content = link_pattern.sub(fix_link, html_content)

            # Write back if modified
            if modified:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                log.debug(f"Rewrote links in {html_path.name}")
                return True

            return False

        except Exception as e:
            log.error(f"Error processing {html_path}: {e}")
            return False


def get_plugin():
    """Return the plugin class (required by MkDocs)."""
    return NotebookLinkRewriterPlugin
