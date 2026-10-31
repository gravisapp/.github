"""Profile cards. Each function takes a Theme and returns a complete SVG document."""

import math

from .svg import WIDTH as W, document, mono_width, r1, text
from .theme import Theme


# ── hero ──────────────────────────────────────────────────────────────────
# The signature element of the app: a progression ladder whose current step climbs.
def hero(t: Theme) -> str:
    height, steps, x0, x1, y = 300, 10, 64, W - 64, 236
    gap = (x1 - x0) / (steps - 1)
    cycle = 13  # seconds: 10 steps, a hold on the top step, reset
    slot = 100 / cycle  # percent of the cycle per step
    hold_end = 94

    css = ".dot{transform-box:fill-box;transform-origin:center;transform:scale(.55)}"
    dots = counter = ""
    for i in range(steps):
        on = r1(slot * (i + 1))
        off = hold_end if i == steps - 1 else r1(slot * (i + 2))
        passed = "" if i == steps - 1 else f"{off}%,{hold_end}%{{fill:{t.text};transform:scale(.55)}}"
        # dim → accent and large while current → solid once passed → dim again for the next cycle
        css += (
            f"@keyframes d{i}{{0%,{r1(on - 0.5)}%{{fill:{t.text3};transform:scale(.55)}}"
            f"{on}%,{r1(off - 0.5)}%{{fill:{t.accent};transform:scale(1)}}{passed}"
            f"100%{{fill:{t.text3};transform:scale(.55)}}}}"
            f".d{i}{{animation:d{i} {cycle}s linear infinite}}"
        )
        dots += f'<circle class="dot d{i}" cx="{r1(x0 + i * gap)}" cy="{y}" r="8" fill="{t.text3}"/>'

        # Step counter "n/10": one label per value, visible during its slot.
        css += (
            f"@keyframes c{i}{{0%{{opacity:0}}{on}%{{opacity:1}}{off}%,100%{{opacity:0}}}}"
            f".c{i}{{animation:c{i} {cycle}s steps(1,end) infinite;opacity:0}}"
        )
        counter += text(x1, 196, f"{i + 1}/{steps}", cls=f"rnd c{i}", size=22, weight=600, fill=t.text2, anchor="end")

    top = r1(slot * steps)
    css += (
        f"@keyframes up{{0%,{r1(top - 0.5)}%{{opacity:0}}{top}%,92%{{opacity:1}}{hold_end}%,100%{{opacity:0}}}}"
        f".up{{animation:up {cycle}s linear infinite;opacity:0}}"
    )
    body = (
        f'<rect x="0" y="0" width="{W}" height="{height}" rx="24" fill="{t.bg}"/>'
        + text(x0, 74, "OPEN-SOURCE · HOME WORKOUTS", cls="mono", size=13, fill=t.text2, weight=600, ls=3)
        + text(x0 - 4, 148, "Gravis", size=76, weight=700, fill=t.text, ls=-1.5)
        + text(x0, 190, "Bodyweight training that climbs with you — one step at a time.", size=20, fill=t.text2)
        + counter
        + text(x1, 166, "next step unlocked", cls="mono up", size=12, fill=t.success, anchor="end", ls=1)
        + f'<rect x="{x0}" y="{y - 1}" width="{x1 - x0}" height="2" rx="1" fill="{t.line}"/>'
        + dots
    )
    return document(height, "Gravis — open-source home workouts", css, body)


# ── chips ─────────────────────────────────────────────────────────────────
CHIPS = [
    ("platforms", "iOS · Android", True),
    ("stack", "React Native · Expo", False),
    ("data", "offline-first", False),
    ("equipment", "bodyweight", False),
    ("status", "prototype", False),
]


