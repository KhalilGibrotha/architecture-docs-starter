#!/usr/bin/env python3
"""
Run Vale against formal documentation in this repository.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
TARGET_DIRS = {"docs", "initiatives", "patterns", "governance", "decisions", "references", "notes"}
SKIP_NAMES = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "CLAUDE.md"}
SKIP_DIRS = {".git", ".github", ".vale", "node_modules", "exports", "archive", "diagrams", "build"}


def formal_markdown_files(root: Path, include_templates: bool) -> list[str]:
    paths: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]

        current = Path(dirpath)
        rel_dir = current.relative_to(root)
        top_level = rel_dir.parts[0] if rel_dir.parts else ""
        if top_level and top_level not in TARGET_DIRS and not (include_templates and top_level == "templates"):
            dirnames[:] = []
            continue

        for filename in sorted(filenames):
            if not filename.endswith(".md") or filename in SKIP_NAMES:
                continue
            path = current / filename
            text = path.read_text(encoding="utf-8")
            if FRONT_MATTER_RE.match(text):
                paths.append(str(path.relative_to(root)))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-exit", action="store_true")
    parser.add_argument("--include-templates", action="store_true")
    parser.add_argument("--include-support-docs", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    cmd = ["vale"]
    if args.no_exit:
        cmd.append("--no-exit")

    if args.include_support_docs:
        targets = sorted(TARGET_DIRS)
        if args.include_templates:
            targets.append("templates")
        cmd.extend(targets)
    else:
        targets = formal_markdown_files(repo_root, args.include_templates)
        if not targets:
            print("No formal markdown documents with front matter were found.", file=sys.stderr)
            return 0
        cmd.extend(targets)

    try:
        result = subprocess.run(cmd, cwd=repo_root)
    except FileNotFoundError:
        print("vale is not installed or not on PATH.", file=sys.stderr)
        return 1

    if result.returncode != 0 and not args.no_exit:
        print("Hint: run 'vale sync' in the repo root if styles are missing.", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
