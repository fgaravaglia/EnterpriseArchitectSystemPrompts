#!/usr/bin/env python3
"""Heuristic linter for the diagram-marmaid skill.

Usage: python lint_mermaid.py <file.mmd | file.md>
(.md files: every ```mermaid block is checked)

Checks: classDef exported, every flowchart node classed, reserved IDs,
Italian accented chars in labels, unquoted labels, decisions with <2 exits.
It is a heuristic: it catches common mistakes, it does not replace a real render.
"""
import re, sys

RESERVED = {"end", "graph", "subgraph", "class", "classdef", "style", "click", "default"}
ACCENTS = re.compile(r"[àèéìòùÀÈÉÌÒÙ]")
NODE = re.compile(r'^\s*([A-Za-z_][\w]*)\s*(\(\[|\[\(|\(\(|\[|\(|\{)')

def blocks(text, is_md):
    if not is_md:
        return [text]
    return re.findall(r"```mermaid\n(.*?)```", text, re.S)

def lint(code, idx):
    issues = []
    lines = code.strip().splitlines()
    head = next((l.strip() for l in lines if l.strip() and not l.strip().startswith(("%%", "---"))), "")
    kind = head.split()[0] if head else ""
    is_flow = kind in ("flowchart", "graph")
    if kind == "graph":
        issues.append("use 'flowchart' instead of 'graph'")
    has_classdef = any(l.strip().startswith("classDef") for l in lines)
    if kind in ("flowchart", "graph", "stateDiagram-v2") and not has_classdef:
        issues.append("no classDef exported: styles must live in the code")
    if ACCENTS.search(code):
        issues.append("accented (Italian?) characters found: diagram labels must be in English")
    if is_flow:
        defined, unclassed = set(), []
        for l in lines:
            m = NODE.match(l)
            if not m or l.strip().startswith(("subgraph", "classDef", "class ", "%%")):
                continue
            nid = m.group(1)
            defined.add(nid)
            if nid.lower() in RESERVED:
                issues.append(f"reserved word used as node id: '{nid}'")
            if ":::" not in l:
                unclassed.append(nid)
            if m.group(2) in ("[", "(", "{") and '"' not in l:
                issues.append(f"label not double-quoted: '{nid}'")
            if m.group(2) == "{" and ":::decision" not in l:
                issues.append(f"diamond '{nid}' is not class 'decision'")
        if unclassed:
            issues.append("nodes without class: " + ", ".join(unclassed))
        # decision exits
        for nid in [d for d in defined if re.search(rf'^\s*{nid}\s*\{{.*:::decision', code, re.M)]:
            exits = len(re.findall(rf'\b{nid}\s*--(?:>|\s*\w+\s*-->)\s*|\b{nid}\s*-->\|', code))
            exits = len(re.findall(rf'\b{nid}\s*-->\|', code))
            if exits < 2:
                issues.append(f"decision '{nid}' has {exits} labeled exit(s), expected >=2")
    return issues

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    bad = 0
    for i, code in enumerate(blocks(text, path.endswith(".md")), 1):
        for msg in lint(code, i):
            bad += 1
            print(f"[block {i}] {msg}")
    print("OK: no issues found" if not bad else f"{bad} issue(s) found")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
