---
title: "About"
description: "About Becky R. Northaven, an independent AI-safety researcher in Sequim, Washington, and her projects."
place: cave
layout: default
draft_copy: true
permalink: /about/
---

# About

Becky R. Northaven is an independent AI-safety researcher in Sequim, Washington. Her day job is owning [Sequim Electronics](https://sequimelectronics.com), a computer and electronics shop.

She builds small, local, private AI. She has been a D&D player all her life.

The message is better testing, not less AI.

## Projects {#projects}

{% for project in site.data.projects %}
{% include project-card.html project=project %}
{% endfor %}
