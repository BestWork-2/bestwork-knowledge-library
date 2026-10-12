#!/usr/bin/env python3
"""Import the converted BestWork Markdown library into the Jekyll collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path


CATEGORY_DESCRIPTIONS = {
    "AI": "Articles examining behavioral data, people analytics, and artificial intelligence.",
    "Behavioral Data": "Foundational perspectives on behavioral data and its practical applications.",
    "BestWork": "Core explanations of BestWork, its principles, and its applications.",
    "Blog": "The Changing the Game article series.",
    "Career": "Career development, job fit, and training perspectives.",
    "Case Studies": "Examples of behavioral and cognitive data applied to organizational challenges.",
    "Cities": "Workforce data, cities, and resilient labor markets.",
    "Cognitive": "Cognitive abilities, learning, and the different ways people solve problems.",
    "Consulting": "Using evidence and behavioral data in advisory work.",
    "Customer Service": "Customer-centric performance and the people side of service.",
    "Cybersecurity": "The human and behavioral dimensions of cybersecurity.",
    "Entrepreneurs": "Entrepreneurial roles, strengths, and business performance.",
    "Industries / Franchising": "Behavioral-data applications in franchising.",
    "Industries / Recruiting": "Behavioral-data applications in recruiting.",
    "Industries / Staffing": "Behavioral-data applications in staffing.",
    "Job Seekers": "Job agility, career direction, and understanding individual strengths.",
    "Leadership": "Leadership outcomes, strengths, and development.",
    "Legal": "Legal and compliance considerations for assessments and selection.",
    "Miscellaneous": "Cross-disciplinary essays on performance, strategy, and data.",
    "Psychology": "Psychometrics, personality measurement, assessment quality, and interpretation.",
    "Sales": "Sales roles, performance, training, and behavioral strengths.",
    "Screening": "Background screening and evidence-based selection.",
    "Students & College": "College decisions, student strengths, employability, and career direction.",
    "Talent Acquisition": "Selection, hiring, candidate fit, and evidence-based recruiting.",
    "Talent Management": "Performance, innovation, development, and workforce decisions.",
    "Team Engineering": "Team composition, collaboration, and data-informed team performance.",
    "Training": "Training effectiveness aligned with behavioral and cognitive strengths.",
    "Turnover": "Job fit, job design, training, and employee retention.",
    "Veterans": "Recognizing and translating veterans' strengths for civilian work.",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "document"


def display_name(parts: tuple[str, ...]) -> str:
    special = {"AI": "AI", "BESTWORK": "BestWork", "BLOG": "Blog"}
    return " / ".join(special.get(part, part.title()) for part in parts)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def repair_legacy_text(value: str) -> str:
    # Two filenames arrived with an ellipsis decoded through a legacy Mac/PC
    # code page. Normalize that known sequence without rewriting article prose.
    return value.replace("ΓÇª", "…")


def parse_document(path: Path) -> tuple[str, str, str, str, str]:
    text = repair_legacy_text(path.read_text(encoding="utf-8")).replace("\r\n", "\n")
    lines = text.splitlines()
    title = path.stem
    if lines and lines[0].startswith("# "):
        title = lines.pop(0)[2:].replace("\\#", "#").strip()
    while lines and not lines[0].strip():
        lines.pop(0)

    source_file = ""
    source_format = path.suffix.lstrip(".").upper()
    while lines and lines[0].startswith(">"):
        line = lines.pop(0)
        source_match = re.search(r"Converted from `([^`]+)`", line)
        format_match = re.search(r"Source format:\s*(.+)$", line)
        if source_match:
            source_file = source_match.group(1)
        if format_match:
            source_format = format_match.group(1).strip()
    while lines and not lines[0].strip():
        lines.pop(0)
    body = "\n".join(lines).strip() + "\n"

    candidates = re.split(r"\n\s*\n", body)
    description = ""
    for candidate in candidates:
        candidate = re.sub(r"^#{1,6}\s+", "", candidate.strip())
        candidate = re.sub(r"[*_>`]", "", candidate)
        candidate = re.sub(r"\s+", " ", candidate).strip()
        if len(candidate) >= 80 and not candidate.lower().startswith("page "):
            description = candidate
            break
    if not description:
        description = f"An article from the BestWork knowledge library about {title}."
    if len(description) > 220:
        description = description[:217].rsplit(" ", 1)[0] + "..."
    return title, description, source_file, source_format, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    source_root = args.source.resolve()
    repository = args.repository.resolve()
    articles_root = repository / "_articles"
    categories_root = repository / "categories"
    data_root = repository / "_data"

    for directory in (articles_root, categories_root, data_root):
        directory.mkdir(parents=True, exist_ok=True)

    for existing in articles_root.rglob("*.md"):
        existing.unlink()
    for existing in categories_root.glob("*.md"):
        existing.unlink()

    category_counts: Counter[str] = Counter()
    category_records: dict[str, dict[str, str | int]] = {}
    imported = 0

    for source in sorted(source_root.rglob("*.md")):
        relative = source.relative_to(source_root)
        category_parts = relative.parts[:-1]
        category = display_name(category_parts)
        category_slug = "/".join(slugify(part) for part in category_parts)
        title, description, source_file, source_format, body = parse_document(source)
        # Use the repository filename for URL identity so same-title source
        # variants (for example PDF and Pages) remain distinct.
        article_slug = slugify(repair_legacy_text(relative.stem))
        permalink = f"/library/{category_slug}/{article_slug}/"
        article_id = hashlib.sha256(source_file.encode("utf-8")).hexdigest()[:12]
        destination_name = repair_legacy_text(relative.stem) + ".md"
        destination = articles_root.joinpath(*category_parts, destination_name)
        destination.parent.mkdir(parents=True, exist_ok=True)

        front_matter = [
            "---",
            "layout: article",
            f"title: {yaml_string(title)}",
            f"description: {yaml_string(description)}",
            f"category: {yaml_string(category)}",
            f"category_slug: {yaml_string(category_slug)}",
            f"permalink: {yaml_string(permalink)}",
            f"article_id: {yaml_string(article_id)}",
            f"source_file: {yaml_string(source_file)}",
            f"source_format: {yaml_string(source_format)}",
            "publisher: BestWork",
            "published: true",
            "---",
            "",
        ]
        destination.write_text("\n".join(front_matter) + body, encoding="utf-8", newline="\n")
        imported += 1
        category_counts[category] += 1
        category_records[category] = {
            "name": category,
            "slug": category_slug,
            "description": CATEGORY_DESCRIPTIONS.get(
                category, f"BestWork articles about {category.lower()}."
            ),
        }

    records = []
    for category in sorted(category_records):
        record = category_records[category]
        record["count"] = category_counts[category]
        records.append(record)
        page_name = str(record["slug"]).replace("/", "-") + ".md"
        category_page = [
            "---",
            "layout: category",
            f"title: {yaml_string(str(record['name']))}",
            f"description: {yaml_string(str(record['description']))}",
            f"category: {yaml_string(str(record['name']))}",
            f"permalink: {yaml_string('/library/' + str(record['slug']) + '/')}",
            "---",
            "",
        ]
        (categories_root / page_name).write_text(
            "\n".join(category_page), encoding="utf-8", newline="\n"
        )

    yaml_lines = []
    for record in records:
        yaml_lines.extend(
            [
                f"- name: {yaml_string(str(record['name']))}",
                f"  slug: {yaml_string(str(record['slug']))}",
                f"  description: {yaml_string(str(record['description']))}",
                f"  count: {record['count']}",
            ]
        )
    (data_root / "categories.yml").write_text(
        "\n".join(yaml_lines) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Imported {imported} documents across {len(records)} categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
