#!/usr/bin/env python3
"""Find the shortest paths between two wiki pages through their wikilinks.

Usage:
    python3 scripts/link_path.py . multi-head-attention wmt-2014
    python3 scripts/link_path.py . "Vaswani 2017" kv-cache --max 5

Pages can be named by file name, title or alias (case-insensitive). Links count
in both directions. index.md, log.md and project files are left out, because
every page links to the index and a path through it says nothing.

Prints up to --max shortest paths (default 3). The agent reads the pages along
each path to explain what every hop means. No dependencies; reads only.
"""
import argparse
import difflib
import os
import re
import sys
from collections import deque

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
SKIP_FILES = {"index.md", "log.md", "README.md", "CLAUDE.md"}


def frontmatter_value(text, key):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    m2 = re.search(rf"^{key}:\s*(.*)$", m.group(1), re.M)
    return m2.group(1).strip() if m2 else None


def load(vault):
    wiki = os.path.join(vault, "wiki")
    if not os.path.isdir(wiki):
        sys.exit(f"no wiki/ folder in {vault}")
    pages = {}
    for dirpath, dirnames, filenames in os.walk(wiki):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.endswith(".md") and name not in SKIP_FILES:
                with open(os.path.join(dirpath, name), encoding="utf-8", errors="replace") as fh:
                    pages[name[:-3]] = fh.read()
    return pages


def build(pages):
    names = {}
    for stem, text in pages.items():
        names[stem.lower()] = stem
        title = frontmatter_value(text, "title")
        if title:
            names.setdefault(title.lower(), stem)
        aliases = frontmatter_value(text, "aliases") or ""
        for a in aliases.strip("[]").split(","):
            a = a.strip().strip("\"'")
            if a:
                names.setdefault(a.lower(), stem)
    graph = {stem: set() for stem in pages}
    for stem, text in pages.items():
        for target in LINK.findall(text):
            dest = names.get(target.strip().lower())
            if dest and dest != stem:
                graph[stem].add(dest)
                graph[dest].add(stem)
    return names, graph


def resolve(query, names):
    key = query.strip().lower()
    if key in names:
        return names[key]
    close = difflib.get_close_matches(key, list(names), n=5, cutoff=0.5)
    hint = f" Did you mean: {', '.join(sorted({names[c] for c in close}))}?" if close else ""
    sys.exit(f"no page named '{query}'.{hint}")


def shortest_paths(graph, start, goal, limit, max_hops):
    """All shortest paths (up to limit) via BFS with multiple parents."""
    dist, parents = {start: 0}, {start: []}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal or dist[node] >= max_hops:
            continue
        for nxt in sorted(graph[node]):
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                parents[nxt] = [node]
                queue.append(nxt)
            elif dist[nxt] == dist[node] + 1:
                parents[nxt].append(node)
    if goal not in dist:
        return []
    paths = []

    def walk(node, tail):
        if len(paths) >= limit:
            return
        if node == start:
            paths.append([start] + tail)
            return
        for p in parents[node]:
            walk(p, [node] + tail)

    walk(goal, [])
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--max", type=int, default=3, help="paths to show (default 3)")
    ap.add_argument("--max-hops", type=int, default=6, help="give up beyond this (default 6)")
    args = ap.parse_args()

    pages = load(args.vault)
    names, graph = build(pages)
    a, b = resolve(args.a, names), resolve(args.b, names)
    if a == b:
        sys.exit("both names point at the same page")

    paths = shortest_paths(graph, a, b, args.max, args.max_hops)
    if not paths:
        print(f"no path between {a} and {b} within {args.max_hops} hops")
        print(f"  {a}: {len(graph[a])} neighbours, {b}: {len(graph[b])} neighbours")
        return
    print(f"{len(paths)} shortest path(s), {len(paths[0]) - 1} hop(s):")
    for path in paths:
        print("  " + " -- ".join(f"[[{p}]]" for p in path))


if __name__ == "__main__":
    main()
