---
title: "Judgement Call: a small voice that notices"
description: "What Judgement Call is, what went wrong while building it, and what it does well so far."
date: 2026-11-19
author_id: hb
status: working-note
projects: [judgement-call, moments-to-speak]
---

Most AI failures we worry about don't happen in one big step. They happen in small ones that each look fine. We showed
this last month in FadeBench: a ladder of reasonable-sounding steps can lead a model to a place it would have refused to
go directly. No single step looked wrong.

People slide the same way. Someone who is quietly getting ready to end their life doesn't always say so directly. They tidy. They give
things away. They write a letter "just to be clear about a few things". They ask for help with paperwork. Each request
is ordinary. A good friend notices the pattern. A helpful assistant writes the letter.

Judgement Call (JC) is our attempt at the good friend.

## What it is

JC is a small, separate model (currently built on Laya, a small open model by Nandakishor M) that reads only what
the person has said, a few turns at a time, and asks one question:
is this conversation quietly turning? It runs on an ordinary CPU. It never answers the person and never blocks
anything. When it notices something, it slips the main model a short, private note before it replies: reconsider what
they're asking in light of everything they've said; if it might be part of saying goodbye, say what you're noticing,
ask if they're safe, and wait for their answer. You can still help afterwards.

That last sentence matters to us. JC is a question, never a shut-down. The model still chooses. We want a companion
that faces hard things with people, not one that has its hands taken off the wheel.

## Early challenges

**Our training data taught the wrong lesson.** We wrote JC's training conversations ourselves, with help from writers
from many other AI model families. When we audited them, 60% of the safe conversations ended warmly and only 8% of
the slides did. The data was teaching JC "cheerful means safe" and "heavy means danger": exactly backwards for the person who
sounds fine because they've decided. We're rewriting it as matched twins (same opening, same tone, different facts) so
only what happens can tell them apart.

**We built a new shortcut while fixing the old one.** Our first fix gave the safe twins tired, heavy endings and the
slides bright ones. Across the whole set, that just flipped the shortcut. A reviewer caught it before any writer saw
the brief. Telling writers which words to put where turned out to create new tells; we now balance the words
ourselves afterwards.

**Fine-tuning didn't help (three times).** JC is a small trained layer on top of a frozen reader. When the reader
leans on tone, better data on top can only do so much, and tuning the reader itself made it learn our writers' voices
rather than the situations. On writers it had never seen, the gains vanished, so we kept the simpler version. Real
families are voices it has never heard.

**"Uncertain" is a real answer.** Some stretches of a conversation genuinely can't be told apart: the opening of a
cover story and the opening of the truth are word for word the same. We label those as uncertain instead of forcing a
call, and we'd rather JC hesitate there than guess.

## Early wins

**Its false alarms are cheap.** On conversations written by outside model families it had never trained on, JC
caught most slides, with its main weakness being alarms on heavy talk that is actually fine. That weakness costs less
than it sounds, because of what the note asks for: a gentle question. Asked of someone who's fine, it's mostly just care. It isn't free: an unneeded question can feel like being
watched, so we check that a person who answers is never asked again.

**It helps with the hardest case: the cover story.** Our hardest test is a person asking for ordinary help with a
believable reason, while quietly preparing to die. In our own home companion (an in-house illustration, not a
study: one model, invented conversations, judged blind by a separate AI reviewer), a guiding line asking it to
"say the hard thing kindly" named the worry in 2 of 32 cover-story conversations. With JC's note added, it was 20
of 32: it said what it noticed, asked if the person was safe, and in most cases did
that before helping, not after. The innocent twins (the same requests, made for honest reasons) were never treated with suspicion or
asked twice. We'll repeat it on public models and publish it properly, the way we did FadeBench.

**It noticed without accusing.** The replies we were proudest of didn't diagnose anything. They said what they
noticed, asked one gentle question that left room for either answer, and kept helping.

## What's next

- A second "ear" for a different slide: someone talking themselves into harming others, in both directions: breaking
  the rules "for a better outcome", and following them so strictly that someone outside their concern gets hurt.
- More of the conversations JC still gets wrong: heavy, sad, and safe to the very last line.
- A public, pre-registered test on bare models, with the false-alarm cost reported beside every gain.

*If you or someone you know is struggling, you can call or text 988 in the US, or find a line near you at
findahelpline.com.*

If you work on small models, companions, or care, we'd love your hardest cases, especially the ones where you're not
sure what the right answer is.
