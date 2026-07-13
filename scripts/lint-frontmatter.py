#!/usr/bin/env python3
"""
Validate YAML front matter in markdown documents.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

APPROVED_DOC_TYPES = {
    "overview",
    "gap-analysis",
    "pattern",
    "checklist",
    "reference",
    "guide",
    "adr",
    "proposal",
    "standard",
    "policy",
    "runbook",
    "request",
    "release-notes",
    "rca",
    "spec",
    "sad",
    "meeting-notes",
}

STANDARD_STATUSES = {"Draft", "In Review", "Accepted", "Retired"}
DECISION_STATUSES = {"Proposed", "Accepted", "Rejected", "Retired"}
INFORMATIONAL_STATUSES = {"Informational"}

DECISION_TYPES = {"adr", "proposal"}
INFORMATIONAL_TYPES = {"meeting-notes"}

REQUIRED_FIELDS_STANDARD = [
    "title",
    "doc_type",
    "domain",
    "department",
    "status",
    "version",
    "date",
    "author",
    "owner",
]
REQUIRED_FIELDS_INFORMATIONAL = ["title", "status", "date", "author"]

SKIP_NAMES = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "CLAUDE.md"}
SKIP_DIRS = {".git", ".vale", "node_modules", ".github", "exports", "archive", "diagrams", "build"}
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class FrontMatterParseError(Exception):
    pass


def extract_front_matter(text: str) -> dict | None:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise FrontMatterParseError(str(exc)) from exc
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise FrontMatterParseError("Front matter must parse as a YAML mapping.")
    return parsed


def valid_statuses_for(doc_type: str) -> set[str]:
    if doc_type in DECISION_TYPES:
        return DECISION_STATUSES
    if doc_type in INFORMATIONAL_TYPES:
        return INFORMATIONAL_STATUSES
    return STANDARD_STATUSES


def validate(front_matter: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    status = str(front_matter.get("status", "")).strip()
    required_fields = (
        REQUIRED_FIELDS_INFORMATIONAL if status == "Informational" else REQUIRED_FIELDS_STANDARD
    )

    for field in required_fields:
        if field not in front_matter or front_matter[field] is None or str(front_matter[field]).strip() == "":
            issues.append(("ERROR", f"Missing required field: '{field}'"))

    doc_type = str(front_matter.get("doc_type", "")).strip()
    if doc_type and doc_type not in APPROVED_DOC_TYPES:
        issues.append(("ERROR", f"Invalid doc_type: '{doc_type}'"))

    if status and doc_type in APPROVED_DOC_TYPES:
        allowed = valid_statuses_for(doc_type)
        if status not in allowed:
            issues.append(("ERROR", f"Invalid status '{status}' for doc_type '{doc_type}'"))

    version = str(front_matter.get("version", "")).strip()
    if version and version != "rolling" and not re.match(r"^\d+\.\d+", version):
        issues.append(("WARNING", f"Version '{version}' does not look like a semver string such as '0.1' or '1.0'"))

    return issues


def scan(root: Path, strict: bool) -> int:
    errors = 0
    warnings = 0
    checked = 0
    skipped = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]

        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            if filename in SKIP_NAMES:
                skipped += 1
                continue

            path = Path(dirpath) / filename
            rel = path.relative_to(root)
            text = path.read_text(encoding="utf-8")

            try:
                front_matter = extract_front_matter(text)
            except FrontMatterParseError as exc:
                print(f"[ERROR] {rel}: malformed front matter: {exc}")
                errors += 1
                checked += 1
                continue

            if front_matter is None:
                skipped += 1
                continue

            checked += 1
            for severity, message in validate(front_matter):
                print(f"[{severity}] {rel}: {message}")
                if severity == "ERROR":
                    errors += 1
                else:
                    warnings += 1

    print(f"\nChecked {checked} file(s), skipped {skipped}. Errors: {errors}, Warnings: {warnings}.")
    if errors or (strict and warnings):
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: path is not a directory: {root}", file=sys.stderr)
        return 1
    return scan(root, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())

