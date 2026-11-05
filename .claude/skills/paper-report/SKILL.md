---
name: paper-report
description: >-
  Write a mini-survey of a research topic from the papers in the vault, saved
  to output/: scope, background concepts, a taxonomy of approaches, how the
  line of work developed, a comparison on shared benchmarks, where papers
  disagree, open problems, and what the vault cannot establish, with every
  claim cited to a vault page. Use this skill whenever the user asks for a
  report, a survey, a literature review, a related-work section, a write-up
  for a reading group, or a document summarising what they have read on a
  topic, even if they do not say report. Do NOT use for a quick answer (that
  is paper-query), for a single-claim wiki page (that is paper-synthesize), or
  for summarising one paper.
---

# Write a mini-survey

A survey that presents only findings looks stronger and is less useful,
because the reader cannot tell where it rests on five papers and where it rests
on one. The value of writing it from the vault is that every sentence can be
traced, and the gaps are visible.

## Core rule

Scope against the vault before writing, and report the gaps first. Every claim
in the survey cites a vault page; nothing comes from general knowledge unless
it is labelled as outside the vault.

## Workflow

1. **Inventory.** From `wiki/index.md`, list the papers, concepts, models and
   benchmarks on the topic. Note which are thin: papers with `status: skimmed`,
   concept pages with no Evidence section, takes still pending.
2. **Check the threshold.** Fewer than three papers on the topic is a reading
   list, not a survey. Say so, suggest the papers from Gaps in `wiki/index.md`
   to `/fetch`, and stop unless the owner says go ahead.
3. **Report the gaps before writing,** in a few lines, so the owner can decide
   whether to read more first.
4. **Build the skeleton from the graph:** group papers by the concept pages
   they link to (that is the taxonomy), order them by `year` (that is the
   lineage), and collect Key results rows that share benchmark, metric and
   setting (that is the comparison table).
5. **Write** in the format below. Link papers as `[[slug|Author Year]]` so the
   survey stays navigable in Obsidian, and give each one its arXiv id in the
   References section so it also reads outside the vault.
6. **Save** to `output/report-<topic-slug>-<YYYY-MM-DD>.md` with frontmatter
   `type: report`, `created`, `topic`, `papers: [slugs]`. Never write inside
   `wiki/`.
7. **Log** one line to `wiki/log.md`, then offer to turn the survey's central
   claim into a synthesis page with `paper-synthesize`.

## Output format

```
# <Topic>: a survey of N papers in this vault

## Scope            what is covered, what is deliberately left out
## Background       the concepts a reader needs, each linked
## Approaches       the taxonomy: one subsection per family of methods
## How it developed the lineage, by year, with what each step changed
## Comparison       table on shared benchmarks; mismatched settings marked
## Where papers disagree
## Open problems
## What this vault cannot establish
## References       Author Year, title, arXiv id, [[page]]
```

## Calibration

If the vault covers less than half the topic, say so in the first paragraph
rather than producing a survey that reads as complete.

The comparison table is where surveys most often mislead. A cell from a
different model size, dataset split or metric is marked "not comparable" with
the reason, never silently placed next to the others.

Keep it to what a reader could finish in fifteen minutes. A survey of ten
papers that runs past three thousand words is restating paper pages; link to
them instead.
