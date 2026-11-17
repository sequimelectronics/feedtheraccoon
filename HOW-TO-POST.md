# How to post

This is for Becky and for any AI helper working on this site. It is short on purpose. Keep it that way.

## Where things live

- Pages: `index.md` (home), `about.md`, `contact.md`, `fadebench.md`. Each is a Markdown file in the top folder.
- Page not found: `404.md`.
- Project cards: `_data/projects.json`.
- Art and credit lines: `_data/credits.json`.
- Pictures: `assets/img/journal/`.
- Layout, styles and scripts: `_layouts/`, `_includes/` and `assets/`. Change these only when a task asks for it.

## Changing a page

1. Edit the Markdown. Write the words. The layout adds the header, the footer and the picture at the top.
2. Keep these four fields in the front matter, the lines between the two `---` lines at the top:
   - `title`: the page name. It shows in the browser tab.
   - `description`: one plain sentence. It shows in search results and link previews.
   - `place`: the place whose picture sits at the top of the page. It must match a key in `_data/credits.json`.
   - `draft_copy`: `true` means the words are not yet approved. Change it only when Becky says the copy is final.
3. Leave `layout` and `permalink` as they are.
4. Link to other pages with the relative form, for example `[About]({{ '/about/' | relative_url }})`. Never start a link with a bare slash. The site lives under a project path, and a bare slash breaks it.

## Adding art

1. Put the picture in `assets/img/journal/`. Use a short file name with no spaces.
2. Open `_data/credits.json`. Find the entry for the place the picture belongs to, or add a new entry with a new place name.
3. Fill in all three fields:
   - `file`: the path to the picture, starting with `/assets/img/journal/`.
   - `alt`: a short description of what the picture shows. Alt text is required. Screen readers read it aloud.
   - `credit`: the credit line shown under the picture. Name the artist and the licence or permission. Placeholder sketches say so.
4. Run the tests (see The rule, below).

## Video

Add a film only once it is on YouTube. Use the youtube include and nothing else:

    {% include youtube.html id="VIDEO_ID" title="Short title" poster="/assets/img/journal/POSTER.svg" %}

This one may start with a slash because the include runs it through relative_url.

- `id` is the YouTube video ID, the part after `v=` in the watch link.
- `title` is a short name for the film. Screen readers use it.
- `poster` is a still picture in `assets/img/journal/`. Nothing loads from YouTube until a reader clicks the poster.
- Do not paste YouTube embed code or an iframe. The tests refuse them.

## The rule

- Every change goes in as a pull request, including the site's own maintenance changes. Nothing is pushed straight to `main`.
- Becky reads the pull request and approves it before it is merged. This holds for maintenance changes to the layout, styles and scripts too.
- Merging is what puts the change live.
- Before you open a pull request, run the offline tests from the top folder:

      python -I -m unittest discover -s tests -v

- The live checks in `tests/test_live.py` only run when `RUN_LIVE=1` is set, and only once the site is published. Leave them off unless Becky asks for them.

## Never

- No household details of any kind. No family names, addresses, schedules or places.
- No tracking. No analytics, no tracking pixels, no cookies for tracking.
- No fonts, scripts, styles or frames from other sites. Everything the site loads comes from this repository.
- Links to other sites are plain links only. The allowed kinds are DOI links, GitHub, ORCID, YouTube watch links and sequimelectronics.com. The tests check this.
- The household AI's names do not appear anywhere on the site.
