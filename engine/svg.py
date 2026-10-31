"""Small SVG building blocks shared by all cards."""

from html import escape

WIDTH = 1000

# Embedded faces first (see fonts.py); system stacks only as a fallback.
FONTS = {
    "sans": 'GravisSans,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif',
    "mono": "GravisMono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
}


def r1(n: float) -> float:
    return round(n, 1)


def document(height: int, title: str, font_css: str, css: str, body: str) -> str:
    fonts = "".join(f".{name}{{font-family:{stack}}}" for name, stack in FONTS.items())
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>"
        f"<style>{font_css}{fonts}{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>"
        f"{body}</svg>"
    )


def text(x, y, s, *, cls="sans", size=15, fill, weight=400, anchor="start", ls=0) -> str:
    """`cls` starts with a font class (sans | mono), optionally followed by animation classes."""
    spacing = f' letter-spacing="{ls}"' if ls else ""
    return (
        f'<text x="{r1(x)}" y="{r1(y)}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{spacing}>{escape(str(s))}</text>'
    )
