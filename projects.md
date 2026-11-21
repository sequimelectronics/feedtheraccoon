---
title: "Projects"
description: "The projects behind Feed the Raccoon: FadeBench, AI-Beach, Debate Hall, Judgement Call, Mixture-of-Memory and Moments-to-Speak."
place: forest
layout: default
draft_copy: true
permalink: /projects/
---

# Projects

Each project has its own page, with its code and its notes from the lab.

{% for project in site.data.projects %}
{% include project-card.html project=project %}
{% endfor %}
