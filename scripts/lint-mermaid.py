#!/usr/bin/env python3
"""
Preflight Mermaid fences in markdown documents.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
SKIP_DIRS = {".git", ".github", ".vale", "archive", "exports", "build", "diagrams", "node_modules"}
SKIP_NAMES = {"README.md", "CLAUDE.md", "CONTRIBUTING.md", "CHANGELOG.md"}
VALID_STARTERS = (
    "flowchart ",
    "sequenceDiagram",
    "requirementDiagram",
    "stateDiagram-v2",
    "classDiagram",
)


def eligible_markdown_files(root: Path, include_templates: bool) -> list[Path]:
    results: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if path.name in SKIP_NAMES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not include_templates and "templates" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if FRONT_MATTER_RE.match(text):
            results.append(path)
    return results


def lint_file(path: Path, root: Path) -> list[tuple[str, int, str]]:
    issues: list[tuple[str, int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    fence_start = 0
    fence_body: list[str] = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not in_fence and stripped.startswith("``` mermaid"):
            issues.append(("ERROR", idx, "Use '```mermaid' with no space after the opening backticks."))
            continue

        if not in_fence and stripped.startswith("```mermaid"):
            in_fence = True
            fence_start = idx
            fence_body = []
            continue

        if in_fence and stripped == "```":
            content_lines = [item.strip() for item in fence_body if item.strip()]
            if not content_lines:
                issues.append(("ERROR", fence_start, "Mermaid fence is empty."))
            else:
                first = content_lines[0]
                if first.startswith("graph "):
                    issues.append(("ERROR", fence_start, "Use 'flowchart TD/LR' instead of deprecated 'graph TD/LR'."))
                elif not first.startswith(VALID_STARTERS):
                    issues.append(("WARNING", fence_start, "First Mermaid line does not match the preferred diagram starters."))
            in_fence = False
            fence_start = 0
            fence_body = []
            continue

        if in_fence:
            fence_body.append(line)

    if in_fence:
        issues.append(("ERROR", fence_start, "Unclosed Mermaid fence."))

    rel = path.relative_to(root).as_posix()
    return [(severity, line_no, f"{rel}:{line_no}: {message}") for severity, line_no, message in issues]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".")
    parser.add_argument("--include-templates", action="store_true")
    parser.add_argument("--strict-warnings", action="store_true")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    files = eligible_markdown_files(root, args.include_templates)

    errors = 0
    warnings = 0
    for path in files:
        for severity, _, message in lint_file(path, root):
            print(f"[{severity}] {message}")
            if severity == "ERROR":
                errors += 1
            else:
                warnings += 1

    print(f"\nChecked {len(files)} file(s). Errors: {errors}, Warnings: {warnings}.")
    if errors or (args.strict_warnings and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

