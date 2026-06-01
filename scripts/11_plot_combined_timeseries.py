import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
CHARTS_DIR = REPO_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

files = {
    "AAVE": "08_timeseries_aave.csv",
    "UNI":  "09_timeseries_uni.csv",
    "DAI":  "10_timeseries_dai.csv",
}

frames = []
for token, fname in files.items():
    df = pd.read_csv(DATA_DIR / fname)
    frames.append(df)
data = pd.concat(frames, ignore_index=True)
data["snapshot_date"] = pd.to_datetime(data["snapshot_date"])

TOKEN_ORDER = ["UNI", "AAVE", "DAI"]

COLORS = {
    "UNI":  "#c0392b",
    "AAVE": "#e67e22",
    "DAI":  "#2980b9",
}

MARKERS = {
    "UNI":  "o",
    "AAVE": "s",
    "DAI":  "^",
}

WINDOWS = [
    ("1d", "1 day",   "11_all_tokens_1d_window.png"),
    ("1w", "1 week",  "12_all_tokens_1w_window.png"),
    ("1m", "1 month", "13_all_tokens_1m_window.png"),
    ("1y", "1 year",  "14_all_tokens_1y_window.png"),
]

for window_key, window_label, outfile in WINDOWS:
    fig, ax = plt.subplots(figsize=(11, 6))

    subset = data[data["window"] == window_key]

    for token in TOKEN_ORDER:
        token_data = subset[subset["token"] == token].sort_values("snapshot_date")
        ax.plot(
            token_data["snapshot_date"],
            token_data["gini"],
            marker=MARKERS[token],
            markersize=6,
            linewidth=2,
            color=COLORS[token],
            label=token,
        )

    ax.set_xlabel("Time (quarterly snapshots)", fontsize=11)
    ax.set_ylabel("Gini coefficient", fontsize=11)
    ax.set_title(
        f"Active-holder Gini coefficient over time — {window_label} activity window\n(three tokens compared)",
        fontsize=12, pad=12,
    )
    ax.set_ylim(0.94, 1.001)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))

    legend = ax.legend(
        title="Token",
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        fontsize=10,
    )
    legend.get_title().set_fontsize(10)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / outfile, dpi=160, bbox_inches="tight")
    plt.close()
