# Glam Beauty Aesthetics website

Static website for Glam Beauty Aesthetics, an aesthetics clinic at 28 Barking Road, Canning Town, London E16 1EQ.

## Deploying on Vercel
Import this repository in Vercel with **Framework preset: Other**, no build command, and the output directory left as the project root. `vercel.json` sets clean addresses and caching. `.vercelignore` keeps `_build/` and this README off the live site.

## Updating the site
- **Home page:** edit `index.html`. Prices in its treatment menu are the single source of truth.
- **Treatment pages, privacy policy, sitemap and chat answers** are generated:

  ```bash
  python _build/build.py
  ```

  Treatment page text is in `_build/build.py`, reviews in `_build/reviews.json`, and chat answers in `_build/chat_kb.py`.
- After changing CSS or JavaScript, raise `ASSET_V` in `_build/build.py` and the `?v=` numbers in `index.html` so browsers load the new files.

## Preview locally

```bash
python -m http.server 8765
```

Then open http://localhost:8765.
