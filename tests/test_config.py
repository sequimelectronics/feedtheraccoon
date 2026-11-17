import re
import unittest

from util import ROOT, contrast, read


def top_level_config():
    values = {}
    plugins = None
    for line in read("_config.yml").splitlines():
        if not line or line.startswith((" ", "\t", "#")):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        if key == "plugins":
            inner = raw.strip("[]")
            plugins = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
        else:
            values[key] = raw.strip("\"'")
    return values, plugins


class ConfigTests(unittest.TestCase):
    def test_config_values(self):
        values, _ = top_level_config()
        self.assertEqual(values.get("title"), "Feed the Raccoon")
        self.assertEqual(values.get("author"), "Becky R. Northaven")
        self.assertEqual(values.get("url"), "https://sequimelectronics.github.io")
        self.assertEqual(values.get("baseurl"), "/feedtheraccoon")

    def test_contact_email(self):
        values, _ = top_level_config()
        self.assertEqual(values.get("contact_email"), "bnorthaven@feedtheraccoon.com")

    def test_no_remote_theme_or_unknown_plugins(self):
        values, plugins = top_level_config()
        self.assertNotIn("remote_theme", values)
        self.assertNotIn("theme", values)
        self.assertIsNotNone(plugins, "plugins list missing from _config.yml")
        self.assertTrue(
            set(plugins) <= {"jekyll-seo-tag", "jekyll-sitemap"},
            f"unexpected plugins: {plugins}",
        )

    def test_contrast_helper(self):
        self.assertEqual(round(contrast("#000000", "#FFFFFF"), 1), 21.0)
        self.assertGreaterEqual(contrast("#2B1D14", "#FBF4E4"), 7)


if __name__ == "__main__":
    unittest.main()
