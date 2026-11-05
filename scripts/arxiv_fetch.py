#!/usr/bin/env python3
"""Fetch arXiv papers into raw/papers/ and add them to the reading queue.

Usage:
    python3 scripts/arxiv_fetch.py 1706.03762 https://arxiv.org/abs/2205.14135
    python3 scripts/arxiv_fetch.py --no-pdf 2307.03172      # metadata only
    python3 scripts/arxiv_fetch.py --no-queue 2307.03172    # skip the queue

For each id it writes:
    raw/papers/<id>.json   title, authors, abstract, dates, categories, links
    raw/papers/<id>.pdf    the paper (skipped with --no-pdf)

and appends one line to the Inbox section of
projects/paper-reading/Inputs/queue.md.

No dependencies. Run it from the vault root. raw/ is an archive, so files that
already exist are never overwritten. arXiv asks API users to wait about three
seconds between requests; this script does.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query?id_list={id}"
PDF = "https://arxiv.org/pdf/{id}"
ABS = "https://arxiv.org/abs/{id}"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
UA = "paper-brain/1.0 (personal reading vault)"
RAW = os.path.join("raw", "papers")
QUEUE = os.path.join("projects", "paper-reading", "Inputs", "queue.md")
PAUSE = 3.0

# New-style ids (2205.14135, optionally v2) and old-style ids (cs/0112017).
NEW_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
OLD_ID = re.compile(r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?")


def parse_id(text):
    """Return the version-less arXiv id from an id or URL, or None."""
    text = text.strip()
    for pattern in (NEW_ID, OLD_ID):
        m = pattern.search(text)
        if m:
            return m.group(1)
    return None


def file_stem(arxiv_id):
    return arxiv_id.replace("/", "_")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def parse_atom(xml_bytes, arxiv_id):
    """Turn an arXiv API Atom response into a metadata dict, or None."""
    root = ET.fromstring(xml_bytes)
    entry = root.find("a:entry", NS)
    if entry is None:
        return None
    title = clean(entry.findtext("a:title", default="", namespaces=NS))
    entry_id = entry.findtext("a:id", default="", namespaces=NS)
    # The API answers an unknown id with a single entry titled "Error".
    if not title or title.lower() == "error" or "api/errors" in entry_id:
        return None
    version = None
    m = re.search(r"v(\d+)$", entry_id)
    if m:
        version = int(m.group(1))
    primary = entry.find("arxiv:primary_category", NS)
    return {
        "arxiv": arxiv_id,
        "version": version,
        "title": title,
        "authors": [clean(a.findtext("a:name", default="", namespaces=NS))
                    for a in entry.findall("a:author", NS)],
        "abstract": clean(entry.findtext("a:summary", default="", namespaces=NS)),
        "published": entry.findtext("a:published", default="", namespaces=NS)[:10],
        "updated": entry.findtext("a:updated", default="", namespaces=NS)[:10],
        "year": int(entry.findtext("a:published", default="0000", namespaces=NS)[:4] or 0),
        "primary_category": primary.get("term") if primary is not None else None,
        "categories": [c.get("term") for c in entry.findall("a:category", NS)],
        "comment": clean(entry.findtext("arxiv:comment", default="", namespaces=NS)) or None,
        "journal_ref": clean(entry.findtext("arxiv:journal_ref", default="", namespaces=NS)) or None,
        "doi": clean(entry.findtext("arxiv:doi", default="", namespaces=NS)) or None,
        "url": ABS.format(id=arxiv_id),
        "pdf_url": PDF.format(id=arxiv_id),
    }


def add_to_queue(queue_path, meta, today):
    """Append a line to the Inbox section, unless the id is already queued."""
    if not os.path.exists(queue_path):
        print(f"  queue not found at {queue_path}, skipping")
        return False
    with open(queue_path, encoding="utf-8") as fh:
        text = fh.read()
    if f"arXiv:{meta['arxiv']} " in text or f"arXiv:{meta['arxiv']}\n" in text:
        print("  already in the queue")
        return False
    lines = text.rstrip("\n").split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().lower() == "## inbox")
    except StopIteration:
        lines += ["", "## Inbox", ""]
        start = len(lines) - 2
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    section = [l for l in lines[start + 1:end] if l.strip() != "_Empty._"]
    while section and not section[-1].strip():
        section.pop()
    item = f"- **{meta['title']}** · arXiv:{meta['arxiv']} · untriaged · added {today}"
    if not section or not section[-1].lstrip().startswith("- "):
        section.append("")  # blank line between the section text and the list
    section.append(item)
    lines = lines[:start + 1] + section + [""] + lines[end:]
    text = "\n".join(lines).rstrip("\n") + "\n"
    text = re.sub(r"^updated: .*$", f"updated: {today}", text, count=1, flags=re.M)
    with open(queue_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return True


def fetch_one(arxiv_id, want_pdf, want_queue, today):
    stem = file_stem(arxiv_id)
    meta_path = os.path.join(RAW, stem + ".json")
    pdf_path = os.path.join(RAW, stem + ".pdf")
    print(f"{arxiv_id}")

    meta = None
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
        print("  metadata already in raw/, not overwriting")
    else:
        try:
            meta = parse_atom(get(API.format(id=arxiv_id)), arxiv_id)
        except (urllib.error.URLError, ET.ParseError, TimeoutError) as exc:
            print(f"  metadata lookup failed: {exc}")
        if meta is None:
            print("  no metadata from the API; writing a minimal record")
            meta = {"arxiv": arxiv_id, "title": f"arXiv {arxiv_id}",
                    "url": ABS.format(id=arxiv_id), "pdf_url": PDF.format(id=arxiv_id),
                    "note": "API lookup failed; the agent should fill this in from the PDF"}
        meta["fetched"] = today
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"  {meta['title']}")
        time.sleep(PAUSE)

    if want_pdf:
        if os.path.exists(pdf_path):
            print("  pdf already in raw/, not overwriting")
        else:
            try:
                data = get(PDF.format(id=arxiv_id))
                if not data.startswith(b"%PDF"):
                    raise ValueError("response is not a PDF")
                with open(pdf_path, "wb") as fh:
                    fh.write(data)
                print(f"  pdf saved ({len(data) // 1024} KB)")
            except (urllib.error.URLError, ValueError, TimeoutError) as exc:
                print(f"  pdf download failed: {exc}")
            time.sleep(PAUSE)

    if want_queue and add_to_queue(QUEUE, meta, today):
        print("  added to queue Inbox")
    return meta


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="+", help="arXiv ids or URLs")
    ap.add_argument("--no-pdf", action="store_true", help="fetch metadata only")
    ap.add_argument("--no-queue", action="store_true", help="do not touch the queue")
    args = ap.parse_args()

    if not os.path.isdir(RAW):
        sys.exit(f"{RAW}/ not found: run this from the vault root")

    today = dt.date.today().isoformat()
    ids, bad = [], []
    for raw_id in args.ids:
        parsed = parse_id(raw_id)
        (ids if parsed else bad).append(parsed or raw_id)
    for b in bad:
        print(f"not an arXiv id or URL: {b}")

    fetched = [fetch_one(i, not args.no_pdf, not args.no_queue, today) for i in dict.fromkeys(ids)]
    print(f"\nfetched {len(fetched)} paper(s) into {RAW}/")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
