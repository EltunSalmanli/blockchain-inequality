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

WINDOW_ORDER = ["1d", "1w", "1m", "3m", "6m", "1y", "all"]
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

fig, ax = plt.subplots(figsize=(9, 5.5))

for token in TOKEN_ORDER:
    subset = data[data["token"] == token].set_index("window")
    y = [subset.loc[w, "gini"] for w in WINDOW_ORDER]
    ax.plot(
        WINDOW_ORDER, y,
        marker=MARKERS[token],
        markersize=7,
        linewidth=2,
        color=COLORS[token],
        label=token,
    )

ax.set_xlabel("Activity window", fontsize=11)
ax.set_ylabel("Gini coefficient", fontsize=11)
ax.set_title(
    "Active-holder Gini coefficient across five Ethereum tokens\n(sent-only definition)",
    fontsize=12, pad=12,
)
ax.set_ylim(0.94, 1.005)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

legend = ax.legend(
    title="Token",
    loc="lower right",
    frameon=True,
    framealpha=0.95,
    fontsize=10,
)
legend.get_title().set_fontsize(10)

ax.text(
    0.02, 0.97,
    "Governance tokens (UNI, AAVE):\nstrong window-sensitivity",
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="top",
    color="#7a1d10",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fdf2f0",
              edgecolor="#c0392b", alpha=0.85),
)
ax.text(
    0.02, 0.78,
    "Stablecoins (DAI, USDC, USDT):\nessentially flat",
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="top",
    color="#0e5a4a",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#eafaf5",
              edgecolor="#16a085", alpha=0.85),
)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "01_gini_vs_window.png", dpi=160, bbox_inches="tight")
