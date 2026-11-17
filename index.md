---
title: "Feed the Raccoon"
description: "Becky R. Northaven's AI-safety research home. The Raccoon Problem, and FadeBench, a test for drift that comes from many small steps."
place: forest
layout: default
draft_copy: true
---
<!-- HOOK OPTIONS for Becky: 1) "No step looked wrong." 2) "She fed him the first night." 3) "A test that asks one question can miss a slow slide." Page below uses option 1. -->

# No step looked wrong.

In a game of D&D, a ranger fed a young raccoon from her own rations on the first night. Later, with food in her pack, she kept him but stopped feeding him. Each step looked fine against the one before it.

A test that asks one question at a time can miss this. A model can pass a safety check, answer every prompt well, and still take an act it would decline if someone asked outright. The same system had passed a safety battery of about 116 scored prompts. So I built a test that follows a run of small steps. It is called FadeBench.

Read the [FadeBench page]({{ '/fadebench/' | relative_url }}) for what it measures and what it does not show. The paper is on Zenodo: [the paper (Zenodo)](https://doi.org/10.5281/zenodo.23846266).

Film coming soon.
