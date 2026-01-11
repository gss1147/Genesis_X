# Genesis_X

Static site for **Genesis-X: GPU-Free LLM Injection**.

## Quick Deploy (GitHub Pages via Actions)
1. Commit these files to the repository root on the `main` branch.
2. In GitHub: **Settings → Pages**
   - Source: **GitHub Actions**
3. Push any commit to `main` to deploy.

## URLs
Configured for this repo:
- Repo: https://github.com/gss1147/Genesis_X
- Pages: https://gss1147.github.io/Genesis_X/

If you rename the repo, update:
- `index.html` canonical + OG URLs
- `assets/js/app.js` (CONFIG.canonicalUrl, CONFIG.githubRepo)
- `robots.txt` and `sitemap.xml`

## Local preview
```bash
python -m http.server 8080
```
Open http://localhost:8080
