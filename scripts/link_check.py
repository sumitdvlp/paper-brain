#!/usr/bin/env python3
"""Check a paper vault for broken wikilinks, orphan pages and stubs.

Usage:
    python3 link_check.py /path/to/vault [--json]

No dependencies. Reads only; never modifies the vault.

Adapted from second-brain-os (MIT): https://github.com/undefined-ui/second-brain-os
"""
import argparse
import json
import os
import re
import sys

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
# Hidden folders (.claude, .obsidian, .git, .trash), the page templates and
# the scripts folder hold instructions and tooling, not knowledge, so they are
# never counted as pages. Same for CLAUDE.md and README.md wherever they sit.
SKIP_DIRS = {"node_modules", "raw", "templates", "scripts", "examples", "output"}
SKIP_FILES = {"CLAUDE.md", "README.md"}


def is_page(name):
    return name.endswith(".md") and name not in SKIP_FILES


def prune(dirnames):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]


STUB_WORDS = 40


def collect(vault):
    pages = {}
    for dirpath, dirnames, filenames in os.walk(vault):
        prune(dirnames)
        for name in filenames:
            if not is_page(name):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            pages[path] = text
    return pages


def title_of(path, text):
    stem = os.path.splitext(os.path.basename(path))[0]
    return stem


def aliases_of(text):
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return []
    m2 = re.search(r"^aliases:\s*\[(.*?)\]", m.group(1), re.M)
    if not m2:
        return []
    return [a.strip().strip("\"'") for a in m2.group(1).split(",") if a.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.vault):
        sys.exit(f"not a directory: {args.vault}")

    pages = collect(args.vault)
    names, alias_names = {}, {}
    for path, text in pages.items():
        names[title_of(path, text).lower()] = path
        for a in aliases_of(text):
            alias_names.setdefault(a.lower(), path)

    outbound = {p: set() for p in pages}
    inbound = {p: set() for p in pages}
    broken, by_alias = [], []

    for path, text in pages.items():
        for target in LINK.findall(text):
            key = target.strip().lower()
            # Obsidian resolves links by file name only. A link that matches an
            # alias still counts for the graph, but it is reported so it can be
            # rewritten as [[file-name|Alias]].
            dest = names.get(key) or alias_names.get(key)
            if dest:
                if key not in names:
                    by_alias.append((path, target.strip(), dest))
                if dest != path:
                    outbound[path].add(dest)
                    inbound[dest].add(path)
            else:
                broken.append((path, target.strip()))

    # Only wiki pages can be orphans; project files and logs are entry points.
    def in_wiki(p):
        return os.path.relpath(p, args.vault).split(os.sep)[0] == "wiki"

    orphans = [p for p in pages if in_wiki(p) and not inbound[p]
               and not p.endswith(("index.md", "log.md", "README.md"))]
    stubs = [p for p, t in pages.items() if in_wiki(p) and len(t.split()) < STUB_WORDS
             and not p.endswith(("index.md", "log.md"))]
    links = sum(len(v) for v in outbound.values())

    result = {
        "pages": len(pages),
        "links": links,
        "avg_links_per_page": round(links / len(pages), 2) if pages else 0,
        "broken": [{"page": os.path.relpath(p, args.vault), "target": t} for p, t in broken],
        "alias_links": [{"page": os.path.relpath(p, args.vault), "target": t,
                         "file": os.path.splitext(os.path.basename(d))[0]} for p, t, d in by_alias],
        "orphans": [os.path.relpath(p, args.vault) for p in sorted(orphans)],
        "stubs": [os.path.relpath(p, args.vault) for p in sorted(stubs)],
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"pages: {result['pages']}")
    print(f"links: {result['links']} (avg {result['avg_links_per_page']} per page)")
    print(f"broken links: {len(result['broken'])}")
    for b in result["broken"][:40]:
        print(f"  {b['page']} -> [[{b['target']}]]")
    print(f"alias links (rewrite as [[file|Alias]]): {len(result['alias_links'])}")
    for a in result["alias_links"][:40]:
        print(f"  {a['page']} -> [[{a['target']}]] should be [[{a['file']}|{a['target']}]]")
    print(f"orphans: {len(result['orphans'])}")
    for o in result["orphans"][:40]:
        print(f"  {o}")
    print(f"stubs (<{STUB_WORDS} words): {len(result['stubs'])}")
    for s in result["stubs"][:40]:
        print(f"  {s}")


if __name__ == "__main__":
    main()
