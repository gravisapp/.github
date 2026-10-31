# .github

Organization profile for Gravis. GitHub shows [`profile/README.md`](profile/README.md) on the organization page.

## Cards

The images in `profile/assets/` are generated, each in a dark and a light variant
(the README picks one with `prefers-color-scheme`). Python 3.10+, standard library only:

```bash
python -m engine build
```

- `engine/theme.py` — colors and fonts, mirroring the app's design tokens
- `engine/cards.py` — one function per card: hero, chips, dividers, project, roadmap
- `engine/svg.py` — shared SVG helpers

Animations are plain CSS inside the SVG and stop under `prefers-reduced-motion`.
