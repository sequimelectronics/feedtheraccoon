"""Tests for the click-to-load video include. Standard library only."""

import re
import unittest

from util import read

INCLUDE = "_includes/youtube.html"
SCRIPT = "assets/js/video.js"


class VideoIncludeTests(unittest.TestCase):
    def test_no_static_iframe(self):
        self.assertNotIn("<iframe", read(INCLUDE))

    def test_nocookie_only(self):
        js = read(SCRIPT)
        self.assertIn("youtube-nocookie.com", js)
        self.assertNotIn("www.youtube.com/embed", js)

    def test_video_has_noscript_link(self):
        text = read(INCLUDE)
        self.assertIn('<a href="https://www.youtube.com/watch?v={{ include.id | escape }}">', text)
        self.assertIn('data-video-title="{{ include.title | escape }}"', text)
        self.assertIn("<noscript>", text)

    def test_video_js_safe(self):
        js = read(SCRIPT)
        for banned in ("innerHTML", "eval(", "document.write"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, js)
        self.assertIn("createElement", js)
        self.assertIn("setAttribute", js)
        self.assertIn("[A-Za-z0-9_-]{11}", js)

    def test_video_js_binds_once(self):
        js = read(SCRIPT)
        guard = js.find("window.__ftrVideoBound")
        self.assertNotEqual(guard, -1, "video.js needs a bind-once guard")
        self.assertLess(guard, js.find("addEventListener"))

    def test_play_label_hidden_from_screen_readers(self):
        self.assertIn('<span class="video-play" aria-hidden="true">Play</span>', read(INCLUDE))

    def test_include_no_inline_script_or_style(self):
        text = read(INCLUDE)
        self.assertEqual(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>", text), [])
        self.assertNotIn("<style", text)
        self.assertNotIn("style=", text)


if __name__ == "__main__":
    unittest.main()
