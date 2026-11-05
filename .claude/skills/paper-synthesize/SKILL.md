---
name: paper-synthesize
description: >-
  Write a synthesis page that says something no single paper in the vault
  says: a lineage of how a method developed, a comparison of methods on a
  shared benchmark, a recorded contradiction between papers, or an open
  question that keeps coming up. Use this skill whenever the user asks to
  write up, map or summarise a line of work across several papers, build a
  family tree of methods, compare approaches in a page they can keep, or
  record where papers disagree, even if they do not say synthesis. Do NOT use
  for one-off answers that do not need saving (that is paper-query), for a
  longer survey document meant for outside the vault (that is paper-report),
  or for ingesting a single paper.
---

# Write a synthesis page

Synthesis pages are where reading many papers turns into understanding a
field. They are also the easiest pages to fake: a list of paper summaries with
a heading on top is not a synthesis.

## Core rule

A synthesis page must make a claim no single paper page makes, and every part
of that claim must trace to a page in the vault.

## Workflow

1. **Gather** the relevant pages the way `paper-query` does: index first, then
   links outward.
2. **Check the threshold.** A lineage needs at least three papers. A comparison
   needs at least two papers with results in a matching setting. A
   contradiction needs two papers that actually disagree on the same question.
   If the vault does not meet the threshold, say what is missing and stop.
3. **Pick the kind** (`lineage`, `comparison`, `contradiction`,
   `open-question`) and write from `templates/synthesis.md`.
   - A lineage says what each step changed and why, not just what came next.
   - A comparison table marks every cell that is not directly comparable.
   - A contradiction states both positions fairly, then the current position
     and what evidence would settle it.
4. **Link back.** Every paper and concept the page draws on gets a link to the
   synthesis page in its Related or Links section.
5. **Update `wiki/index.md`** and append to `wiki/log.md`.

## Output format

```
Synthesis: [[<page>]] (<kind>)
Claim: <the one-sentence point no single paper makes>
Draws on: <n> papers, <n> concepts
Back-links added: <n>
Missing for a stronger version: <papers or results not in the vault>
```

## Calibration

If you cannot state the claim in one sentence, the page is not ready. Report
what is missing instead of writing a page that restates its sources.
