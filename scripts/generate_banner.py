#!/usr/bin/env python3
"""
Generates the profile banner as two theme-aware SVGs from assets/banner.json:
    assets/banner-dark.svg
    assets/banner-light.svg

Usage:
    python scripts/generate_banner.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "assets" / "banner.json"
OUT_DIR = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "frame": "#30363d",
        "prompt": "#58a6ff",
        "text": "#c9d1d9",
        "accent": "#7ee787",
        "dim": "#8b949e",
    },
    "light": {
        "bg": "#ffffff",
        "frame": "#d0d7de",
        "prompt": "#0969da",
        "text": "#24292f",
        "accent": "#1a7f37",
        "dim": "#57606a",
    },
}

WIDTH = 760
LINE_HEIGHT = 26
TOP_PADDING = 56
LEFT_PADDING = 24
CHAR_WIDTH = 9.1  # approx monospace advance at 15px
FONT = "JetBrains Mono, Fira Code, Consolas, monospace"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(colors: dict, cfg: dict) -> str:
    lines = cfg["lines"]
    height = TOP_PADDING + LINE_HEIGHT * len(lines) + 30

    body = []
    y = TOP_PADDING
    for line in lines:
        prompt = line.get("prompt", "")
        text = esc(line["text"])
        color = colors["accent"] if line.get("accent") else colors["text"]
        x = LEFT_PADDING
        if prompt:
            body.append(
                f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="15" '
                f'fill="{colors["prompt"]}">{esc(prompt)}</text>'
            )
            x += (len(prompt) + 1) * CHAR_WIDTH
        body.append(
            f'<text x="{x:.1f}" y="{y}" font-family="{FONT}" font-size="15" '
            f'fill="{color}">{text}</text>'
        )
        y += LINE_HEIGHT

    prompt = cfg["prompt"]
    cursor_x = LEFT_PADDING + (len(prompt) + 1) * CHAR_WIDTH
    body.append(
        f'<text x="{LEFT_PADDING}" y="{y}" font-family="{FONT}" font-size="15" '
        f'fill="{colors["prompt"]}">{esc(prompt)}</text>'
    )
    body.append(
        f'<rect x="{cursor_x:.1f}" y="{y - 14}" width="9" height="16" fill="{colors["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" '
        f'dur="1.1s" repeatCount="indefinite" />'
        f"</rect>"
    )

    dots = "".join(
        f'<circle cx="{24 + i * 18}" cy="22" r="6" fill="{c}"/>'
        for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"])
    )

    return f'''<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.75" y="0.75" width="{WIDTH - 1.5}" height="{height - 1.5}" rx="10" fill="{colors['bg']}" stroke="{colors['frame']}" stroke-width="1.5"/>
  <line x1="0" y1="40" x2="{WIDTH}" y2="40" stroke="{colors['frame']}" stroke-width="1"/>
  {dots}
  <text x="{WIDTH / 2}" y="26" font-family="{FONT}" font-size="12" fill="{colors['dim']}" text-anchor="middle">profile.sh</text>
  {''.join(body)}
</svg>'''


def main():
    cfg = json.loads(CONFIG_PATH.read_text())
    for theme_name, colors in THEMES.items():
        svg = build_svg(colors, cfg)
        out_path = OUT_DIR / f"banner-{theme_name}.svg"
        out_path.write_text(svg)
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
