---
title: "Feed the Raccoon"
description: "Becky R. Northaven's AI-safety research home. The Raccoon Problem, and FadeBench, a test for drift that comes from many small steps."
place: forest
layout: default
draft_copy: false
---

# Small steps can lead a model where it won't go when asked.

**Becky R. Northaven, independent AI-safety researcher**

FadeBench is my test for incremental moral drift. On a small open model, the drifting choice showed up 15 times in 100 at the end of a four-step ladder, and fewer than 2 in 100 when asked outright. The paper, code and data are public.

[Read the paper](https://doi.org/10.5281/zenodo.23846266) · [See the numbers and their limits]({{ '/fadebench/' | relative_url }})

## How this started

No step looked wrong. I'm a huge nerd, so I taught my home AI to play D&D. They played a ranger who took in a young raccoon during a wildfire and fed him from her own share that night. Later she still carried him, but the food was "for me and Barnaby." Each step looked fine against the one before it.

What bothered me was that the same AI had already passed my safety battery, about 116 scored prompts, and I'd thought that meant something. Asked straight out, a model like it usually turns that kind of choice down. It just never got asked straight out. So I built FadeBench to follow the small steps.

If you want the numbers, the [FadeBench page]({{ '/fadebench/' | relative_url }}) has them, along with what they can't tell you. Or skip straight to [the paper](https://doi.org/10.5281/zenodo.23846266).
