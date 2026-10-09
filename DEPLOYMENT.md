# Deployment guide

## 1. Create the GitHub repository

Create a public repository, for example `bestwork-knowledge-library`, under the appropriate BestWork organization or account. Do not initialize it with a README because this checkout already contains one.

Add the remote and push:

```bash
git remote add origin https://github.com/OWNER/bestwork-knowledge-library.git
git push -u origin main
```

## 2. Enable GitHub Pages

In the GitHub repository:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions**.
3. Open the **Actions** tab and verify that `Deploy GitHub Pages` succeeds.

The workflow in `.github/workflows/pages.yml` builds Jekyll, uploads the Pages artifact, and deploys it.

## 3. Configure the permanent URL

When the permanent URL is known, set these values in `_config.yml`:

```yaml
url: "https://library.example.com"
baseurl: ""
repository: "OWNER/bestwork-knowledge-library"
```

For a project site without a custom domain, use:

```yaml
url: "https://OWNER.github.io"
baseurl: "/bestwork-knowledge-library"
repository: "OWNER/bestwork-knowledge-library"
```

Commit and push the configuration change before submitting the sitemap.

## 4. Optional custom domain

For a subdomain such as `library.example.com`:

1. Verify the domain in the GitHub account or organization.
2. Enter the custom domain under **Settings → Pages**.
3. Create a DNS `CNAME` record from `library` to `OWNER.github.io`.
4. Wait for GitHub's DNS check to succeed.
5. Enable **Enforce HTTPS**.

The Actions deployment does not require a tracked `CNAME` file; configure the custom domain in repository settings.

## 5. Search and AI discovery

After deployment:

1. Confirm that `/robots.txt`, `/sitemap.xml`, `/search.json`, and `/llms.txt` return HTTP 200.
2. Verify the site in Google Search Console and Bing Webmaster Tools.
3. Submit the fully qualified `/sitemap.xml` URL to both services.
4. Inspect several article URLs and request indexing where appropriate.
5. Enable IndexNow separately if fast update notification is required.
6. Confirm that CDN, WAF, or bot controls do not challenge `OAI-SearchBot`.

## 6. Post-launch checks

- Search for a distinctive article title in Google and Bing after indexing begins.
- Test the site at mobile and desktop widths.
- Run Google's Rich Results Test on representative articles.
- Check that canonical links use the permanent domain.
- Check that duplicate source documents have intentional, distinct URLs.
- Review crawler and referral traffic without logging sensitive visitor data.

