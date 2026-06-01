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

TOKEN_ORDER = ["UNI", "AAVE", "DAI", "USDC", "USDT"]

COLORS = {
    "UNI":  "#c0392b",
    "AAVE": "#e67e22",
    "DAI":  "#2980b9",
    "USDC": "#16a085",
    "USDT": "#27ae60",
}

MARKERS = {
    "UNI":  "o",
    "AAVE": "s",
    "DAI":  "^",
    "USDC": "D",
    "USDT": "v",
}

pivot = data.pivot_table(
    index=["token", "window"],
    columns="active_definition",
    values="gini",
).reset_index()

fig, ax = plt.subplots(figsize=(7.5, 7.5))

axis_min, axis_max = 0.94, 1.005
ax.plot([axis_min, axis_max], [axis_min, axis_max],
        color="black", linestyle="--", linewidth=1, alpha=0.6,
        label="perfect agreement (y = x)")

for token in TOKEN_ORDER:
    subset = pivot[pivot["token"] == token]
    ax.scatter(
        subset["sent_only"],
        subset["sent_or_received"],
        color=COLORS[token],
        marker=MARKERS[token],
        s=90,
        edgecolor="black",
        linewidth=0.6,
        label=token,
        zorder=3,
    )

ax.set_xlim(axis_min, axis_max)
ax.set_ylim(axis_min, axis_max)
ax.set_aspect("equal")

ax.set_xlabel("Gini under sent-only definition", fontsize=11)
ax.set_ylabel("Gini under sent-or-received definition", fontsize=11)
ax.set_title(
    "Robustness check: two definitions of \"active\" agree closely\n"
    "(35 points: 5 tokens x 7 windows)",
    fontsize=12, pad=12,
)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

legend = ax.legend(
    loc="lower right",
    frameon=True,
    framealpha=0.95,
    fontsize=9.5,
)

ax.text(
    0.03, 0.97,
    "Points on the diagonal mean the two definitions give\n"
    "identical Gini. Points above the diagonal: sent-or-received\n"
    "yields higher Gini. Points below: sent-only yields higher.",
    transform=ax.transAxes,
    fontsize=8.5,
    verticalalignment="top",
    color="#222222",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
              edgecolor="#888888", alpha=0.9),
)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "04_sent_vs_received_scatter.png", dpi=160, bbox_inches="tight")
