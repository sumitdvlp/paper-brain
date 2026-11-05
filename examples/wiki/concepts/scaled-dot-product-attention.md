---
title: Scaled dot-product attention
type: concept
created: 2026-11-04
updated: 2026-11-04
aliases: [dot-product attention, softmax attention]
tags: [attention]
---

# Scaled dot-product attention

## In one paragraph

Each position asks a question (a query), every position offers a label (a key)
and some content (a value). The query is compared with every key by a dot
product, the scores become weights through a softmax, and the output is the
weighted average of the values. Dividing the scores by the square root of the
key size stops them from growing so large that the softmax saturates.

## How it works

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

[[attention-is-all-you-need|Vaswani 2017]] argues for the scaling rather
than measuring it: if query and key components are independent with mean 0 and
variance 1, their dot product has variance $d_k$. The authors suspect that for
large $d_k$ the scores get large, the softmax pushes almost all weight onto one
position, and gradients become very small.

## Where it came from

Introduced in this vault by [[attention-is-all-you-need|Vaswani 2017]]. The
paper cites earlier work finding that unscaled dot-product attention falls
behind additive attention for large $d_k$, and adds the scaling as its fix.

## Variants and extensions

[[multi-head-attention]] runs several of these in parallel on smaller
projections.

## Evidence

- [[attention-is-all-you-need|Vaswani 2017]]: chosen over additive attention
  because it is faster and more memory-efficient in practice, using optimised
  matrix multiplication.

## Open questions

- The cost is quadratic in sequence length. No paper in the vault yet addresses
  that.

## Related

[[transformer]] · [[multi-head-attention]]
