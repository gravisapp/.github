"""Design tokens. Mirror gravis-mobile/src/constants/theme.ts (alpha colors flattened to hex)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    bg: str  # hero background
    card: str  # card surface, must stand out from GitHub's page background
    inset: str  # elements inside a card (tags)
    text: str
    text2: str
    text3: str
    line: str
    accent: str = "#FF6A4D"
    on_accent: str = "#000000"
    success: str = "#34C759"


THEMES = {
    "dark": Theme(
        bg="#000000", card="#1C1C1E", inset="#000000",
        text="#FFFFFF", text2="#999999", text3="#4D4D4D", line="#2C2C2E",
    ),
    # GitHub's light page is white, so light cards use the app's #F5F5F7 background instead of white.
    "light": Theme(
        bg="#F5F5F7", card="#F5F5F7", inset="#FFFFFF",
        text="#000000", text2="#666666", text3="#B3B3B3", line="#E0E0E3",
    ),
}

# GitHub renders SVG through <img>, so only installed system fonts are available.
FONTS = {
    "sans": '-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,Helvetica,Arial,sans-serif',
    "rnd": 'ui-rounded,"SF Pro Rounded",-apple-system,"Segoe UI",Roboto,sans-serif',
    "mono": 'ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace',
}