def chips(t: Theme) -> str:
    height, h, gap, size, period = 96, 56, 12, 15, 9
    widths = [max(mono_width(value, size), mono_width(label, 10, 1)) + 36 for label, value, _ in CHIPS]
    x = (W - sum(widths) - gap * (len(CHIPS) - 1)) / 2

    css = "@keyframes press{0%{transform:none}1.5%,5%{transform:translateY(3px)}8%,100%{transform:none}}"
    body = ""
    for i, ((label, value, accent), w) in enumerate(zip(CHIPS, widths)):
        fill = t.accent if accent else t.card
        fg = t.on_accent if accent else t.text
        fg2 = t.on_accent if accent else t.text2
        css += f".k{i}{{animation:press {period}s ease-out {r1(i * 0.9)}s infinite}}"
        body += (
            f'<g class="k{i}"><rect x="{r1(x)}" y="20" width="{r1(w)}" height="{h}" rx="14" fill="{fill}"/>'
            + text(x + 18, 40, label, cls="mono", size=10, fill=fg2, ls=1)
            + text(x + 18, 62, value, cls="mono", size=size, weight=700, fill=fg)
            + "</g>"
        )
        x += w + gap
    title = ", ".join(f"{label}: {value}" for label, value, _ in CHIPS)
    return document(height, title, css, body)


# ── section divider ───────────────────────────────────────────────────────
def divider(t: Theme, index: str, label: str) -> str:
    height, y, pad = 56, 30, 16
    caption = f"{index} · {label}"
    pill_w = mono_width(caption, 13, 3) + 40
    px = (W - pill_w) / 2

    ticks = ""
    for i, x in enumerate(range(pad, W - pad + 1, 12)):
        if px - 8 < x < px + pill_w + 8:
            continue
        major = i % 8 == 0
        ticks += f'<rect x="{x}" y="{y - 6 if major else y - 2.5}" width="1" height="{12 if major else 5}"/>'

    css = (
        f"@keyframes sweep{{0%{{transform:translateX(-260px)}}100%{{transform:translateX({W}px)}}}}"
        ".sw{animation:sweep 7s linear infinite}"
    )
    body = (
        '<defs><linearGradient id="g" x1="0" x2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{height}">'
        f'<rect class="sw" x="0" y="0" width="260" height="{height}" fill="url(#g)"/></mask></defs>'
        f'<g fill="{t.text3}">{ticks}</g>'
        f'<rect x="{pad}" y="{y - 0.5}" width="{r1(px - pad - 8)}" height="1" fill="{t.line}"/>'
        f'<rect x="{r1(px + pill_w + 8)}" y="{y - 0.5}" width="{r1(W - pad - px - pill_w - 8)}" height="1" fill="{t.line}"/>'
        f'<g mask="url(#m)"><g fill="{t.accent}">{ticks}</g>'
        f'<rect x="{pad}" y="{y - 1}" width="{W - pad * 2}" height="2" fill="{t.accent}"/></g>'
        f'<rect x="{r1(px)}" y="{y - 15}" width="{r1(pill_w)}" height="30" rx="15" fill="{t.card}"/>'
        f'<text x="{W / 2}" y="{y + 4.5}" class="mono" font-size="13" font-weight="700" letter-spacing="3" '
        f'text-anchor="middle"><tspan fill="{t.accent}">{index}</tspan><tspan fill="{t.text2}"> · </tspan>'
        f'<tspan fill="{t.text}">{label}</tspan></text>'
    )
    return document(height, caption, css, body)


