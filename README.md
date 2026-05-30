# The Bonnar Bible (web)

A fast, installable, **offline-capable** reference app for the Scott Bonnar reel‑mower
restoration "Bible" — searchable chapters, mobile‑first, no backend.

## What's here

| File | Purpose |
|------|---------|
| `index.html` | The whole app (HTML + CSS + JS, no build step). |
| `data/data.json` | Extracted content — 433 sections across 391 pages. |
| `extract.py` | Regenerates `data/data.json` from the source PDF (PyMuPDF). |
| `generate_icons.py` | Regenerates the app icons (Pillow). |
| `manifest.webmanifest`, `sw.js`, `icon-*.png` | PWA scaffolding (installable + offline). |
| `.nojekyll` | Tells GitHub Pages to serve files as‑is. |

## Run locally

It must be served over HTTP (the app `fetch`es `data.json`), not opened as a `file://`.

```bash
python -m http.server 8123
# then open http://localhost:8123
```

## Deploy to GitHub Pages

1. Create a new repo on GitHub (e.g. `bonnar-bible`).
2. From this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial Bonnar Bible web app"
   git branch -M main
   git remote add origin https://github.com/<you>/bonnar-bible.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   pick `main` / `/ (root)`, save.
4. Your app appears at `https://<you>.github.io/bonnar-bible/`.

All paths are relative, so it works under that project sub‑path. The `.nojekyll`
file ensures every asset is served untouched.

## Install as an app

Open the Pages URL on your phone, then **Add to Home Screen** (iOS Safari) or
**Install app** (Android Chrome). It launches full‑screen with its own icon and
works offline after the first load.

## Updating content

After editing the source PDF or extraction logic:

```bash
python extract.py          # rebuild data/data.json
```

Then bump the `CACHE` version string in `sw.js` (e.g. `bonnar-bible-v2`) so installed
clients pick up the new data, and redeploy.

## Notes / limitations

- Text is reproduced from the PDF's text layer; diagrams and model photos
  (Annexes 1–2) are images in the source and are not yet included.
- Single‑author workflow: content comes from the PDF, edited via `extract.py`.
