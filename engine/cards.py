"""Profile cards. Each function takes a Theme and returns a complete SVG document."""

import math

from .fonts import font_faces
from .logo import logo
from .svg import WIDTH as W, document, r1, text
from .theme import Theme

HEADLINE = ["A new way", "to train at home."]
STATUS = ("IN DEVELOPMENT", "iOS & ANDROID")


# ── hero ──────────────────────────────────────────────────────────────────
# An iPhone whose screen fills with water like the app's rest screen. The logo
# sits in the middle; where the water covers it, it turns black along the waterline.
def hero(t: Theme) -> str:
    height = 440
    pw, ph = 204, 408
    px, py = W - 72 - pw, (height - ph) / 2
    bezel = 7
    sx, sy, sw, sh = px + bezel, py + bezel, pw - bezel * 2, ph - bezel * 2
    logo_cy = sy + sh * 0.5

    # Water: a wave three periods wide (slides one period sideways) with a flat body
    # below it; the group moves vertically from below the screen to above the logo.
    period, amp = sw, 7
    crest = " ".join(
        f"L {r1(sx - period + x)} {r1(amp * math.sin(x / period * 2 * math.pi))}"
        for x in range(0, period * 3 + 1, 6)
    )
    wave = f"M {sx - period} {sh + 40} {crest} L {r1(sx + period * 2)} {sh + 40} Z"
    empty, full = sy + sh + amp + 2, sy - amp - 2
    half = logo_cy  # static frame (reduced motion): waterline through the logo

    css = (
        f"@keyframes wave{{0%{{transform:translateX(0)}}100%{{transform:translateX({period}px)}}}}"
        ".wv{animation:wave 3.2s linear infinite}"
        # rise slowly, hold full, drain faster, pause empty
        f"@keyframes rise{{0%{{transform:translateY({empty}px)}}62%,72%{{transform:translateY({full}px)}}"
        f"94%,100%{{transform:translateY({empty}px)}}}}"
        f".rs{{transform:translateY({half}px);animation:rise 12s ease-in-out infinite}}"
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}.bl{animation:blink 2.4s ease-in-out infinite}"
    )

    def water(fill: str) -> str:
        return f'<g class="rs"><path class="wv" d="{wave}" fill="{fill}"/></g>'

    screen_rect = f'x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="34"'
    phone = (
        "<defs>"
        f'<clipPath id="scr"><rect {screen_rect}/></clipPath>'
        f'<mask id="under" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{height}">{water("#fff")}</mask>'
        "</defs>"
        # side buttons
        f'<rect x="{px - 3}" y="{py + 96}" width="3" height="28" rx="1.5" fill="{t.phone_edge}"/>'
        f'<rect x="{px - 3}" y="{py + 136}" width="3" height="48" rx="1.5" fill="{t.phone_edge}"/>'
        f'<rect x="{px + pw}" y="{py + 120}" width="3" height="64" rx="1.5" fill="{t.phone_edge}"/>'
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="41" fill="{t.phone}" stroke="{t.phone_edge}" stroke-width="1.5"/>'
        f'<g clip-path="url(#scr)">'
        f'<rect {screen_rect} fill="#000000"/>'
        + logo(sx + sw / 2, logo_cy, sw * 0.72, "#FFFFFF", t.accent)
        + water(t.accent)
        + f'<g mask="url(#under)">{logo(sx + sw / 2, logo_cy, sw * 0.72, "#000000", "#000000")}</g>'
        + "</g>"
        # Dynamic Island stays on top of the water
        + f'<rect x="{r1(sx + sw / 2 - 30)}" y="{sy + 10}" width="60" height="18" rx="9" fill="#000000"/>'
    )

    x0 = 72
    headline = "".join(
        text(x0, 186 + i * 56, line, size=48, weight=600, fill=t.text, ls=-1.2) for i, line in enumerate(HEADLINE)
    )
    status = (
        f'<circle class="bl" cx="{x0 + 4}" cy="{287}" r="4" fill="{t.accent}"/>'
        f'<text x="{x0 + 18}" y="292" class="mono" font-size="13" font-weight="500" letter-spacing="2.6">'
        f'<tspan fill="{t.text2}">{STATUS[0]}</tspan><tspan fill="{t.text3}"> · {STATUS[1]}</tspan></text>'
    )
    font_css = font_faces({("sans", 600): "".join(HEADLINE), ("mono", 500): " · ".join(STATUS)})

    body = f'<rect x="0" y="0" width="{W}" height="{height}" rx="28" fill="{t.bg}"/>' + headline + status + phone
    title = f"Gravis — {' '.join(HEADLINE)} {STATUS[0].capitalize()} for iOS and Android."
    return document(height, title, font_css, css, body)


CARDS = {"hero": hero}