# ── project card: gravis-mobile ───────────────────────────────────────────
def project_mobile(t: Theme) -> str:
    height, pad = 260, 36
    px, py, pw, ph = W - pad - 150, 24, 150, height - 48
    lines = [
        "The app itself: progression ladders for every movement,",
        "a distraction-free flow mode, rest timer and history.",
        "Runs fully offline — your data stays on the phone.",
    ]

    tags, tx = "", pad
    for tag in ["TypeScript", "Expo Router", "expo-sqlite", "Reanimated"]:
        w = mono_width(tag, 12) + 24
        tags += f'<rect x="{r1(tx)}" y="{height - 64}" width="{r1(w)}" height="28" rx="14" fill="{t.inset}"/>'
        tags += text(tx + 12, height - 45.5, tag, cls="mono", size=12, fill=t.text2)
        tx += w + 8

    # Mini rest screen: a wave three periods wide slides one period under the clip
    # while slowly rising; the digits sit below the wave's highest point.
    wave_y, period, bottom = py + ph * 0.45, pw, py + ph + 60
    points = " ".join(
        f"L {r1(px - period + x)} {r1(wave_y + 7 * math.sin(x / period * 2 * math.pi))}"
        for x in range(0, period * 3 + 1, 6)
    )
    wave = f"M {px - period} {bottom} {points} L {px + period * 2} {bottom} Z"
    digits_y = py + ph * 0.74

    css = (
        f"@keyframes wave{{0%{{transform:translateX(0)}}100%{{transform:translateX({period}px)}}}}"
        ".wv{animation:wave 3.2s linear infinite}"
        "@keyframes rise{0%{transform:translateY(16px)}100%{transform:translateY(-8px)}}"
        ".rs{animation:rise 9s ease-in-out infinite alternate}"
    )
    name_w = mono_width("gravis-mobile", 24)
    body = (
        f'<rect x="0" y="0" width="{W}" height="{height}" rx="24" fill="{t.card}"/>'
        + text(pad, 64, "gravis-mobile", cls="mono", size=24, weight=700, fill=t.text)
        + text(pad + name_w + 14, 64, "iOS · Android", cls="mono", size=12, fill=t.accent, ls=1)
        + "".join(text(pad, 104 + i * 26, line, size=17, fill=t.text2) for i, line in enumerate(lines))
        + tags
        + f'<defs><clipPath id="ph"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22"/></clipPath></defs>'
        + f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22" fill="#000000"/>'
        + f'<g clip-path="url(#ph)"><g class="rs"><path class="wv" d="{wave}" fill="{t.accent}"/></g></g>'
        + f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22" fill="none" stroke="{t.line}" stroke-width="2"/>'
        # Black digits on the accent: white would fail contrast (~2.8:1).
        + text(px + pw / 2, digits_y, "1:24", cls="rnd", size=40, weight=700, fill=t.on_accent, anchor="middle")
        + text(px + pw / 2, digits_y + 22, "rest", cls="mono", size=11, fill=t.on_accent, anchor="middle", ls=2)
    )
    return document(height, "gravis-mobile — the iOS and Android app", css, body)


# ── roadmap ───────────────────────────────────────────────────────────────
ROADMAP = [
    ("MVP", "in progress", ["Exercise ladders", "Flow mode & rest timer", "Offline history & charts"]),
    ("v1.1", "next", ["Apple Health · Health Connect", "Records & measurements", "Reminders"]),
    ("v2", "later", ["Accounts & sync", "Friends & feed", "Widgets & watch"]),
]


def roadmap(t: Theme) -> str:
    height, pad, line_y = 250, 36, 44
    col = (W - pad * 2) / len(ROADMAP)
    css = (
        "@keyframes pulse{0%,100%{transform:scale(1);opacity:.35}50%{transform:scale(2.2);opacity:0}}"
        ".pl{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}"
    )
    body = (
        f'<rect x="0" y="0" width="{W}" height="{height}" rx="24" fill="{t.card}"/>'
        f'<rect x="{pad}" y="{line_y - 1}" width="{W - pad * 2}" height="2" rx="1" fill="{t.line}"/>'
    )
    for i, (name, status, items) in enumerate(ROADMAP):
        x = pad + col * i
        current = i == 0
        if current:
            body += f'<circle class="pl" cx="{r1(x + 8)}" cy="{line_y}" r="8" fill="{t.accent}"/>'
        body += (
            f'<circle cx="{r1(x + 8)}" cy="{line_y}" r="{8 if current else 5}" fill="{t.accent if current else t.text3}"/>'
            + text(x, 98, name, cls="rnd", size=30, weight=700, fill=t.text if current else t.text2)
            + text(x, 122, status.upper(), cls="mono", size=11, fill=t.accent if current else t.text2, ls=2)
            + "".join(
                text(x, 160 + j * 26, item, size=16, fill=t.text if current else t.text2) for j, item in enumerate(items)
            )
        )
    title = "Roadmap: " + ", ".join(f"{name} ({status})" for name, status, _ in ROADMAP)
    return document(height, title, css, body)


CARDS = {
    "hero": hero,
    "chips": chips,
    "div-about": lambda t: divider(t, "01", "ABOUT"),
    "div-projects": lambda t: divider(t, "02", "PROJECTS"),
    "div-roadmap": lambda t: divider(t, "03", "ROADMAP"),
    "project-mobile": project_mobile,
    "roadmap": roadmap,
}
