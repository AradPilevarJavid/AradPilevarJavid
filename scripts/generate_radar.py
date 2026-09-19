#!/usr/bin/env python3
"""
Generates radar/spider charts from assets/skills.json and assets/langmix.json:
    assets/radar-dark.svg        assets/radar-light.svg
    assets/radar-langs-dark.svg  assets/radar-langs-light.svg

Usage:
    python scripts/generate_radar.py
"""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {"fg": "#c9d1d9", "grid": "#30363d", "fill": "#58a6ff", "line": "#79c0ff"},
    "light": {"fg": "#24292f", "grid": "#d0d7de", "fill": "#0969da", "line": "#0969da"},
}


def render(config_path: Path, out_prefix: str):
    cfg = json.loads(config_path.read_text())
    labels = [item["label"] for item in cfg["items"]]
    values = [item["value"] for item in cfg["items"]]
    max_val = cfg.get("max", max(values))

    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_closed = values + values[:1]
    angles_closed = angles + angles[:1]

    for theme_name, c in THEMES.items():
        fig = plt.figure(figsize=(4.2, 4.2))
        ax = fig.add_subplot(111, polar=True)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, max_val)

        ax.plot(angles_closed, values_closed, color=c["line"], linewidth=2)
        ax.fill(angles_closed, values_closed, color=c["fill"], alpha=0.25)

        ax.set_xticks(angles)
        ax.set_xticklabels(labels, color=c["fg"], fontsize=10, fontfamily="monospace")
        ax.set_yticks(range(1, int(max_val) + 1))
        ax.set_yticklabels([])
        ax.grid(color=c["grid"], linewidth=0.8)
        ax.spines["polar"].set_color(c["grid"])

        title = cfg.get("title")
        if title:
            ax.set_title(title, color=c["fg"], fontsize=12, fontfamily="monospace", pad=20)

        out_path = ASSETS / f"{out_prefix}-{theme_name}.svg"
        fig.savefig(out_path, format="svg", transparent=True, bbox_inches="tight")
        plt.close(fig)
        print(f"wrote {out_path}")


def main():
    render(ASSETS / "skills.json", "radar")
    render(ASSETS / "langmix.json", "radar-langs")


if __name__ == "__main__":
    main()
