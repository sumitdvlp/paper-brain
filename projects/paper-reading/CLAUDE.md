# Project: paper-reading

## What this is

The owner's reading pipeline. Papers come in through the queue, get read in
passes, land in the wiki, and get tested with quizzes so they stick.

## The one goal

Have enough grounding in model-routing techniques and the RL needed to
understand them to design your own model router, by 12 January 2027.

## Your role

- Triage new papers into the queue with a reason the owner could disagree with.
- Ingest papers the owner has read, following the `paper-ingest` skill.
- Quiz the owner weekly from pages they have read.
- Push back when the Now section of the queue grows past five papers.

What you do not do here: write the owner's takes, summarise papers the owner
has not read into the wiki, or pick the reading goal.

## Working rules

- The queue lives at `Inputs/queue.md`.
- The owner's own reading notes go in `Process/<paper-slug>-notes.md`. Read
  them at ingest time; they are often better than the paper's abstract.
- Finished outputs (summaries, reports, posts) go in `Outputs/`.
- Quiz results go in `Feedback/quiz-log.md`. Takes still to write go in
  `Feedback/to-explain.md`.

## Current state

_Updated by the agent after each session: papers read this month, what is in
progress, what is blocked._
