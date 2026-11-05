---
name: paper-lint
description: >-
  Audit the paper vault for structural and paper-specific problems and repair
  the mechanical ones: broken wikilinks, orphans, stubs, frontmatter that
  breaks the schema, paper pages missing an arXiv id or year, results without
  conditions, duplicate pages for the same paper, missing takes, and a queue
  that disagrees with the wiki. Use this skill whenever the user asks to lint,
  clean, audit or health-check the vault, after ingesting many papers, or when
  a scheduled maintenance run fires. Do NOT use for ingesting, answering
  questions, or rewriting pages that are structurally fine.
---

# Lint the vault

Structural rot is silent. Nothing errors; the vault slowly stops answering
questions well because pages are unreachable and numbers lost their settings.

## Core rule

Report before repairing. Fix mechanical problems automatically; never delete or
merge a page without listing it first and getting a yes.

## Workflow

1. **Run the scripts** from the vault root (use `python` instead of `python3`
   on Windows):
   - `python3 scripts/vault_stats.py .`
   - `python3 scripts/link_check.py .`
   - `python3 scripts/paper_check.py .`
2. **Broken links:** fix typos and renames; put genuine gaps under Gaps in
   `wiki/index.md`. Convert alias links (`[[Vaswani 2017]]`) to file-name
   links with a label.
3. **Orphans:** add the missing link from where the page belongs, or flag it.
4. **Stubs:** pages under about 40 words. Flag for re-ingest.
5. **Paper checks:** missing `arxiv` or `year`, Key results rows with an empty
   condition column, two pages with the same arXiv id, `status` that disagrees
   with the queue. Fill metadata from `raw/papers/<id>.json` where it exists.
6. **Takes:** make sure every paper with an empty Your take is listed in
   `projects/paper-reading/Feedback/to-explain.md`.
7. **Near-duplicates:** concept or entity pages for the same thing under
   different names (`kv-cache` and `key-value-cache`). Propose merges only.
8. **Index drift:** pages missing from `wiki/index.md`, entries pointing
   nowhere.
9. **Repair,** then append the run to `wiki/log.md`.

## Output format

```
Vault: <n> pages (<n> papers, <n> concepts, <n> entities, <n> synthesis)
Link graph: <n> links, average <n> per page, <n> orphans

Fixed automatically:
- <list>

Needs a decision:
- <list, each with the recommended action>

Health: orphan rate <n>%, broken links <n>, results without conditions <n>, takes pending <n>
```

## Calibration

Weekly, or after ingesting more than about ten papers. Not after every ingest.
