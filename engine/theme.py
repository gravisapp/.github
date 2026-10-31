"""Design tokens. Mirror gravis-mobile/src/constants/theme.ts (alpha colors flattened to hex)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    bg: str  # card background, must stand out from GitHub's page background
    text: str
    text2: str
    text3: str
    accent: str = "#FE6A2A"  # brand color from the logo
    phone: str = "#1C1C1E"  # device frame stays dark in both themes
    phone_edge: str = "#3A3A3C"


THEMES = {
    "dark": Theme(bg="#000000", text="#FFFFFF", text2="#999999", text3="#4D4D4D"),
    # GitHub's light page is white, so the light card uses the app's #F5F5F7 background.
    "light": Theme(bg="#F5F5F7", text="#000000", text2="#666666", text3="#B3B3B3"),
}
