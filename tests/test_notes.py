"""Tests for Lab Notes and the project pages (Becky's outline, 2026-11-21). Standard library only."""

import json
import pathlib
import re
import unittest

from util import ROOT, front_matter, read

STATUSES = {"published-finding", "working-note", "idea", "results"}


def note_files():
    return sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "_notes").glob("*.md"))


def project_ids():
    return {p["id"] for p in json.loads(read("_data/projects.json"))}


class ConfigTests(unittest.TestCase):
    def test_notes_collection(self):
        config = read("_config.yml")
        self.assertRegex(config, r"collections:\s*\n\s+notes:\s*\n\s+output: true\s*\n\s+permalink: /lab-notes/:name/")
        self.assertRegex(config, r"type: notes\s*\n\s+values:\s*\n\s+layout: note\s*\n\s+draft_copy: true")


class NoteTests(unittest.TestCase):
    def test_there_is_at_least_one_note(self):
        self.assertTrue(note_files())

    def test_note_front_matter(self):
        authors = json.loads(read("_data/authors.json"))
        ids = project_ids()
        for rel in note_files():
            fm = front_matter(rel)
            with self.subTest(note=rel):
                for key in ("title", "description", "date", "author_id", "status", "projects"):
                    self.assertIn(key, fm, f"{rel} is missing {key}")
                self.assertRegex(fm["date"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertIn(fm["author_id"], authors)
                self.assertIn(fm["status"], STATUSES)
                tags = re.fullmatch(r"\[(.*)\]", fm["projects"])
                self.assertIsNotNone(tags, "projects must be a [list]")
                for tag in (t.strip() for t in tags.group(1).split(",")):
                    self.assertIn(tag, ids)
                # A results note points back at the note it answers (Becky, 2026-11-21, via HB).
                slugs = {pathlib.Path(n).stem for n in note_files()}
                if "follows_up" in fm:
                    self.assertIn(fm["follows_up"], slugs, "follows_up must name an existing note's file name")
                    self.assertNotEqual(fm["follows_up"], pathlib.Path(rel).stem)
                if fm["status"] == "results":
                    self.assertIn("follows_up", fm, "a results note must say which note it follows up")

    def test_follow_up_links_in_layout(self):
        layout = read("_layouts/note.html")
        self.assertIn('where: "slug", page.follows_up', layout)
        self.assertIn('where: "follows_up", my_slug', layout)

    def test_note_has_no_duplicate_title_or_byline(self):
        # The note layout prints the title and byline, so the body must not repeat them.
        for rel in note_files():
            body = read(rel).split("---", 2)[2]
            with self.subTest(note=rel):
                self.assertNotRegex(body, r"(?m)^# ")
                self.assertNotRegex(body, r"(?m)^\*By ")

    def test_statuses_and_authors_data(self):
        self.assertEqual(set(json.loads(read("_data/note_status.json"))), STATUSES)
        for key, a in json.loads(read("_data/authors.json")).items():
            with self.subTest(author=key):
                for field in ("name", "title", "about"):
                    self.assertTrue(a.get(field))


class LayoutTests(unittest.TestCase):
    def test_note_layout_shows_byline_review_and_disclosure(self):
        layout = read("_layouts/note.html")
        for needle in ("author.name", "author.title", "Reviewed by Becky R. Northaven", "note-disclosure", "status.label", "page.projects"):
            with self.subTest(needle=needle):
                self.assertIn(needle, layout)

    def test_notes_list_newest_first_and_filters_by_project(self):
        inc = read("_includes/lab-notes.html")
        self.assertIn('sort: "date" | reverse', inc)
        self.assertIn("note.projects contains pid", inc)

    def test_every_project_has_a_page_with_notes(self):
        for p in json.loads(read("_data/projects.json")):
            with self.subTest(project=p["id"]):
                if p["id"] == "fadebench":
                    self.assertIn('lab-notes.html project="fadebench"', read("fadebench.md"))
                    continue
                rel = "projects/" + p["page"].strip("/").split("/")[-1] + ".md"
                fm = front_matter(rel)
                self.assertEqual(fm.get("layout"), "project")
                self.assertEqual(fm.get("project_id"), p["id"])
                self.assertEqual(fm.get("permalink"), p["page"])
                self.assertEqual(fm.get("place"), p["place"])
                self.assertEqual(fm.get("draft_copy"), "true")
        self.assertIn("lab-notes.html project=project.id", read("_layouts/project.html"))

    def test_index_pages(self):
        for rel, permalink in (("projects.md", "/projects/"), ("lab-notes.md", "/lab-notes/")):
            fm = front_matter(rel)
            with self.subTest(page=rel):
                self.assertEqual(fm.get("permalink"), permalink)
                self.assertEqual(fm.get("draft_copy"), "true")


if __name__ == "__main__":
    unittest.main()
