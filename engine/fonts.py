"""Embedded fonts: Inter and JetBrains Mono (SIL OFL 1.1, licenses in engine/fonts/).

Each face is pinned from the variable font to a static instance, subset to the
characters a card actually uses and inlined as WOFF2, so the cards look the same
on every system without loading anything.
"""

import base64
import io
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

DIR = Path(__file__).resolve().parent / "fonts"

# cls (see svg.FONTS) → CSS family and source file. Axis values come from the weight.
FAMILIES = {
    "sans": ("GravisSans", "Inter[opsz,wght].ttf", {"opsz": 32}),
    "mono": ("GravisMono", "JetBrainsMono[wght].ttf", {}),
}


def _woff2(file: str, axes: dict, chars: str) -> str:
    font = TTFont(DIR / file)
    instantiateVariableFont(font, axes, inplace=True)
    options = Options()
    options.flavor = "woff2"
    subsetter = Subsetter(options)
    subsetter.populate(text=chars)
    subsetter.subset(font)
    buffer = io.BytesIO()
    font.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def font_faces(usage: dict[tuple[str, int], str]) -> str:
    """`usage` maps (cls, weight) to the text set in that face; returns @font-face rules."""
    rules = ""
    for (cls, weight), chars in usage.items():
        family, file, axes = FAMILIES[cls]
        data = _woff2(file, {**axes, "wght": weight}, chars)
        rules += (
            f"@font-face{{font-family:{family};font-weight:{weight};font-style:normal;"
            f'src:url(data:font/woff2;base64,{data}) format("woff2")}}'
        )
    return rules
