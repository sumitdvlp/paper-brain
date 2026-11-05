---
name: paper-quiz
description: >-
  Test the owner on papers and concepts they have read, from their own vault
  pages, either by asking questions or by having them explain a concept back
  and grading the explanation. Use this skill whenever the user wants to test
  themselves, revise, review for a reading group, make flashcards, explain
  something back, check what they have forgotten, or asks "quiz me". Do NOT
  use for generic quizzing on topics the vault does not cover, or for
  answering a question from the vault.
---

# Quiz and explain-back

Reading a paper is not the same as learning it. The test is whether the owner
can say what it showed and why it works without the page open.

## Core rule

Questions and grading come from the owner's pages, at the depth those pages
record. Never from general knowledge about the topic.

## Workflow

1. **Pick the scope:** a topic, a paper, papers ingested in the last week, or
   papers listed in `projects/paper-reading/Feedback/to-explain.md`.
2. **Quiz mode.** Write five to eight questions of three kinds:
   - *Recall:* what did the paper show, with which number, on which benchmark.
   - *Mechanism:* why the method works, as the concept page explains it.
   - *Transfer:* what would happen in a new case (a longer sequence, a smaller
     model, a different dataset), answerable from the pages.
   Withhold answers until the owner has attempted them.
3. **Explain mode.** Ask the owner to explain one concept in their own words.
   Compare against the concept page: what they got right, what they missed,
   what they got wrong.
4. **Grade against the page, not against what is true.** If the owner is
   right and the page is wrong or unclear, that is a page problem worth fixing.
5. **Log** one line to `projects/paper-reading/Feedback/quiz-log.md`.
6. **Offer** to write any missing takes from what the owner just said, with
   their approval, and remove those papers from `to-explain.md`.

## Output format

```
<n> questions from <n> pages

1. <question>
...

[after answers]
Solid: <topics>
Shaky: <topics, with the pages to reread>
Page problems found: <pages that are unclear or wrong>
```

## Calibration

Keep a session to a handful of pages. A page that cannot produce a good
transfer question usually records the paper's wording instead of an
understanding of it; say so.
