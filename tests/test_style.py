"""Tests for the layout, colour tokens, font, theme toggle and CSP. Standard library only."""

import hashlib
import re
import unittest

from util import ROOT, contrast, read

LIGHT = {
    "--bg": "#FBF4E4",
    "--ink": "#2B1D14",
    "--soft": "#5A4535",
    "--accent": "#A3401C",
    "--link": "#1E5546",
    "--edge": "#B99B76",
    "--control-edge": "#86664A",
}
DARK = {
    "--bg": "#1E1915",
    "--ink": "#F4EADB",
    "--soft": "#D3C3AC",
    "--accent": "#F2A65A",
    "--link": "#A8D5B0",
    "--edge": "#5E4E3F",
    "--control-edge": "#9A7F62",
}

CSP = (
    "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
    "font-src 'self'; frame-src https://www.youtube-nocookie.com; base-uri 'self'; "
    "form-action 'none'; object-src 'none'"
)

FONT_SHA256 = {
    "AtkinsonHyperlegible-Regular.woff2": "2df4ba17804bc7a36f123127966075d8427bff2df58d0d76820c1130bb1a4150",
    "AtkinsonHyperlegible-Bold.woff2": "da8fce41a04f8498fbf79076f92d304b12e70c76f71b143c5dcfb6536c93c075",
    "OFL.txt": "f32d22b3908fcad2c86a74000614ec22e6a7f66ea7e867e616026a27aebdc143",
}

NAV_LABELS = ["FadeBench", "Projects", "Lab Notes", "About", "Contact"]


def css_body(css, selector):
    """Declarations inside the first rule whose selector matches the regex `selector`."""
    m = re.search(selector + r"\s*\{([^}]*)\}", css)
    return m.group(1) if m else ""


def tokens(css, selector):
    return dict(re.findall(r"(--[a-z-]+):\s*(#[0-9A-Fa-f]{6})", css_body(css, selector)))


def forced_colors_inner(css):
    """Text between the forced-colors @media opening brace and its matching closing brace."""
    idx = css.find("@media (forced-colors: active)")
    if idx == -1:
        return ""
    start = css.index("{", idx) + 1
    depth = 1
    for pos in range(start, len(css)):
        if css[pos] == "{":
            depth += 1
        elif css[pos] == "}":
            depth -= 1
            if depth == 0:
                return css[start:pos]
    return css[start:]


def forced_colors_rules(css):
    """(selectors, body) pairs for each plain rule inside the forced-colors block."""
    pairs = []
    for m in re.finditer(r"([^{}]+)\{([^}]*)\}", forced_colors_inner(css)):
        selectors = [s.strip() for s in m.group(1).split(",") if s.strip()]
        pairs.append((selectors, m.group(2)))
    return pairs


def layout_and_include_files():
    files = list(ROOT.glob("_layouts/*.html")) + list(ROOT.glob("_includes/*.html"))
    return sorted(p.relative_to(ROOT).as_posix() for p in files)


def head_without_csp():
    return re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>', "", read("_includes/head.html"))


