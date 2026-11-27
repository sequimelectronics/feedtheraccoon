"""Tests for the journal plates: placeholder art, credits data, the include and the paper background. Standard library only."""

import json
import re
import unittest

from util import ROOT, contrast, read
from test_pages import LAUNCH_PAGES
from test_style import css_body

PLACES = ("forest", "prairie", "cave", "foxrescue")
PLACEHOLDER_CREDIT = ""  # Becky 2026-11-27: no "Placeholder sketch" caption; blank until real art
PAPER = "#FBF4E4"


def credits():
    return json.loads(read("_data/credits.json"))


class PlateTests(unittest.TestCase):
    def test_every_place_has_art_and_credit(self):
        data = credits()
        self.assertEqual(set(data), set(PLACES))
        for place in {page[0] for page in LAUNCH_PAGES.values()}:
            self.assertIn(place, data, f"launch page place {place} has no credit entry")
        for place, entry in data.items():
            with self.subTest(place=place):
                self.assertEqual(set(entry), {"file", "alt", "credit"})
                self.assertEqual(entry["file"], f"/assets/img/journal/{place}.svg")
                self.assertTrue((ROOT / entry["file"].lstrip("/")).is_file(), "art file missing")
                self.assertEqual(entry["credit"], PLACEHOLDER_CREDIT)

    def test_alt_text_nonempty(self):
        for place, entry in credits().items():
            with self.subTest(place=place):
                self.assertGreaterEqual(len(entry["alt"].strip()), 20)
                self.assertTrue(entry["alt"].startswith("Ink sketch of"))

    def test_journal_images_sit_on_paper(self):
        css = read("assets/css/site.css")
        plate = css_body(css, r"\.plate")
        self.assertRegex(plate, r"background:\s*#FBF4E4")
        self.assertRegex(plate, r"border:\s*2px solid var\(--control-edge\)")
        self.assertRegex(plate, r"border-radius:\s*0\.5rem")
        for selector in (r":root:not\(\[data-theme=\"light\"\]\)", r":root\[data-theme=\"dark\"\]"):
            block = re.search(selector + r"\s*\{([^}]*)\}", css)
            self.assertIsNotNone(block)
        self.assertNotRegex(css, r"@media \(prefers-color-scheme: dark\)\s*\{[^@]*\.plate\s*\{")
        figcaption = css_body(css, r"\.plate figcaption")
        colour = re.search(r"color:\s*(#[0-9A-Fa-f]{6})", figcaption)
        self.assertIsNotNone(colour, "figcaption colour must be a fixed value, not a theme token")
        self.assertGreaterEqual(contrast(colour.group(1), PAPER), 4.5)

    def test_plate_include_and_layout(self):
        include = read("_includes/journal-plate.html")
        self.assertIn("{% assign plate = site.data.credits[include.place] %}", include)
        self.assertIn('<figure class="plate">', include)
        self.assertIn('<img src="{{ plate.file | relative_url }}" alt="{{ plate.alt }}" width="640" height="360">', include)
        self.assertIn('{% if plate.credit != "" %}<figcaption>{{ plate.credit }}</figcaption>{% endif %}', include)
        self.assertIn("{% if plate %}", include)
        layout = read("_layouts/default.html")
        self.assertIn("{% if page.place %}{% include journal-plate.html place=page.place %}{% endif %}", layout)
        self.assertLess(layout.index("journal-plate"), layout.index("{{ content }}"))
        self.assertGreater(layout.index("journal-plate"), layout.index("<main"))

    def test_svgs_are_plain_placeholders(self):
        for place in PLACES:
            with self.subTest(place=place):
                text = read(f"assets/img/journal/{place}.svg")
                self.assertLess(len(text.encode("utf-8")), 4096)
                self.assertIn('viewBox="0 0 640 360"', text)
                self.assertIn('stroke="#2B1D14"', text)
                self.assertIn(f">{place.replace('foxrescue', 'fox rescue')}</text>", text)
                without_ns = text.replace('xmlns="http://www.w3.org/2000/svg"', "")
                self.assertNotRegex(without_ns, r"https?://")
                for bad in ("<script", "<style", "href", "src=", "url(", "<foreignObject", "<image"):
                    self.assertNotIn(bad, text)
                self.assertNotRegex(text, r"\sstyle\s*=")


if __name__ == "__main__":
    unittest.main()
