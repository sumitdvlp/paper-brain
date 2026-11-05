# raw/

The archive. Nothing here is edited after it lands.

- `papers/` holds `<arxiv-id>.pdf` and `<arxiv-id>.json` (metadata), written by
  `scripts/arxiv_fetch.py`. You can also drop any PDF here by hand; name it with
  a short slug and the agent will work out the rest.
- `notes/` holds exported highlights and annotations (Zotero, a PDF reader,
  Kindle).

PDFs are ignored by git by default (see `.gitignore`) because arXiv papers can
be fetched again from the metadata. Remove that line if you want them versioned.
