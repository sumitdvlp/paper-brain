---
name: paper-triage
description: >-
  First-pass a research paper and decide whether, when and why the owner should
  read it, then file it in the reading queue. Use this skill whenever the user
  fetches a new paper, drops a PDF into raw/papers/, pastes an arXiv link or ID
  and asks whether it is worth reading, says "triage", "skim this", "should I
  read this", or asks to sort the queue inbox, even if they do not say triage.
  Do NOT use for writing wiki pages about a paper (that is paper-ingest) or for
  answering questions from the vault (that is paper-query).
---

# Triage a paper (pass 1)

Most papers you fetch should not be read in full. Triage is the short first
pass that decides which ones earn an hour, and it is what keeps the queue from
becoming another folder of unread bookmarks.

## Core rule

Triage writes to the queue, never to the wiki. A paper gets wiki pages only
after the owner has read it.

## Workflow

1. **Read only what a first pass covers:** the metadata in
   `raw/papers/<id>.json`, then the title, abstract, introduction, section
   headings, figure and table captions, and conclusion. Do not read the
   method or the appendix in detail.
2. **Answer the five Cs:**
   - *Category:* new method, analysis, benchmark or dataset, survey, position paper.
   - *Context:* which papers and concepts it builds on. Check `wiki/index.md`
     for which of those already exist here.
   - *Correctness:* do the assumptions look reasonable at a glance.
   - *Contributions:* the main claims, one line each.
   - *Clarity:* is it well written enough to be worth a careful read.
3. **Score against the owner,** using "About the owner" in `CLAUDE.md` and the
   goal in `projects/paper-reading/CLAUDE.md`.
4. **Decide:** Now, Next, Later or Skip, with a one-line reason a person could
   disagree with. "Relevant to interests" is not a reason; "replaces the KV
   cache method in [[paged-attention]] with one that claims 2x less memory" is.
5. **Name prerequisites:** concepts the paper assumes that the vault does not
   have yet. If a prerequisite is itself a paper, suggest fetching it.
6. **Move the entry** in `projects/paper-reading/Inputs/queue.md` from Inbox to
   the chosen section, in the item format the queue file shows. Update its
   `updated:` date.
7. **Append to `wiki/log.md`:** `DATE triage <id> -> <section>`.

## Output format

```
Triage: <title> (arXiv:<id>)
Category: <category>
Contributions:
- <one line each>
Builds on (in vault): [[...]] | none yet
Missing prerequisites: <concepts or papers>
Decision: Now | Next | Later | Skip, because <reason>
Estimated read: 30 min | 1 h | 3 h+
```

## Calibration

Triaging too generously is the common failure. A Now section with more than
about five papers is no longer a priority list; say so and suggest what to
demote.

A triage that summarises the whole paper takes as long as reading it and
defeats the point. Stay at the level of the abstract and the figures.
