# examples/

What one `/ingest 1706.03762` produces in an empty vault. Read these pages to
see the format, then ignore the folder: the scripts skip it and the agent is
told never to link to it. Delete it whenever you like.

```
wiki/papers/attention-is-all-you-need.md      the paper page
wiki/concepts/scaled-dot-product-attention.md concept, with the equation
wiki/concepts/multi-head-attention.md         concept
wiki/entities/transformer.md                  model
wiki/entities/wmt-2014.md                     benchmark
```

Things to notice:

- **Your take** is written by the owner, before seeing the agent's summary.
- Every row of **Key results** has a benchmark and a condition.
- Limitations are split into what the authors say and what the vault shows.
- Links to papers not in the vault yet (Bahdanau 2014, positional encoding)
  are written anyway and listed as gaps, so the next fetch has a target.
- Background knowledge on a concept page is marked as such.
