"""
Heatmap of active-holder Gini coefficient across tokens and windows.

Reads the 5 grid CSVs from data/, builds a 5x7 matrix of Gini values
(rows = tokens, columns = windows), and plots it as a heatmap.

Run from the repo root:
    python scripts/01_plot_heatmap.py

Output: charts/01_heatmap_sent_only.png and charts/01_heatmap_sent_or_received.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------
# Paths
# ---------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
CHARTS_DIR = REPO_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# Load the five grid CSVs
# ---------------------------------------------------------------
files = {
    "AAVE": "02_grid_aave.csv",
    "UNI":  "03_grid_uni.csv",
    "DAI":  "04_grid_dai.csv",
    "USDC": "05_grid_usdc.csv",
    "USDT": "06_grid_usdt.csv",
}

frames = []
for token, fname in files.items():
    df = pd.read_csv(DATA_DIR / fname)
    frames.append(df)

data = pd.concat(frames, ignore_index=True)

# Fixed column order (chronological)
WINDOW_ORDER = ["1d", "1w", "1m", "3m", "6m", "1y", "all"]
TOKEN_ORDER  = ["UNI", "AAVE", "DAI", "USDC", "USDT"]


def make_heatmap(active_def, outfile):
    """Build a heatmap for one active-definition and save it."""
    subset = data[data["active_definition"] == active_def]
    matrix = (subset
              .pivot(index="token", columns="window", values="gini")
              .reindex(index=TOKEN_ORDER, columns=WINDOW_ORDER))

    fig, ax = plt.subplots(figsize=(9, 5))
    # Tight color range to make tiny differences visible
    vmin, vmax = 0.94, 1.00
    im = ax.imshow(matrix.values, cmap="YlOrRd", vmin=vmin, vmax=vmax, aspect="auto")

    # Tick labels
    ax.set_xticks(np.arange(len(WINDOW_ORDER)))
    ax.set_xticklabels(WINDOW_ORDER)
    ax.set_yticks(np.arange(len(TOKEN_ORDER)))
    ax.set_yticklabels(TOKEN_ORDER)

    # Cell annotations
    for i, token in enumerate(TOKEN_ORDER):
        for j, window in enumerate(WINDOW_ORDER):
            val = matrix.iloc[i, j]
            ax.text(j, i, f"{val:.4f}",
                    ha="center", va="center",
                    color="black" if val < 0.98 else "white",
                    fontsize=9)

    ax.set_xlabel("Activity window")
    ax.set_ylabel("Token")
    ax.set_title(f"Active-holder Gini coefficient ({active_def.replace('_', ' ')})")

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Gini")

    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {outfile}")


make_heatmap("sent_only",        CHARTS_DIR / "01_heatmap_sent_only.png")
make_heatmap("sent_or_received", CHARTS_DIR / "01_heatmap_sent_or_received.png")

print("\nDone. Heatmaps saved in charts/.")
