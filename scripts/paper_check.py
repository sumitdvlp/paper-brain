#!/usr/bin/env python3
"""Paper-specific health checks for a paper-brain vault.

Usage:
    python3 scripts/paper_check.py /path/to/vault [--json]

Checks every page in wiki/papers/ for:
    - missing arxiv, year or status, and status values outside the schema
    - a Key results table that is empty, or rows with no condition
    - an empty Your take section, and whether it is listed in to-explain.md
    - two pages with the same arXiv id
    - papers marked read or deep that are not in the Done section of the queue

No dependencies. Reads only; never modifies the vault.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

STATUSES = {"queued", "skimmed", "read", "deep"}
QUEUE = os.path.join("projects", "paper-reading", "Inputs", "queue.md")
TO_EXPLAIN = os.path.join("projects", "paper-reading", "Feedback", "to-explain.md")
PLACEHOLDER = "_not written yet._"


def frontmatter(text):
    """Parse the simple key: value frontmatter these pages use."""
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    meta = {}
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t", "#")):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        meta[key.strip()] = value
    return meta


def section(text, heading):
    """Return the body of a '## heading' section, without HTML comments."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return None
    return re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()


def result_rows(body):
    """Data rows of the first markdown table in a section."""
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue  # separator row
        rows.append(cells)
    return rows[1:]  # drop the header


def read(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    papers_dir = os.path.join(args.vault, "wiki", "papers")
    if not os.path.isdir(papers_dir):
        sys.exit(f"not a paper vault (no wiki/papers/): {args.vault}")

    queue = read(os.path.join(args.vault, QUEUE))
    done = section(queue, "Done") or ""
    to_explain = read(os.path.join(args.vault, TO_EXPLAIN)).lower()

    problems, statuses, years, ids = [], Counter(), Counter(), {}
    pending_takes, unlisted_takes, no_condition = [], [], 0
    pages = sorted(f for f in os.listdir(papers_dir) if f.endswith(".md"))

    for name in pages:
        slug = name[:-3]
        text = read(os.path.join(papers_dir, name))
        meta = frontmatter(text)
        where = f"wiki/papers/{name}"

        if meta.get("type") != "paper":
            problems.append((where, f"type is '{meta.get('type', '')}', expected 'paper'"))
        for key in ("arxiv", "year", "status"):
            if not meta.get(key):
                problems.append((where, f"missing {key}"))
        status = meta.get("status", "")
        if status:
            statuses[status] += 1
            if status not in STATUSES:
                problems.append((where, f"status '{status}' is not one of {sorted(STATUSES)}"))
        if meta.get("year"):
            years[meta["year"]] += 1
        arxiv = meta.get("arxiv")
        if arxiv:
            if arxiv in ids:
                problems.append((where, f"same arXiv id as {ids[arxiv]}"))
            ids.setdefault(arxiv, where)
            if status in ("read", "deep") and queue and f"arXiv:{arxiv}" not in done:
                problems.append((where, "marked read but not in the Done section of the queue"))

        results = section(text, "Key results")
        if results is None:
            problems.append((where, "no Key results section"))
        else:
            rows = [r for r in result_rows(results) if any(r)]
            if not rows:
                problems.append((where, "Key results table is empty"))
            for r in rows:
                if len(r) < 4 or not r[3]:
                    no_condition += 1
                    problems.append((where, f"result without a condition: {r[0][:60]}"))

        take = section(text, "Your take")
        if take is None or not take or take.lower() == PLACEHOLDER:
            pending_takes.append(where)
            if f"[[{slug}" not in to_explain:
                unlisted_takes.append(where)
                problems.append((where, "take pending but not listed in Feedback/to-explain.md"))

    result = {
        "papers": len(pages),
        "by_status": dict(statuses),
        "by_year": dict(sorted(years.items())),
        "takes_pending": len(pending_takes),
        "results_without_condition": no_condition,
        "problems": [{"page": p, "problem": m} for p, m in problems],
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"papers         {result['papers']}")
    for s in ("queued", "skimmed", "read", "deep"):
        if statuses[s]:
            print(f"  {s:<12} {statuses[s]}")
    if years:
        print("by year        " + ", ".join(f"{y}: {n}" for y, n in sorted(years.items())))
    print(f"takes pending  {len(pending_takes)}")
    print(f"results without a condition  {no_condition}")
    print(f"problems       {len(problems)}")
    for p, m in problems[:60]:
        print(f"  {p}: {m}")


if __name__ == "__main__":
    main()
