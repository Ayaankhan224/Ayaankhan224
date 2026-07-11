"""
Build a separate terminal-style tech stack window.

The tiles are self-contained SVG shapes/text so the README does not depend on
external icon services that may be blocked inside GitHub-rendered SVG images.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "tech-stack.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 860, 116
PAD = 18
TITLEBAR_H = 30
TILE = 40
GAP = 10

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"

STACK = [
    ("C", "#1f6feb", "#061222"),
    ("C++", "#d81b60", "#190711"),
    ("Java", "#f89820", "#180c04"),
    ("JS", "#f7df1e", "#161400"),
    ("Py", "#3776ab", "#08111f"),
    ("HTML", "#e34f26", "#180905"),
    ("React", "#61dafb", "#07151a"),
    ("CSS", "#663399", "#10081a"),
    ("Sass", "#cc6699", "#180a12"),
    ("TW", "#38bdf8", "#06151a"),
    ("Vite", "#bd34fe", "#12061a"),
    ("Node", "#83cd29", "#0d1805"),
    ("Ex", "#e6edf3", "#101319"),
    ("Mongo", "#47a248", "#071508"),
    ("SQL", "#00758f", "#061217"),
    ("PG", "#4169e1", "#090d1e"),
    ("Ps", "#31a8ff", "#06121b"),
]


def esc(value):
    return html.escape(value)


def reveal(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.12 + i * 0.055
    return (
        f'<g opacity="0" transform="translate(0,4)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    "<defs>"
    f'<linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    "</linearGradient>"
    "</defs>",
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#tbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">ayaan@github: ~$ tech-stack</text>'
)

total_w = len(STACK) * TILE + (len(STACK) - 1) * GAP
x = (W - total_w) / 2
y = TITLEBAR_H + 23

for i, (label, color, tile_bg) in enumerate(STACK):
    tx = x + i * (TILE + GAP)
    font_size = 17 if len(label) <= 3 else 11
    inner = (
        f'<rect x="{tx:.1f}" y="{y}" width="{TILE}" height="{TILE}" rx="7" fill="{tile_bg}" '
        f'stroke="#202938" stroke-width="1"/>'
        f'<text x="{tx + TILE/2:.1f}" y="{y + TILE/2 + font_size/3:.1f}" fill="{color}" '
        f'font-size="{font_size}" font-weight="800" text-anchor="middle">{esc(label)}</text>'
    )
    parts.append(reveal(inner, i))

parts.append(f'<text x="{PAD}" y="{H-15}" fill="{MUTED}" font-size="11">languages · frontend · backend · data · design</text>')
parts.append(f'<text x="{W-PAD}" y="{H-15}" fill="{TEXT}" font-size="11" text-anchor="end">ready</text>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H)
