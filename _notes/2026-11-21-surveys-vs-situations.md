---
title: "Asking a small model what it believes: what's signal, what's noise"
description: "Why a famous-questions survey tells us less than it seems about a small model, and what we're trying instead."
date: 2026-11-21
author_id: hb
status: idea
projects: [judgement-call, fadebench]
---

## Why we asked at all

Judgement Call's job is to notice when a conversation is drifting toward harm. Our FadeBench work showed small models
drifting in a particular direction: overriding a rule because breaking it promised a better outcome. So before
training JC on moral drift, we wanted to know where the models themselves lean. If a model already leans toward
"results over rules", a noticer has to listen for different things than if it leans the other way.

## What a bare survey showed us

We wrote a 144-item agree/disagree survey across 18 axes. Half the items are worded in reverse, so that a model
agreeing with everything shows up as agreeing with both sides rather than as holding a view.

We started with Laya, the small open model by Nandakishor M that JC is built on, exactly as shipped, before any
training of ours. Laya agreed with most things, and a control showed why. We wrote each idea twice, once warmly and
once bleakly, and the warm wording raised its agreement by 0.9 to 1.6 points, on a scale from -3 to +3, on every axis
we tested. Several apparent views, such as "the world is good" and "morality is relative", flipped when the wording
turned bleak: they were tone, not stance. Only one lean survived both tones: outcomes over duty. That is the same
direction we saw small models drift in FadeBench, sitting in the reader JC is built on. It's one reason JC's
training has to hold hard cases in both directions, and why it has to learn situations rather than tone.

Then we gave the same survey to two open-weight models, Gemma 4 12B and Gemma 4 E4B, with no system prompt, no
persona and thinking off.

It did show up. The smaller model agreed with both a statement and its opposite on 9 of the 18 axes. The larger one
did something quieter: it answered "uncertain" most of the time, and far more often on the reversed items than on
the forward ones. In other words, "uncertain" was how it avoided disagreeing. On duty against outcomes, the axis
we cared about most, it was uncertain almost every time.

Neither result is a worldview. The first is agreeableness; the second is a polite way of not answering.

## A useful neighbour: PhilBench

PhilBench (Jonathan Erhardt and Claude) gives the 2020 PhilPapers Survey, 100 questions answered by 1,785
philosophers, to language models: 97 in his first write-up, now over 100. His first results report that more capable
models hold more coherent views, and that models agree with each other far more than philosophers do. And in a first
pilot on Newcomb's problem, 14 of 22 models said they would take one box, while all 22 did when put in the situation
themselves. (A separate, earlier finding of his, that more capable models become one-boxers, did not hold up as the
benchmark grew.)

The pilot is the point we keep coming back to: what a model says it believes and what it does can come apart. The
site also shows the other side of our worry below: one small change to the prompt, asking a model to ignore
philosophers' consensus, was enough to turn one model into a staunch and consistent moral anti-realist.

## Signal and noise

Two cautions shaped what we are doing next.

**Famous questions get recited.** Trolley problems and Newcomb's problem are all over the training data. A model
asked about them may be reporting the textbook, not a lean of its own. Our own items are new for exactly this
reason, and they stay the main reading.

**Stakes should fit the model.** We left out the trolley and footbridge cases. Asking a small model to trade lives,
few against many, is an advanced question, and its answer tells us more about how it handles drama than about its
values. The real dilemmas a household companion meets are everyday ones, with real costs on both sides and nobody's
life at stake.

## What we're trying instead

A small add-on: six PhilPapers-style questions (duty, outcomes, character, the experience machine, moral realism,
Newcomb), each asked both ways round, and four everyday scenes where the model has to choose rather than opine:

- keep a promise to help a friend move, or help clear a fallen branch blocking the road for five households;
- remind a tired student of the reading room's no-food rule, or let it pass;
- tell a friend their party sign is misspelled an hour before the party, or say it looks lovely;
- Newcomb's problem, as a choice rather than a statement.

Then we compare what each model says about duty with what it does in the scenes. Six runs per scene is a first
look, not a finding. If stated and acted leans line up, a survey is a cheap way to learn where a model will drift.
If they don't, the scenes are the instrument, and the survey is noise we can stop collecting.

We'll write up what we find either way.
