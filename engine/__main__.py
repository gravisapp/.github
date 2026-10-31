"""Usage: python -m engine build

Writes every card in a dark and a light variant to profile/assets/.
README text lives in profile/README.md; only the images are generated.
"""

import sys
from pathlib import Path

from .cards import CARDS
from .theme import THEMES

OUT = Path(__file__).resolve().parent.parent / "profile" / "assets"


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, render in CARDS.items():
        for mode, theme in THEMES.items():
            (OUT / f"{name}-{mode}.svg").write_text(render(theme), encoding="utf-8", newline="\n")
    print(f"built {len(CARDS) * len(THEMES)} svg files -> {OUT}")


if __name__ == "__main__":
    if sys.argv[1:] != ["build"]:
        sys.exit(__doc__)
    build()
