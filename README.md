# BestWork Knowledge Library

This repository publishes the BestWork document collection as a searchable, accessible GitHub Pages site.

## What is included

- 176 source-derived Markdown documents in the `_articles` collection
- Category landing pages and complete library navigation
- Client-side title, category, and description search
- `Article` JSON-LD and standard SEO metadata
- XML sitemap generation
- Explicit AI-search crawler rules
- `llms.txt` as a supplementary machine-readable index
- Responsive, accessible layouts
- GitHub Actions deployment to GitHub Pages
- A deterministic import and validation workflow

## Before publishing

1. Review the content and rights notice in `LICENSE.md`.
2. Proofread the OCR-derived leadership article and other extraction-sensitive documents.
3. Update `url` and `repository` in `_config.yml` after the GitHub organization, repository name, and final domain are known.
4. Review the GPTBot policy in `robots.txt`. Search access is enabled; model-training access is currently disabled.
5. Run the validator described below.

## Local setup

Ruby/Jekyll is not required to edit content. To preview the complete site locally:

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

## Refreshing the imported library

The import script leaves the original conversion directory untouched:

```powershell
python tools/import_library.py "..\markdown" "."
python tools/validate_repository.py "."
```

Review the resulting diff before committing because import regenerates article front matter, category pages, and `_data/categories.yml`.

## Deployment

See `DEPLOYMENT.md` for repository creation, Pages settings, custom-domain configuration, webmaster registration, and post-launch checks.

## Content corrections

Make corrections in the corresponding `_articles` file and submit a pull request. Preserve the `source_file`, `article_id`, and `permalink` values unless the source identity or URL intentionally changes.

