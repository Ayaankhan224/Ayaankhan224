#!/usr/bin/env python3
"""
Render data/contributions.json as a compact contribution stats chart for the
profile README.
"""
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "stats-chart.svg")

W = 860
H = 286
PAD = 22
TITLEBAR_H = 30

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
GREEN = "#39d353"
GREEN_DARK = "#0e4429"
CYAN = "#22d3ee"
GOLD = "#f2cc60"
ORANGE = "#ffa657"
CARD = "#111722"
STROKE = "#30363d"


def fmt_month(month):
    year, mon = month.split("-")
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return names[int(mon) - 1]


def metric(parts, x, y, w, label, value, note, color):
    parts.append(f'<g opacity="0" transform="translate(0,5)">')
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="72" rx="10" fill="{CARD}" stroke="{STROKE}"/>')
    parts.append(f'<text x="{x + 16}" y="{y + 24}" fill="{MUTED}" font-size="11">{label}</text>')
    parts.append(f'<text x="{x + 16}" y="{y + 50}" fill="{color}" font-size="23" font-weight="800">{value}</text>')
    parts.append(f'<text x="{x + w - 16}" y="{y + 50}" fill="{MUTED}" font-size="11" text-anchor="end">{note}</text>')
    parts.append(f'<animate attributeName="opacity" from="0" to="1" begin="{0.12 + x / 2200:.2f}s" dur="0.4s" fill="freeze"/>')
    parts.append(f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{0.12 + x / 2200:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>')
    parts.append("</g>")


def render(data):
    total = data["total_contributions"]
    active = data["active_days"]
    avg = data["avg_per_active_day"]
    current = data["current_streak"]["length"]
    longest = data["longest_streak"]["length"]
    best = data["best_day"]
    rng = data["range"]
    monthly = data["monthly"]
    max_month = max([m["total"] for m in monthly] + [1])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        "<defs>",
        f'<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#sbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{color}"/>')

    parts.append(f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">ayaan@github: ~/contributions --stats</text>')

    metric_w = 190
    gap = 14
    y = 50
    metric(parts, PAD, y, metric_w, "last year", f"{total:,}", "contributions", GREEN)
    metric(parts, PAD + (metric_w + gap), y, metric_w, "active days", f"{active}", f"{avg}/active day", CYAN)
    metric(parts, PAD + 2 * (metric_w + gap), y, metric_w, "current streak", f"{current}", "days", GOLD)
    metric(parts, PAD + 3 * (metric_w + gap), y, metric_w, "longest streak", f"{longest}", "days", ORANGE)

    chart_x = PAD
    chart_y = 154
    chart_w = W - PAD * 2
    chart_h = 78
    parts.append(f'<text x="{chart_x}" y="{chart_y - 18}" fill="{TEXT}" font-size="13" font-weight="700">monthly contribution pace</text>')
    parts.append(f'<text x="{W - PAD}" y="{chart_y - 18}" fill="{MUTED}" font-size="11" text-anchor="end">{rng["start"]} to {rng["end"]}</text>')
    parts.append(f'<line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="{STROKE}"/>')

    bar_gap = 10
    bar_w = (chart_w - bar_gap * (len(monthly) - 1)) / len(monthly)
    for i, month in enumerate(monthly):
        value = month["total"]
        bh = 4 if value == 0 else max(8, chart_h * value / max_month)
        bx = chart_x + i * (bar_w + bar_gap)
        by = chart_y + chart_h - bh
        fill = GREEN if value else GREEN_DARK
        delay = 0.45 + i * 0.055
        parts.append(f'<g opacity="0" transform="translate(0,6)">')
        parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="5" fill="{fill}"><title>{month["month"]}: {value} contributions</title></rect>')
        parts.append(f'<text x="{bx + bar_w / 2:.1f}" y="{chart_y + chart_h + 18}" fill="{MUTED}" font-size="10" text-anchor="middle">{fmt_month(month["month"])}</text>')
        if value:
            parts.append(f'<text x="{bx + bar_w / 2:.1f}" y="{by - 7:.1f}" fill="{TEXT}" font-size="10" text-anchor="middle">{value}</text>')
        parts.append(f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>')
        parts.append(f'<animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>')
        parts.append("</g>")

    footer_y = 270
    parts.append(f'<text x="{PAD}" y="{footer_y}" fill="{MUTED}" font-size="12">best day <tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')
    parts.append(f'<text x="{W - PAD}" y="{footer_y}" fill="{MUTED}" font-size="12" text-anchor="end">auto-refreshed from public GitHub contribution data</text>')
    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    with open(IN_PATH) as f:
        data = json.load(f)
    with open(OUT_PATH, "w") as f:
        f.write(render(data))
    print(f"wrote {OUT_PATH}")
