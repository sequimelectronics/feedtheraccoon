"""Tests for the launch pages and project data. Standard library only."""

import hashlib
import json
import os
import pathlib
import re
import unittest

from util import ROOT, front_matter, read

EXCLUDED_DIRS = {"tests", "docs", ".superpowers", ".git", "_site", ".jekyll-cache", "__pycache__"}
BINARY_EXTS = (".woff2", ".woff", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf")

PAPER_DOI = "https://doi.org/10.5281/zenodo.23846266"
CODE_DOI = "https://doi.org/10.5281/zenodo.23848638"
FADEBENCH_REPO = "https://github.com/sequimelectronics/fadebench"
AI_BEACH_REPO = "https://github.com/sequimelectronics/AI-Beach"
DEBATE_HALL_REPO = "https://github.com/sequimelectronics/DebateHall"
ORCID = "https://orcid.org/0009-0007-6573-6544"

# sha256 digests of the three private words, so the words themselves never appear in the repo.
FORBIDDEN_SHA256 = {
    "6c296fde55b852788be0818c74fc20be7554d5fede6bbd3d421965755dd3d0c1",
    "52af9a5514e2ad22f1bc15f8568e9615746e36cddc05d644f4da7121044f62ed",
    "8a22313f71cd923a8135ff75dc556269bf89f99d426a787904512e01d5751d95",
}

LAUNCH_PAGES = {
    "index.md": ("forest", "/"),
    "about.md": ("cave", "/about/"),
    "contact.md": ("foxrescue", "/contact/"),
    "fadebench.md": ("prairie", "/fadebench/"),
}

BANNED_WORDS = [
    "delve", "genuinely", "robust", "seamless", "leverage", "crucial",
    "tapestry", "nuanced", "holistic", "ensure", "empower", "journey",
    "unlock", "truly", "honestly",
]


def site_files():
    """Every file in the site source: everything except tests, docs and build output."""
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            if name.endswith(".pyc") or name.lower().endswith(BINARY_EXTS):
                continue
            full = pathlib.Path(dirpath) / name
            found.append(full.relative_to(ROOT).as_posix())
    return sorted(found)


def projects():
    return json.loads(read("_data/projects.json"))


class FrontMatterTests(unittest.TestCase):
    def test_launch_pages_exist_with_front_matter(self):
        for page, (place, _permalink) in LAUNCH_PAGES.items():
            with self.subTest(page=page):
                fm = front_matter(page)
                for key in ("title", "description", "place", "layout", "draft_copy"):
                    self.assertIn(key, fm, f"{page} is missing {key}")
                self.assertEqual(fm["place"], place)
                self.assertEqual(fm["layout"], "default")
                self.assertEqual(fm["draft_copy"], "true")

    def test_front_matter_parses(self):
        fm = front_matter("index.md")
        self.assertTrue(fm.get("title"))
        self.assertEqual(fm.get("place"), "forest")

    def test_permalinks(self):
        for page, (_place, permalink) in LAUNCH_PAGES.items():
            with self.subTest(page=page):
                self.assertEqual(front_matter(page).get("permalink", "/" if page == "index.md" else None), permalink)

    def test_404_page(self):
        fm = front_matter("404.md")
        self.assertEqual(fm.get("permalink"), "/404.html")
        self.assertEqual(fm.get("layout"), "default")
        self.assertEqual(fm.get("draft_copy"), "true")
        self.assertEqual(fm.get("place"), "forest")
        self.assertIn("{{ '/' | relative_url }}", read("404.md"))


class ProjectDataTests(unittest.TestCase):
    def test_projects_data(self):
        data = projects()
        self.assertEqual(
            [p["id"] for p in data],
            ["fadebench", "ai-beach", "debate-hall", "mom", "moments-to-speak", "judgement-call"],
        )
        by_id = {p["id"]: p for p in data}
        self.assertEqual(
            {pid: p["status"] for pid, p in by_id.items()},
            {
                "fadebench": "full",
                "ai-beach": "full",
                "debate-hall": "full",
                "mom": "coming_soon",
                "moments-to-speak": "coming_soon",
                "judgement-call": "coming_soon",
            },
        )

    def test_project_fields(self):
        for p in projects():
            with self.subTest(project=p.get("id")):
                self.assertEqual(set(p.keys()), {"id", "name", "status", "place", "story", "links"})
                self.assertTrue(p["name"].strip())
                self.assertTrue(p["story"].strip())
                for link in p["links"]:
                    self.assertEqual(set(link.keys()), {"label", "url"})

    def test_coming_soon_has_no_links(self):
        for p in projects():
            if p["status"] == "coming_soon":
                with self.subTest(project=p["id"]):
                    self.assertEqual(p["links"], [])

    def test_fadebench_links(self):
        urls = [link["url"] for link in projects()[0]["links"]]
        self.assertIn(PAPER_DOI, urls)
        self.assertIn(CODE_DOI, urls)
        self.assertIn(FADEBENCH_REPO, urls)

    def test_project_repo_links(self):
        by_id = {p["id"]: p for p in projects()}
        self.assertIn(DEBATE_HALL_REPO, [l["url"] for l in by_id["debate-hall"]["links"]])
        self.assertIn(AI_BEACH_REPO, [l["url"] for l in by_id["ai-beach"]["links"]])


class CopyTests(unittest.TestCase):
    def test_forbidden_words(self):
        # The private words are stored only as sha256 digests, so they never appear in the repo.
        for rel in site_files():
            tokens = set(re.findall(r"[a-z]+", read(rel).lower()))
            with self.subTest(file=rel):
                hits = [t for t in tokens if hashlib.sha256(t.encode()).hexdigest() in FORBIDDEN_SHA256]
                self.assertEqual(hits, [], "a private name is in the site source")

    def test_no_raw_url_link_text(self):
        for rel in LAUNCH_PAGES:
            with self.subTest(file=rel):
                bad = re.findall(r"\[(?:https?:|doi\.org)[^\]]*\]\(", read(rel))
                self.assertEqual(bad, [])

    def test_long_words_wrap(self):
        css = read("assets/css/site.css")
        for selector in (r"main", r"\.site-footer", r"\.plate figcaption"):
            with self.subTest(selector=selector):
                self.assertRegex(css, selector + r"\s*\{[^}]*overflow-wrap:\s*anywhere")

    def test_draft_pages_are_noindex(self):
        head = read("_includes/head.html")
        self.assertRegex(head, r"page\.draft_copy[^%]*%\}\s*<meta name=\"robots\" content=\"noindex\">")

    def test_nav_marks_current_page(self):
        header = read("_includes/header.html")
        for url in ("/fadebench/", "/about/", "/contact/"):
            with self.subTest(url=url):
                self.assertIn("page.url == '" + url + "'", header)
        self.assertIn('aria-current="page"', header)

    def test_bio_day_job_only_on_about(self):
        self.assertIn("Sequim Electronics", read("about.md"))
        for rel in site_files():
            if rel == "about.md":
                continue
            with self.subTest(file=rel):
                self.assertNotIn("Sequim Electronics", read(rel))

    def test_raccoon_direction(self):
        for rel in site_files():
            with self.subTest(file=rel):
                self.assertIsNone(
                    re.search(
                        r"end up feeding the raccoon|started feeding|toward feeding|towards feeding",
                        read(rel),
                        re.I,
                    )
                )

    def test_copy_style(self):
        targets = list(LAUNCH_PAGES) + ["404.md", "_data/projects.json"]
        for rel in targets:
            text = read(rel)
            with self.subTest(file=rel):
                self.assertNotIn("—", text, "em dash")
                self.assertNotIn(";", text, "semicolon")
                for word in BANNED_WORDS:
                    self.assertIsNone(re.search(rf"\b{word}\b", text, re.I), word)

    def test_internal_links_use_relative_url(self):
        for rel in site_files():
            if not rel.endswith((".md", ".html")):
                continue
            with self.subTest(file=rel):
                bare = re.findall(r'(\]\(|href="|src=")/(?!/)', read(rel))
                self.assertEqual(bare, [])


class IndexTests(unittest.TestCase):
    def test_hook_options_comment_after_front_matter(self):
        text = read("index.md")
        self.assertRegex(
            text,
            r"<!-- HOOK OPTIONS for Becky:.*?1\).*?2\).*?3\).*?-->",
        )

    def test_index_content(self):
        text = read("index.md")
        self.assertIn("Film coming soon", text)
        self.assertIn("{{ '/fadebench/' | relative_url }}", text)
        self.assertIn(PAPER_DOI, text)


class FadeBenchPageTests(unittest.TestCase):
    def test_headline_numbers_verbatim(self):
        text = read("fadebench.md")
        for phrase in (
            "15 times in 100",
            "fewer than 2 times in 100",
            "13.2 points",
            "2.6 to 25.9",
            "43 in 100",
            "2 in 99",
            "38 scenario items",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_limits_and_links(self):
        text = read("fadebench.md")
        self.assertIn("frontier", text)
        self.assertIn(PAPER_DOI, text)
        self.assertIn(CODE_DOI, text)
        self.assertIn(FADEBENCH_REPO, text)


class AboutTests(unittest.TestCase):
    def test_projects_section_and_cards(self):
        text = read("about.md")
        self.assertIn("## Projects {#projects}", text)
        self.assertIn("site.data.projects", text)
        self.assertIn("project-card.html", text)

    def test_bio_links(self):
        self.assertIn("https://sequimelectronics.com", read("about.md"))


class ContactTests(unittest.TestCase):
    def test_contact_email_logic_present(self):
        text = read("contact.md")
        self.assertIn("{% if site.contact_email %}", text)
        self.assertIn("{{ site.contact_email }}", text)
        self.assertIn("Address coming soon.", text)

    def test_contact_no_raw_email_in_markup(self):
        self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", read("contact.md")))

    def test_contact_links(self):
        text = read("contact.md")
        self.assertIn(ORCID, text)
        self.assertIn(FADEBENCH_REPO, text)


class ProjectCardTests(unittest.TestCase):
    def test_card_include(self):
        text = read("_includes/project-card.html")
        self.assertIn('project.status == "full"', text)
        self.assertIn("Coming soon", text)
        self.assertIn("project.story", text)
        self.assertIn("project.links", text)


class GitignoreTests(unittest.TestCase):
    def test_pycache_ignored(self):
        lines = [l.strip() for l in read(".gitignore").splitlines()]
        self.assertIn("__pycache__/", lines)
        self.assertIn("*.pyc", lines)


if __name__ == "__main__":
    unittest.main()