class TokenTests(unittest.TestCase):
    def setUp(self):
        self.css = read("assets/css/site.css")

    def test_tokens_light_and_dark(self):
        light = tokens(self.css, r":root")
        dark_media = tokens(self.css, r":root:not\(\[data-theme=\"light\"\]\)")
        dark_attr = tokens(self.css, r":root\[data-theme=\"dark\"\]")
        self.assertEqual(light, LIGHT)
        self.assertEqual(dark_media, DARK)
        self.assertEqual(dark_attr, DARK)
        self.assertLess(
            self.css.index("@media (prefers-color-scheme: dark)"),
            self.css.index(':root:not([data-theme="light"])'),
        )
        for name, t in (("light", LIGHT), ("dark", DARK)):
            with self.subTest(theme=name):
                self.assertGreaterEqual(contrast(t["--ink"], t["--bg"]), 7)
                for tok in ("--soft", "--link", "--accent"):
                    self.assertGreaterEqual(contrast(t[tok], t["--bg"]), 4.5, tok)
                self.assertGreaterEqual(contrast(t["--bg"], t["--accent"]), 4.5)

    def test_base_size_and_units(self):
        css = self.css
        self.assertRegex(css, r"html\s*\{[^}]*font-size:\s*112\.5%")
        self.assertIsNone(re.search(r"font-size\s*:[^;}]*px", css))
        self.assertRegex(css, r'font-family:\s*"Atkinson Hyperlegible",\s*system-ui,\s*sans-serif')
        self.assertRegex(css, r"line-height:\s*1\.55")
        self.assertIn("font-display: swap", css)

    def test_targets_and_focus(self):
        self.assertRegex(self.css, r"\.site-nav a\s*\{[^}]*min-height:\s*44px")
        self.assertRegex(self.css, r"(?m)^button\b[^{]*\{[^}]*min-height:\s*44px")
        self.assertRegex(self.css, r":focus-visible\s*\{[^}]*3px solid")

    def test_no_external_requests(self):
        for rel in ("assets/css/site.css", "assets/js/theme.js"):
            with self.subTest(file=rel):
                self.assertNotRegex(read(rel), r"https?://")
        self.assertNotRegex(head_without_csp(), r"https?://")
        self.assertNotIn("fonts.googleapis", self.css)
        self.assertRegex(self.css, r'src:\s*url\("\.\./fonts/AtkinsonHyperlegible-(Regular|Bold)\.woff2"\)')

    def test_viewport_and_no_fixed_widths(self):
        self.assertIn(
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            read("_includes/head.html"),
        )
        self.assertIsNone(re.search(r"(?<![-\w])width\s*:\s*\d+px", self.css))
        self.assertRegex(self.css, r"max-width:\s*42rem")
        self.assertIsNone(re.search(r"max-width\s*:\s*\d+px", self.css))

    def test_no_hardcoded_root_links(self):
        files = layout_and_include_files()
        self.assertTrue(files, "no layouts or includes found")
        for rel in files:
            with self.subTest(file=rel):
                self.assertEqual(re.findall(r'(?:href|src)="/(?!/)', read(rel)), [])

    def test_theme_works_without_js(self):
        self.assertRegex(read("_includes/header.html"), r'<button id="theme-toggle"[^>]*\bhidden\b')
        js = read("assets/js/theme.js")
        self.assertIn("btn.hidden = false", js)
        self.assertIn("prefers-color-scheme", self.css)
        for m in re.finditer(r"localStorage", js):
            self.assertIn("try", js[max(0, m.start() - 120):m.start()])

    def test_forced_colors_block(self):
        idx = self.css.find("@media (forced-colors: active)")
        self.assertNotEqual(idx, -1)
        block = self.css[idx:]
        self.assertIn("border", block)
        self.assertIn("outline", block)

    def test_forced_colors_edges_not_boxed(self):
        inner = forced_colors_inner(self.css)
        self.assertTrue(inner.strip(), "no forced-colors block found")
        rules = forced_colors_rules(self.css)
        self.assertTrue(rules, "no forced-colors rules found")
        self.assertNotIn(".site-name", inner)
        for selectors, body in rules:
            for sel in selectors:
                if sel in (".site-header", ".site-footer"):
                    with self.subTest(selector=sel):
                        self.assertNotIn("border: 2px solid", body)
                        self.assertNotRegex(body, r"(?<![-\w])border:")
        all_selectors = [s for selectors, _ in rules for s in selectors]
        self.assertIn(".site-header", all_selectors)
        self.assertIn(".site-footer", all_selectors)

    def test_control_edge_contrast(self):
        for name, t in (("light", LIGHT), ("dark", DARK)):
            with self.subTest(theme=name):
                self.assertGreaterEqual(contrast(t["--control-edge"], t["--bg"]), 3)
        self.assertRegex(self.css, r"\.site-nav a\s*\{[^}]*var\(--control-edge\)")
        self.assertRegex(self.css, r"button, \.button\s*\{[^}]*var\(--control-edge\)")
        self.assertRegex(self.css, r"\.plate\s*\{[^}]*var\(--control-edge\)")

    def test_skip_link_is_first_and_main_has_id(self):
        layout = read("_layouts/default.html")
        self.assertIn('<a class="skip-link" href="#main">', layout)
        self.assertLess(layout.index("skip-link"), layout.index("header.html"))
        self.assertIn('<main id="main">', layout)

    def test_header_nav_order_and_doors(self):
        header = read("_includes/header.html")
        labels = re.findall(r'<a href="[^"]*"(?:\{% if [^%]*%\} aria-current="page"\{% endif %\})?>([^<]+)</a>', header)
        self.assertEqual(labels, NAV_LABELS)
        # Paper and Code moved onto the FadeBench page (Becky's site outline, 2026-11-21).
        for url in ("/fadebench/", "/projects/", "/lab-notes/", "/about/", "/contact/"):
            with self.subTest(url=url):
                self.assertIn("{{ '" + url + "' | relative_url }}", header)

    def test_footer(self):
        footer = read("_includes/footer.html")
        self.assertIn("© Becky R. Northaven", footer)
        self.assertIn("{{ 'now' | date: '%Y' }}", footer)
        self.assertNotIn("Sequim Electronics", footer)


class HeadAndScriptTests(unittest.TestCase):
    def test_csp_meta_present_and_no_inline(self):
        head = read("_includes/head.html")
        self.assertIn(f'<meta http-equiv="Content-Security-Policy" content="{CSP}">', head)
        self.assertIn("{% seo %}", head)
        self.assertIn(
            "<script src=\"{{ '/assets/js/theme.js' | relative_url }}\" defer></script>",
            head,
        )
        for rel in layout_and_include_files():
            with self.subTest(file=rel):
                text = read(rel)
                self.assertEqual(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>", text), [])
                self.assertNotRegex(text, r"\sstyle\s*=")
                self.assertNotRegex(text, r"<style\b")

    def test_theme_js_validates_storage(self):
        js = read("assets/js/theme.js")
        self.assertRegex(js, r'v === "light" \|\| v === "dark" \? v : null')
        self.assertNotRegex(js, r"return localStorage\.getItem")

    def test_theme_js_is_small_and_safe(self):
        js = read("assets/js/theme.js")
        self.assertLessEqual(len(js.splitlines()), 25)
        for bad in ("innerHTML", "eval(", "document.write"):
            self.assertNotIn(bad, js)
        self.assertIn('setAttribute("data-theme"', js)
        self.assertIn('setAttribute("aria-pressed"', js)
        self.assertNotRegex(js, r'setAttribute\("(?!data-theme"|aria-pressed")')

    def test_font_files_pinned(self):
        for name, digest in FONT_SHA256.items():
            with self.subTest(file=name):
                path = ROOT / "assets" / "fonts" / name
                self.assertTrue(path.exists(), f"{name} missing")
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
