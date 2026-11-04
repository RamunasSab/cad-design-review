# GitHub Publishing Guide

## Recommended repository settings

- Repository name: `cad-design-review`
- Visibility: Public
- Description: `Portable AI skill for mechanical design review, tolerances, tolerance stack-ups, and manufacturing DFM.`
- Suggested topics: `agent-skills`, `mechanical-engineering`, `design-for-manufacturing`, `dfm`, `cad`, `tolerances`, `engineering`, `python`
- Default branch: `main`
- Releases: publish a GitHub Release tagged `v1.4.0`

## Publish with Git

From the extracted project directory:

```bash
git init
git add .
git commit -m "Prepare v1.4.0 public release"
git branch -M main
git remote add origin https://github.com/OWNER/cad-design-review.git
git push -u origin main
```

Replace `OWNER` with the GitHub account or organization that owns the repository.

Then create a GitHub Release:

1. Open the repository on GitHub.
2. Select **Releases** → **Draft a new release**.
3. Create a tag named `v1.4.0`.
4. Use the contents of `CHANGELOG.md` as the release notes.
5. Attach `cad-design-review-v1.4.0.zip` if you want to provide a ready-to-download archive.

