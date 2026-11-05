---
title: Reading queue
type: queue
updated: 2026-11-04
---

# Reading queue

Item format: `- **Title** · arXiv:ID · reason · added YYYY-MM-DD`

## Now

Reading this week. Keep this to five or fewer.

- **FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance** · arXiv:2305.05176 · earliest paper here, defines the cascade framing everything else reacts to · added 2026-11-04
- **RouteLLM: Learning to Route LLMs with Preference Data** · arXiv:2406.18665 · the most-cited learned-router baseline that later benchmarks measure against · added 2026-11-04
- **Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs** · arXiv:2510.07429 · the RL-style router you've been missing: contextual bandit trained under partial feedback, a direct rebuttal to RouteLLM's offline-labels assumption · added 2026-11-04

## Next

- **RouterBench: A Benchmark for Multi-LLM Routing System** · arXiv:2403.12031 · benchmark + theoretical framework, best read once a method (FrugalGPT, RouteLLM) is in hand · added 2026-11-04
- **LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing** · arXiv:2601.07206 · re-evaluates RouteLLM-style routers under one protocol, finds several don't beat a simple baseline · added 2026-11-04

## Later

- **LLM Router: Rethinking Routing with Prefill Activations** · arXiv:2603.20895 · activation-based routing, a narrower follow-on technique once the semantic-router baseline picture is solid · added 2026-11-04
- **RSI-Router: Evolving Subtask-Level LLM Routing and Skills for Cost-Efficient Agents** · arXiv:2609.34712 · routing for multi-step agents, not single queries; a different problem scope best tackled once single-query routing is solid · added 2026-11-04

## Done

Moved here at ingest, with a link to the paper page.

_Empty._

## Skipped

Kept so you remember why you passed on something.

_Empty._

## Inbox

Fetched, not triaged yet. `scripts/arxiv_fetch.py` appends here.

_Empty._
