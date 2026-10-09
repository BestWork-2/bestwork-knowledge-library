#!/usr/bin/env python3
"""Static integrity checks for the BestWork Knowledge Library repository."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


REQUIRED_FIELDS = (
    "layout",
    "title",
    "description",
    "category",
    "category_slug",
    "permalink",
    "article_id",
    "source_file",
    "source_format",
    "publisher",
)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    articles = sorted((root / "_articles").rglob("*.md"))
    errors: list[str] = []
    permalinks: list[str] = []
    article_ids: list[str] = []
    source_files: list[str] = []

    if not articles:
        errors.append("No Markdown articles found in _articles.")

    for article in articles:
        text = article.read_text(encoding="utf-8")
        relative = article.relative_to(root).as_posix()
        if "\ufffd" in text or "\x00" in text:
            errors.append(f"{relative}: contains an invalid encoding marker")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append(f"{relative}: missing YAML front matter")
            continue
        front_matter, body = text[4:].split("\n---\n", 1)
        fields = {}
        for line in front_matter.splitlines():
            match = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if match:
                fields[match.group(1)] = match.group(2).strip()
        for field in REQUIRED_FIELDS:
            if not fields.get(field):
                errors.append(f"{relative}: missing {field}")
        if len(body.strip()) < 5:
            errors.append(f"{relative}: article body is unexpectedly short")
        permalinks.append(fields.get("permalink", ""))
        article_ids.append(fields.get("article_id", ""))
        source_files.append(fields.get("source_file", ""))

    for label, values in (
        ("permalink", permalinks),
        ("article_id", article_ids),
        ("source_file", source_files),
    ):
        for value, count in Counter(values).items():
            if value and count > 1:
                errors.append(f"Duplicate {label}: {value} ({count} occurrences)")

    required_paths = (
        "_config.yml",
        "index.md",
        "library.md",
        "robots.txt",
        "search.json",
        "llms.txt",
        "assets/css/style.scss",
        "assets/js/search.js",
        ".github/workflows/pages.yml",
    )
    for path in required_paths:
        if not (root / path).is_file():
            errors.append(f"Missing supporting file: {path}")

    print(f"Articles checked: {len(articles)}")
    print(f"Unique source files: {len(set(source_files))}")
    print(f"Unique permalinks: {len(set(permalinks))}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
