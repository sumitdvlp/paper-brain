---
title: Multi-head attention
type: concept
created: 2026-11-04
updated: 2026-11-04
aliases: [MHA]
tags: [attention]
---

# Multi-head attention

## In one paragraph

Instead of one attention over the full representation, the model projects
queries, keys and values into several smaller spaces and runs
[[scaled-dot-product-attention]] in each one separately. Each head can attend
to different positions for different reasons; their outputs are concatenated
and projected back. With the head size shrunk accordingly, the total compute
is about the same as one full-size head.

## How it works

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)\,W^O$$
$$\text{head}_i = \text{Attention}(QW_i^Q,\; KW_i^K,\; VW_i^V)$$

In the [[transformer]] base model, $h = 8$ and $d_k = d_v = d_{model}/h = 64$.

The Transformer uses it in three places: self-attention in the encoder, masked
self-attention in the decoder, and decoder-to-encoder attention.

## Where it came from

Introduced in this vault by [[attention-is-all-you-need|Vaswani 2017]].

## Variants and extensions

None in the vault yet. _(background, not from a paper in this vault: later
work shares keys and values across heads to shrink the inference cache;
worth fetching when you get to inference efficiency.)_

## Evidence

- [[attention-is-all-you-need|Vaswani 2017]]: a single head scores about 0.9
  BLEU below the best multi-head setting on the En-De dev set, base model,
  same compute. Too many heads also lowers quality.

## Open questions

- What do individual heads actually learn? The paper shows a few attention
  visualisations but no systematic analysis.

## Related

[[scaled-dot-product-attention]] · [[transformer]]
