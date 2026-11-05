---
name: paper-query
description: >-
  Answer a question from the paper vault by reading its own pages, citing every
  page used, and saying plainly what the vault does not cover. Covers plain
  questions, comparing two methods or papers, finding the path that connects
  two methods, tracing how an idea developed over time, listing
  contradictions, and showing which papers a claim rests on. Use this skill
  whenever the user asks what they know or have read about a method, model or
  benchmark, how two papers compare, how two ideas are related, how an idea
  evolved, where papers disagree, or asks any question that should be answered
  from their own reading rather than general knowledge. Do NOT use for
  ingesting papers, for writing synthesis pages (that is paper-synthesize), for
  a saved survey document (that is paper-report), or when the user explicitly
  wants an answer from the open web.
---

# Query the vault

An answer that quietly blends general knowledge with the owner's notes is
worse than no answer, because it cannot be checked. The owner built this vault
so answers rest on papers they actually read.

## Core rule

Every claim in the answer comes from a page in the vault and names that page.
Anything you know that the vault does not is labelled as outside knowledge or
left out.

## Workflow

1. **Start from `wiki/index.md`,** not a full-text sweep.
2. **Follow links outward** one hop at a time from the most relevant pages.
   Stop when new pages stop adding anything.
3. **Answer in the mode the request asks for:**
   - *Ask:* plain prose with `[[page]]` references inline.
   - *Compare:* a table with one column per paper or method. Put numbers side
     by side only when benchmark, metric and setting match; otherwise write
     "not comparable: <why>".
   - *Connect:* run `python3 scripts/link_path.py . <A> <B>` to get the
     shortest paths through the link graph, then read every page on each path
     and say what each hop means ("multi-head attention is the building block
     of the Transformer, which Vaswani 2017 evaluates on WMT 2014"). Drop a
     path whose hops are only incidental mentions. If there is no path, say so,
     and name the concept or paper that would bridge the two.
   - *Timeline:* papers ordered by `year`, one line each on what that paper
     changed. End with where the line stands now in this vault.
   - *Contradictions:* each disagreement with both positions, both papers, and
     whether a later page marks one as superseded.
   - *Sources:* the papers a claim rests on, and how directly each supports it.
4. **Name the gaps.** If the question has three parts and the vault covers two,
   say which.
5. **Offer the next move** when there is an obvious one: a prerequisite paper
   worth fetching, or a synthesis page worth writing with `/synthesize`.

## Output format

The answer, then:

```
Read: <pages consulted>
Not covered: <what the vault does not answer>
Next: <paper to fetch or synthesis to write, if any>
```

## Calibration

Reading too little is the common failure: answering from two pages when the
vault has ten relevant ones. Reading every page is the opposite failure.

If the vault has nothing on the topic, say so in one sentence and stop.
