"""Live checks against the published site. Standard library only.

These tests are opt-in. They are skipped unless RUN_LIVE=1 is set, because the
site is not published yet. They make plain GET requests to SITE_BASE (default:
the GitHub Pages address) and read the returned HTML.

Run them after Pages has finished building:

    RUN_LIVE=1 python -I -m unittest discover -s tests -p "test_live.py" -v

Set SITE_BASE to test another address, for example a local preview.
"""

import html.parser
import os
import pathlib
import re
import unittest
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("SITE_BASE", "https://feedtheraccoon.com").rstrip("/")
TIMEOUT = 20
USER_AGENT = "feedtheraccoon-check"

PAGES = ["/", "/about/", "/contact/", "/fadebench/"]
ASSETS = [
    "/assets/css/site.css",
    "/assets/fonts/AtkinsonHyperlegible-Regular.woff2",
    "/assets/fonts/AtkinsonHyperlegible-Bold.woff2",
]
MISSING_PATH = "/nope-not-a-page"

# Hosts a page may link to with <a href>, and the path prefix allowed on each.
# "/" means any path. Everything else must be same-origin as BASE.
ALLOWED_LINK_HOSTS = {
    "doi.org": "/",
    "github.com": "/",
    "orcid.org": "/",
    "www.youtube.com": "/watch",
    "sequimelectronics.com": "/",
}

ROOT = pathlib.Path(__file__).resolve().parent.parent


def fetch(url):
    """Return (status, body bytes, final URL). HTTP error statuses are returned, not raised."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(), resp.geturl()
    except urllib.error.HTTPError as err:
        return err.code, err.read(), err.geturl()


class RefCollector(html.parser.HTMLParser):
    """Collects (tag, attribute, value) for every src and href on the page."""

    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in ("src", "href"):
                self.refs.append((tag, name, value.strip()))


def config_contact_email():
    """Return the contact_email value from _config.yml (the one mailto: address allowed on the site)."""
    text = (ROOT / "_config.yml").read_text(encoding="utf-8")
    m = re.search(r'^contact_email:\s*"([^"]+)"\s*$', text, re.MULTILINE)
    if not m:
        raise RuntimeError("contact_email line not found in _config.yml")
    return m.group(1)


def same_origin(absolute):
    base = urllib.parse.urlsplit(BASE)
    other = urllib.parse.urlsplit(absolute)
    return other.scheme == base.scheme and other.netloc.lower() == base.netloc.lower()


def allowed_outbound_link(absolute):
    parts = urllib.parse.urlsplit(absolute)
    if parts.scheme != "https":
        return False
    prefix = ALLOWED_LINK_HOSTS.get((parts.hostname or "").lower())
    return prefix is not None and (parts.path or "/").startswith(prefix)


@unittest.skipUnless(os.environ.get("RUN_LIVE") == "1", "live tests need RUN_LIVE=1")
class LiveSiteTests(unittest.TestCase):
    def page_body(self, path):
        status, body, _ = fetch(BASE + path)
        self.assertEqual(status, 200, f"{path} returned {status}")
        return body.decode("utf-8", "replace")

    def test_pages_ok(self):
        for path in PAGES:
            with self.subTest(page=path):
                status, _, _ = fetch(BASE + path)
                self.assertEqual(status, 200)

    def test_404_is_ours(self):
        not_found_text = "This page is not here."
        source = (ROOT / "404.md").read_text(encoding="utf-8")
        self.assertIn(not_found_text, source, "404.md no longer has the expected sentence")
        status, body, _ = fetch(BASE + MISSING_PATH)
        self.assertEqual(status, 404)
        self.assertIn(not_found_text, body.decode("utf-8", "replace"))

    def test_no_third_party_resources(self):
        contact_mailto = "mailto:" + config_contact_email()
        failures = []
        for path in PAGES:
            page_url = BASE + path
            collector = RefCollector()
            collector.feed(self.page_body(path))
            self.assertTrue(collector.refs, f"{path}: no src/href references found, check the page was read")
            for tag, attr, value in collector.refs:
                absolute = urllib.parse.urljoin(page_url, value)
                if same_origin(absolute):
                    continue
                if tag == "a" and attr == "href" and allowed_outbound_link(absolute):
                    continue
                # The one mailto: allowed: the contact address from _config.yml, on <a href> only.
                if tag == "a" and attr == "href" and value.lower() == contact_mailto.lower():
                    continue
                failures.append(f"{path}: <{tag} {attr}={value!r}> -> {absolute}")
        self.assertEqual(failures, [], "third-party or disallowed references found")

    def test_no_static_iframe(self):
        for path in PAGES:
            with self.subTest(page=path):
                self.assertNotIn("<iframe", self.page_body(path).lower())

    def test_assets_ok(self):
        for path in ASSETS:
            with self.subTest(asset=path):
                status, _, _ = fetch(BASE + path)
                self.assertEqual(status, 200)


if __name__ == "__main__":
    unittest.main()
