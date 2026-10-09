# Contributing

## Content changes

- Preserve the meaning and historical context of source material.
- Correct obvious conversion or OCR errors without silently rewriting substantive claims.
- Record material editorial revisions in the pull-request description.
- Preserve `article_id`, `source_file`, and `permalink` unless a deliberate migration is being performed.
- Do not add private, identifying, credential, assessment-response, or confidential company data.

## New documents

Add new source-derived Markdown through `tools/import_library.py` when possible. Each published document must include a title, description, category, stable permalink, source reference, and publisher.

## Validation

Run:

```bash
python tools/validate_repository.py .
```

The GitHub Pages deployment must also complete successfully before merging.

