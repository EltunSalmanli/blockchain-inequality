import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
CHARTS_DIR = REPO_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

files = {
    "AAVE": "02_grid_aave.csv",
    "UNI":  "03_grid_uni.csv",
    "DAI":  "04_grid_dai.csv",
    "USDC": "05_grid_usdc.csv",
    "USDT": "06_grid_usdt.csv",
}

frames = [pd.read_csv(DATA_DIR / fname) for fname in files.values()]
data = pd.concat(frames, ignore_index=True)
data = data[data["active_definition"] == "sent_only"]

TOKEN_ORDER = ["UNI", "AAVE", "DAI", "USDC", "USDT"]

WINDOWS = [
    ("1d", "1 day"),
    ("1w", "1 week"),
    ("1m", "1 month"),
    ("3m", "3 months"),
    ("6m", "6 months"),
    ("1y", "1 year"),
]

COLORS = {
    "UNI":  "#c0392b",
    "AAVE": "#e67e22",
    "DAI":  "#2980b9",
    "USDC": "#16a085",
    "USDT": "#27ae60",
}

fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), sharey=True)
axes = axes.flatten()

for i, (window_key, window_label) in enumerate(WINDOWS):
    ax = axes[i]
    subset = data[data["window"] == window_key].set_index("token")
    values = [subset.loc[t, "gini"] for t in TOKEN_ORDER]
    bar_colors = [COLORS[t] for t in TOKEN_ORDER]

    bars = ax.bar(TOKEN_ORDER, values, color=bar_colors, edgecolor="black", linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.0008,
            f"{val:.4f}",
            ha="center", va="bottom",
            fontsize=8.5,
        )

    ax.set_title(f"Window: {window_label}", fontsize=11, pad=8)
    ax.set_ylim(0.94, 1.005)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=9)

    if i % 3 == 0:
        ax.set_ylabel("Gini coefficient", fontsize=10)

fig.suptitle(
    "Active-holder Gini coefficient by token, across six activity windows\n(sent-only definition)",
    fontsize=13, y=1.00,
)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "03_gini_bars_per_window.png", dpi=160, bbox_inches="tight")
