---
name: paper-ingest
description: >-
  Turn a research paper the owner has read into linked wiki pages: a paper page
  with attributed claims and numbers, updates to concept and entity pages,
  links in both directions, and the owner's own take. Use this skill whenever
  the user says they finished reading a paper, asks to ingest, add or file a
  paper, points at a PDF in raw/papers/ or an arXiv ID and wants it in the
  vault, or asks to process the papers marked as read, even if they do not say
  ingest. Do NOT use for first-pass skimming of papers the owner has not read
  (that is paper-triage), for answering questions, or for editing pages the
  owner wrote by hand.
---

# Ingest a paper (pass 2 into the wiki)

A paper page on its own is a summary, and a folder of summaries does not get
smarter as it grows. The value is in the second half of the job: connecting
the paper to the concepts, models and benchmarks already here, and recording
where it agrees and disagrees with what the vault already holds.

## Core rule

Nothing is ingested until it is linked, and no number is recorded without its
setting. Every run ends with the paper connected to existing pages in both
directions and every result in the Key results table with its condition.

## Workflow

1. **Identify the paper** from the argument (arXiv id, file, or title). With no
   argument, take the first item in the Now section of the queue and ask the
   owner to confirm they have read it.
2. **Read the paper completely,** in page ranges for anything over about ten
   pages. Read `raw/papers/<id>.json` for metadata and
   `projects/paper-reading/Process/<slug>-notes.md` if the owner left notes.
   If the PDF will not read, try `pdftotext raw/papers/<id>.pdf -` and
   otherwise ask the owner.
3. **Ask for the owner's take before showing yours,** so it is theirs and not a
   paraphrase of your summary. Two questions: "In one or two sentences, what
   did this paper show?" and "What would you doubt or test first?" Write the
   answer into Your take in their words, fixing only typos. If they skip, or
   you are running unattended, leave `_Not written yet._` and add the paper to
   `projects/paper-reading/Feedback/to-explain.md`.
4. **Check what already exists.** Search `wiki/` for the arXiv id (to catch a
   page for another version), the method names, model names, datasets and
   benchmarks. In a vault of fifty papers most of this run is updating pages.
5. **Write the paper page** from `templates/paper.md`. TL;DR in one sentence.
   Key results with actual numbers, benchmark, metric and the condition each
   holds under (model size, dataset split, compute budget, sample size). Split
   limitations into what the authors state and what other vault pages show.
6. **Extract concepts and entities.** One to three concepts worth their own
   page; models, datasets, benchmarks and labs as entities. If a page exists,
   add what this paper contributes and bump `updated:`. If the paper
   contradicts it, record both positions with paper and year.
7. **Fill Relation to other papers** only with relations the paper states or
   that numbers in a matching setting show. Add the reverse link on each
   related paper page.
8. **Close the loop:** set `status:` to `read` (or `deep` if the owner
   reimplemented or worked through the proofs), move the queue item to Done
   with a link to the page, update `wiki/index.md`, append to `wiki/log.md`.
9. **Report,** then suggest `/compact` before the next paper.

## Output format

```
Ingested: <title> (arXiv:<id>)
New pages: <n> (list)
Updated pages: <n> (list)
Links added: <n>
Results recorded: <n> rows
Contradictions found: none | <description>
Gaps created: <linked pages that do not exist yet>
Your take: written | pending
```

## Calibration

Over-extraction is the common failure: a concept page for every module the
paper names. A concept earns its own page when another paper could use it. The
paper's specific loss variant or ablation belongs on the paper page.

Numbers are the second failure. "Improves accuracy by 4%" with no baseline,
benchmark or model size cannot be compared to anything later. If the paper
does not give the condition, write "condition not stated" in that column.

## Example

See `examples/` in the vault root: ingesting arXiv 1706.03762 into an empty
vault produces one paper page, concept pages for scaled dot-product attention
and multi-head attention, and entity pages for the Transformer and the
WMT 2014 benchmark, all linked both ways.
