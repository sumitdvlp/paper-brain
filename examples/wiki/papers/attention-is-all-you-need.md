---
title: Attention Is All You Need
type: paper
created: 2026-11-04
updated: 2026-11-04
arxiv: 1706.03762
url: https://arxiv.org/abs/1706.03762
venue: NeurIPS 2017
year: 2017
authors: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin]
status: read
aliases: [Vaswani 2017, 1706.03762, Transformer paper]
tags: [architecture, attention, machine-translation]
---

# Attention Is All You Need

> **TL;DR:** Replaces recurrence in encoder-decoder models with attention
> alone, and reports better translation quality at a fraction of the training
> time.

## Your take

_(example take)_ Recurrence was the bottleneck, not attention: once every
position can look at every other position directly, training parallelises and
translation still gets better. What I would doubt first: the quadratic cost in
sequence length is fine for sentences, but the paper never tests long
documents, which is where that cost would bite.

## Problem

The strongest sequence-to-sequence models of the time were recurrent or
convolutional encoder-decoders with attention added on top. Recurrence
processes tokens one after another, so computation inside a training example
cannot be parallelised, and that gets worse as sequences get longer. Distant
positions are also many steps apart, which makes long-range dependencies
harder to learn.

## Method

The [[transformer|Transformer]] keeps the encoder-decoder shape but builds
both halves from attention and small feed-forward layers only. Each of the six
encoder layers applies [[multi-head-attention]] over the input (self-attention)
followed by a position-wise feed-forward network, each wrapped in a residual
connection and layer normalisation. The six decoder layers add a second
attention block over the encoder output and mask future positions so
generation stays left to right.

The attention operation itself is [[scaled-dot-product-attention]]. Because
nothing in the model is sequential, word order is injected with fixed
sinusoidal [[positional-encoding|positional encodings]] added to the input
embeddings.

Base model sizes: $d_{model} = 512$, feed-forward width 2048, 8 heads with
$d_k = d_v = 64$.

## Key results

| Claim | Number | Benchmark / metric | Condition or caveat |
|---|---|---|---|
| English→German translation | 28.4 BLEU | [[wmt-2014]] En-De, newstest2014 | Transformer (big), single model; reported as more than 2 BLEU above the previous best, ensembles included |
| English→French translation | 41.8 BLEU | [[wmt-2014]] En-Fr, newstest2014 | Transformer (big), single model, 3.5 days on 8 P100 GPUs; figure from the current arXiv version, earlier versions reported 41.0 |
| Training cost, base model | 12 hours | 8 P100 GPUs | 100k steps |
| Training cost, big model | 3.5 days | 8 P100 GPUs | 300k steps |
| Generalises beyond translation | 91.3 F1 | English constituency parsing, WSJ section 23 | 4-layer model trained on WSJ only (about 40K sentences); 92.7 F1 semi-supervised |
| One head is worse than several | about 0.9 BLEU drop | En-De dev set (newstest2013) | single head vs the best multi-head setting, base model, same compute; too many heads also hurt |
| Learned positions match sinusoidal | nearly identical | En-De dev set | base model; sinusoidal kept because it may extrapolate to longer sequences |

## Limitations

**Stated by the authors:** Averaging over attention-weighted positions lowers
effective resolution, which they counter with multiple heads. Handling very
large inputs (images, audio, video) would need attention restricted to a local
neighbourhood, left as future work, as is making generation less sequential.

**Shown elsewhere in this vault:** Nothing yet. This is the first paper here.

## Relation to other papers

- Builds on: [[neural-machine-translation-by-jointly-learning-to-align-and-translate|Bahdanau 2014]] (attention for translation; not in the vault yet)
- Supports: none in the vault yet
- Contradicts: none in the vault yet

## Open questions

- Self-attention costs $O(n^2 \cdot d)$ per layer. The paper argues this is
  cheaper than recurrence when sequence length $n$ is below the representation
  size $d$, which holds for sentences. What happens for long documents?
- Do sinusoidal encodings actually extrapolate to longer sequences, as the
  paper hopes but does not test?

## Links

[[transformer]] · [[scaled-dot-product-attention]] · [[multi-head-attention]] · [[wmt-2014]] · [[positional-encoding]]
