---
title: Transformer
type: entity
kind: model
created: 2026-11-04
updated: 2026-11-04
aliases: [Transformer architecture]
tags: [architecture]
---

# Transformer

## What it is

An encoder-decoder architecture built only from attention and position-wise
feed-forward layers, with no recurrence or convolution.

## Key facts

- Base: 6 encoder and 6 decoder layers, $d_{model} = 512$, 8 heads, about 65M
  parameters ([[attention-is-all-you-need|Vaswani 2017]]).
- Big: $d_{model} = 1024$, 16 heads, about 213M parameters (same paper).

## Why it appears here

The architecture almost every later paper in this vault will build on.

## Mentioned in

- [[attention-is-all-you-need|Vaswani 2017]]
- [[scaled-dot-product-attention]] · [[multi-head-attention]]
