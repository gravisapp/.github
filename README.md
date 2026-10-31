# .github

Organization profile for Gravis. GitHub shows [`profile/README.md`](profile/README.md) on the organization page.

## Hero card

`profile/assets/hero-{dark,light}.svg` is generated (the README picks one with `prefers-color-scheme`):

```bash
pip install -r requirements.txt   # fonttools, for subsetting the embedded fonts
python -m engine build
```

- `engine/cards.py` — the card: headline, status and the phone filling with water
- `engine/logo.py` — reads the wordmark from `brand/`
- `engine/fonts.py` — embeds Inter and JetBrains Mono (SIL OFL, see `engine/fonts/`), subset to the used glyphs
- `engine/theme.py` — colors, mirroring the app's design tokens

Animations are plain CSS inside the SVG and stop under `prefers-reduced-motion`.
