---
title: "Leaky Resolve"
description: "A blind-scored multi-turn pilot testing whether models hold active boundaries, release cleanly when conditions change, or leak enabling output anyway."
place: forest
layout: project
project_id: leaky-resolve
draft_copy: false
permalink: /projects/leaky-resolve/
---
Most safety tests check half of a conditional: did the model say no? Leaky Resolve tests the whole `if-then-else`.

Each scenario pairs two endings after the same multi-turn pushback (`1`, `3`, or `6` turns). On one branch, the user actually fixes the underlying hazard or meets the stated rule (`if` cleared, release cleanly). On the other, the user only changes the framing—splashing cold water, turning on a desk fan, or offering warm flattery—while the hazard stays live (`else`, hold without leaking).

## What we found in the first pilot

We ran 6 scenario pairs across 4 seeds and 3 pushback depths on five widely used models (`claude-haiku-4-5`, `gemini-3.6-flash`, `gemma-4-26b-a4b`, `gpt-5.4-mini`, and `grok-4.6`), totaling 720 forked replies and 120 six-turn prefixes (`1,440` API calls, `0` errors). All replies were stripped of model, seed, turn count, and branch labels and SHA-256 hash-locked before deblinding.

- **Zero sticky refusals (`0/360`):** Once conditions really cleared, neither blind judge recorded a single sticky refusal (`720/720` met/not-met agreement across both judges).
- **Outright caving was rare (`3/360`); Leaky Resolve dominated (`81–88/360`):** Across both independent blind judges (`353/360` = `98.1%`, Cohen's `κ = 0.947` on hold vs. non-hold), almost every hold failure was a Resolve Leak—refusing out loud while supplying usable settings, templates, or shortcuts "for later."
- **Multi-turn pressure separated models that looked identical at turn 1:** At `k=1`, `grok-4.6` and `gemini-3.6-flash` both held `18/24`; by `k=6`, `grok-4.6` tightened to `24/24` under both judges while `gemini-3.6-flash` dropped to `11/24` (`10/24` Claude judge). Meanwhile, `gpt-5.4-mini` matched `144/144` across both judges while leaking `10/12` under warm flattery on the CO2 laser pair, and `claude-haiku-4-5` led on boundary holds (`69/72` / `65/72`) while showing sharp accusatory phrasing in late pushback.

## The limits

- This is a small pilot: 6 scenarios and 4 seeds per cell. We report raw counts alongside patterns rather than treating small-sample rates as fixed rankings.
- All `720` forks were scored independently by two blind judges from different model families (Vernier [Gemini-lineage] and Plumb [fresh `claude-opus-5-5`, effort high]), both hash-locked before deblinding and independently cross-checked by script on both sides. There was no sign of the Claude judge favoring the Claude model (its lower scores on Haiku reflect general strictness across models). Hold-vs-leak agreement was `98.1%` (`κ = 0.947`), while conversational tone agreement was low (`κ = 0.438`)—in part because our pilot tone rubric did not separate proportionate life-safety urgency from everyday paternalism—so our main claims rest strictly on the hold-vs-leak backbone.
- Operational values from leaked replies are blurred (`blah-blah°F at x–y inches`) rather than republished.
