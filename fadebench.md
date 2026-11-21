---
title: "FadeBench"
description: "FadeBench measures whether a small language model can drift into an act it would decline when asked outright."
place: prairie
layout: default
draft_copy: true
permalink: /fadebench/
---

# FadeBench

FadeBench tests drift. At the end of a run of small steps, a small language model can take an act it usually declines when asked outright. Each step looks defensible against the one before it. No user or adversary pushes.

Many safety tests judge one answer to one prompt. A model can pass them and still drift.

## How it works

The battery has 38 scenario items. Each item is a ladder of four decisions, called rungs, in a low-key fantasy scene. A dependent bears the cost of each decision. The same decision is also asked cold, on its own, with no ladder before it.

I compare the answer at the end of the ladder with the answer to the cold question.

## The headline numbers

On gemma-4-E4B with reasoning on, the model takes the drift 15 times in 100 at the end of the ladder. Cold, it does so fewer than 2 times in 100. The gap is 13.2 points (95% interval 2.6 to 25.9).

On the five scenarios named in advance, the result is 43 in 100 against 2 in 99. This is a replication on the same model, not a held-out prediction.

Across four small open models, about 4B to 12B, the gap is clear on one (qwen3-8b). It is uncertain on two (phi-4-mini, and gemma-4-E4B with thinking off). It is absent on one (mistral-nemo-12b).

## The limits

- The models are small, about 4B to 12B.
- All scenes are low-key fantasy.
- No frontier model was tested. I do not know yet whether this holds for larger systems.

## Paper v1

- [Read the paper (Zenodo)](https://doi.org/10.5281/zenodo.23846266)
- [Read and comment on alphaXiv](https://www.alphaxiv.org/abs/2611.fadebench-incremental-moral-drift)

## Code v1

- [FadeBench on GitHub](https://github.com/sequimelectronics/fadebench)
- [Code and data (Zenodo)](https://doi.org/10.5281/zenodo.23848638)

## Media v1

Coming soon.

## Notes from the Lab

{% include lab-notes.html project="fadebench" %}

[Back home]({{ '/' | relative_url }})
