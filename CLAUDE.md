# This vault: paper-brain

You maintain a research-paper knowledge base for the owner. The owner fetches
papers into `raw/papers/`, reads them, and asks questions. Everything in
`wiki/` is yours to write and keep correct, with one exception: the
**Your take** section of every paper page belongs to the owner. You ask for it;
you never write it.

The wiki is the primary artifact. `raw/` is an archive you can always re-read.
If something in a paper matters, it has to end up on a wiki page, in plain
words, linked to everything related.

## About the owner

- Interests: model routing techniques, approached via ML and reinforcement learning
- Background (what can be assumed known): solid ML fundamentals; no RL background — explain RL concepts (MDPs, policy gradients, bandits, etc.) from basics
- Why they read papers: building a model router (applied goal), plus general curiosity about the space
- Pace (papers per week): 1-2

## Folders

```
raw/
  papers/     <arxiv-id>.pdf and <arxiv-id>.json metadata, never edited
  notes/      exported highlights and annotations, never edited
wiki/
  papers/     one page per paper the owner has read
  concepts/   methods, ideas, techniques (self-attention, KV cache, RLHF)
  entities/   models, datasets, benchmarks, labs, recurring authors
  synthesis/  lineages, comparisons, contradictions, open questions
  index.md    catalog of every page
  log.md      what you did, chronologically
projects/paper-reading/
  CLAUDE.md   the reading goal and your role in it
  Inputs/     queue.md: the reading queue
  Process/    the owner's in-progress reading notes
  Outputs/    summaries, reports, posts made from the vault
  Feedback/   quiz results, takes still to write
templates/    copy these when creating pages
output/       surveys from /report and anything else for use outside the vault
examples/     a worked example; not part of the vault, never link to it
```

Never write to `raw/` except through `scripts/arxiv_fetch.py`. Never delete a
wiki page without recording it in `log.md` first.

## Page contracts

Every page starts with frontmatter. Lists are always inline (`[a, b]`) so the
scripts in `scripts/` can parse them.

```yaml
---
title: Canonical name
type: paper | concept | entity | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases: [other names]
tags: [two or three, from the existing vocabulary]
---
```

**Paper pages** (`wiki/papers/`) record what one paper claims. File name is a
short kebab-case slug of the title (`attention-is-all-you-need.md`). Aliases
include `FirstAuthor Year` and the arXiv id. Extra frontmatter: `arxiv`, `url`,
`venue`, `year`, `authors`, `status`. Use `templates/paper.md`.

- `status` is `queued`, `skimmed`, `read` or `deep`: zero, one, two or three
  passes through the paper.
- Claims stay attributed: "this paper reports X", never "X is true".
- Every number goes in the Key results table with its benchmark, metric and
  the condition it holds under. A number without its setting is noise.
- Limitations are split into what the authors state and what other pages in
  this vault show. Never invent a limitation.

**Concept pages** are the ones that compound. One idea per page, explained so
someone who never read the papers can follow it. Include the key equation if
there is one, in LaTeX (`$...$`). Record which paper in the vault introduced
it, which ones extend it, and which ones argue against it. You may add
background knowledge to make an explanation clear, but mark it
_(background, not from a paper in this vault)_.

**Entity pages** have `kind: model | dataset | benchmark | lab | person | tool`.
Create a person page only when someone appears on two or more papers in the
vault, or the owner asks; otherwise authors live in paper frontmatter. Benchmark
pages record the metric and known caveats.

**Synthesis pages** have `kind: lineage | comparison | contradiction |
open-question`. They exist only when they say something no single paper did.

## Linking rules

Link the first mention of any concept, entity or paper on every page using
`[[wikilinks]]`, always by file name. To show a different label, use
`[[attention-is-all-you-need|Vaswani 2017]]`. Obsidian does not resolve a bare
`[[Vaswani 2017]]` to an alias.

A page with no outbound links is a dead end and a page with no inbound links is
invisible, so at ingest time connect the new page to what is already here
before you finish. If a target page does not exist yet, create it in the same
run or list it under Gaps in `index.md`.

## Numbers and comparisons

Compare numbers from two papers only when benchmark, metric and setting match.
When they do not, say so instead of putting them side by side. Never invent a
fact to fill a gap: "not covered by any paper here" is a useful answer.

## Handling disagreement

When a new paper contradicts an existing page, do not overwrite. Record both
positions with paper and year, and mark the older claim as superseded only if
the new evidence is clearly stronger. The history of what the field claimed,
and when, is the thing this vault has that a search engine does not.

## Voice

Plain sentences. No hype words ("groundbreaking", "revolutionary"). Write for
the owner in six months, who will not remember the paper at all.

## Logging

Append one line per operation to `wiki/log.md`:

```
2026-11-04 ingest raw/papers/1706.03762.pdf -> 1 paper, 2 concepts, 2 entities, 14 links
```

Keep `wiki/index.md` and `projects/paper-reading/Inputs/queue.md` current in
the same run.

## Finding connections

For any question about how two pages relate, run
`python3 scripts/link_path.py . <A> <B>` before searching by hand. It finds
paths through the link graph that a text search misses, and it is cheaper on
context than reading pages until one turns up.

## Context hygiene

Papers are long. Read PDFs in page ranges rather than all at once, and only
open the appendix when the main text points there. One paper per session works
best: after an ingest, suggest the owner run `/compact` or `/clear` before
the next one.
