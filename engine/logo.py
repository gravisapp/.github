"""The Gravis wordmark, read from brand/ so the cards always use the current logo."""

import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "brand" / "gravis-logo-white-readme.svg"
NS = {"svg": "http://www.w3.org/2000/svg"}

# Bounding box of the wordmark inside the 500×500 export canvas: x, y, width, height.
BOX = (56.5, 214.5, 387, 71)


def _paths() -> list[tuple[str, bool, bool]]:
    """(d, is_accent, evenodd) for every path; the accent part is the one not filled white."""
    root = ET.parse(SOURCE).getroot()
    return [
        (p.get("d"), p.get("fill", "").lower() not in ("white", "#fff", "#ffffff"), p.get("fill-rule") == "evenodd")
        for p in root.iterfind(".//svg:path", NS)
    ]


def logo(cx: float, cy: float, width: float, color: str, accent: str) -> str:
    """Wordmark centered at (cx, cy), scaled to `width`; letters in `color`, the arrow-A in `accent`."""
    bx, by, bw, bh = BOX
    scale = width / bw
    tx, ty = cx - width / 2 - bx * scale, cy - bh * scale / 2 - by * scale
    rule = ' fill-rule="evenodd"'
    paths = "".join(
        f'<path d="{d}" fill="{accent if is_accent else color}"{rule if evenodd else ""}/>'
        for d, is_accent, evenodd in _paths()
    )
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">{paths}</g>'
