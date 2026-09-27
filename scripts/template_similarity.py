"""Find duplicated Django templates: python scripts/template_similarity.py [--threshold 0.9].

Read-only. Scans ``<app>/templates/**/*.html`` (generated ``*/docs/*`` pages are
excluded) and reports:

* byte-identical groups (same SHA-256), and
* near-identical groups: templates whose line-based ``difflib`` similarity to
  another member is at least ``--threshold``. Byte-identical copies are
  collapsed to one representative before comparison, so a near group lists
  distinct contents only.

Each near group is printed with a unified diff of every member against the
group's first member. ``--json`` emits machine-readable output instead, and
``--basename-stats`` prints how many templates sharing a file name are at least
``--threshold`` similar to a sibling (the audit's "63 of 72 list.html" claim).
"""

import argparse
import difflib
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ("accounts", "characters", "core", "game", "items", "locations", "widgets")


def collect(root=ROOT):
    paths = []
    for app in APPS:
        base = root / app / "templates"
        if base.is_dir():
            paths.extend(p for p in base.rglob("*.html") if "docs" not in p.parts)
    return sorted(paths)


def rel(path, root=ROOT):
    return str(path.relative_to(root))


def identical_groups(paths):
    by_hash = defaultdict(list)
    for path in paths:
        by_hash[hashlib.sha256(path.read_bytes()).hexdigest()].append(path)
    return [group for group in by_hash.values() if len(group) > 1]


class _UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)


def _lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def similarity(a_lines, b_lines):
    return difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False).ratio()


def near_groups(paths, threshold, same_name_only=False):
    """Return (groups, best) where best maps each path to its closest sibling ratio."""
    reps = {}
    for group in identical_groups(paths):
        for dup in group[1:]:
            reps[dup] = group[0]
    distinct = [p for p in paths if p not in reps]
    lines = {p: _lines(p) for p in distinct}
    uf = _UnionFind(distinct)
    best = defaultdict(float)
    for i, a in enumerate(distinct):
        la = lines[a]
        for b in distinct[i + 1 :]:
            if same_name_only and a.name != b.name:
                continue
            lb = lines[b]
            if not la or not lb:
                continue
            shorter, longer = sorted((len(la), len(lb)))
            if 2 * shorter / (shorter + longer) < threshold:
                continue
            matcher = difflib.SequenceMatcher(None, la, lb, autojunk=False)
            if matcher.real_quick_ratio() < threshold or matcher.quick_ratio() < threshold:
                continue
            ratio = matcher.ratio()
            best[a] = max(best[a], ratio)
            best[b] = max(best[b], ratio)
            if ratio >= threshold:
                uf.union(a, b)
    members = defaultdict(list)
    for path in distinct:
        members[uf.find(path)].append(path)
    groups = [sorted(group) for group in members.values() if len(group) > 1]
    groups.sort(key=lambda group: (-len(group), rel(group[0])))
    for dup, rep in reps.items():
        best[dup] = max(best[dup], 1.0)
        best[rep] = max(best[rep], 1.0)
    return groups, best, lines


def group_diff(group, lines, context=0):
    head = group[0]
    chunks = []
    for other in group[1:]:
        diff = difflib.unified_diff(
            lines[head], lines[other], rel(head), rel(other), lineterm="", n=context
        )
        chunks.append("\n".join(diff))
    return "\n".join(chunks)


def basename_stats(paths, best, threshold):
    by_name = defaultdict(list)
    for path in paths:
        by_name[path.name].append(path)
    rows = []
    for name, group in by_name.items():
        if len(group) < 2:
            continue
        similar = sum(1 for p in group if best.get(p, 0) >= threshold)
        rows.append((name, len(group), similar))
    rows.sort(key=lambda row: (-row[1], row[0]))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--threshold", type=float, default=0.9)
    parser.add_argument("--same-name-only", action="store_true")
    parser.add_argument("--no-diff", action="store_true", help="omit per-group diffs")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--basename-stats", action="store_true")
    args = parser.parse_args(argv)

    paths = collect()
    identical = sorted(identical_groups(paths), key=lambda g: (-len(g), rel(g[0])))
    near, best, lines = near_groups(paths, args.threshold, args.same_name_only)

    if args.json:
        json.dump(
            {
                "templates": len(paths),
                "threshold": args.threshold,
                "identical": [[rel(p) for p in g] for g in identical],
                "near": [[rel(p) for p in g] for g in near],
            },
            sys.stdout,
            indent=2,
        )
        print()
        return 0

    print(f"Templates scanned: {len(paths)} (generated docs excluded)")
    files = sum(len(g) for g in identical)
    print(f"\n## Byte-identical: {len(identical)} groups, {files} files\n")
    for group in identical:
        print(f"- x{len(group)} {group[0].name}")
        for path in group:
            print(f"    {rel(path)}")

    near_files = sum(len(g) for g in near)
    print(
        f"\n## Near-identical (>= {args.threshold:.2f}): {len(near)} groups, {near_files} files\n"
    )
    for group in near:
        print(f"### x{len(group)} {group[0].name}")
        for path in group:
            print(f"    {rel(path)}  (best sibling {best[path]:.3f})")
        if not args.no_diff:
            print("```diff")
            print(group_diff(group, lines))
            print("```")
        print()

    if args.basename_stats:
        print(f"\n## Same-name templates at least {args.threshold:.2f} similar to a sibling\n")
        for name, total, similar in basename_stats(paths, best, args.threshold):
            print(f"- {name}: {similar} of {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
