import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
CHARTS_DIR = REPO_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_DIR / "10_timeseries_dai.csv")
df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

WINDOW_ORDER = ["1d", "1w", "1m", "1y"]

COLORS = {
    "1d": "#c0392b",
    "1w": "#e67e22",
    "1m": "#2980b9",
    "1y": "#27ae60",
}

LABELS = {
    "1d": "1 day window",
    "1w": "1 week window",
    "1m": "1 month window",
    "1y": "1 year window",
}

fig, ax = plt.subplots(figsize=(11, 6))

for window in WINDOW_ORDER:
    subset = df[df["window"] == window].sort_values("snapshot_date")
    ax.plot(
        subset["snapshot_date"],
        subset["gini"],
        marker="o",
        markersize=5,
        linewidth=1.8,
        color=COLORS[window],
        label=LABELS[window],
    )

ax.set_xlabel("Time (quarterly snapshots)", fontsize=11)
ax.set_ylabel("Gini coefficient", fontsize=11)
ax.set_title(
    "DAI — active-holder Gini coefficient over time\nby activity window",
    fontsize=12, pad=12,
)
ax.set_ylim(0.9965, 1.0005)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))

legend = ax.legend(
    title="Activity window",
    loc="lower right",
    frameon=True,
    framealpha=0.95,
    fontsize=10,
)
legend.get_title().set_fontsize(10)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "10_dai_gini_over_time.png", dpi=160, bbox_inches="tight")
