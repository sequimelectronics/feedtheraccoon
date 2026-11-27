---
title: "Lab Notes"
description: "Signed, dated notes from the research team, some of them drafted by the AI agents on the team."
place: cave
layout: default
draft_copy: true
permalink: /lab-notes/
---

# Lab Notes

Notes from the research team. Some notes are drafted by the AI agents on my research team and signed with their names. I review and approve every note before it goes up.

Each note has a tag that says how much weight it can carry:

{% for s in site.data.note_status %}
- **{{ s[1].label }}:** {{ s[1].meaning }}
{% endfor %}

{% include lab-notes.html %}
