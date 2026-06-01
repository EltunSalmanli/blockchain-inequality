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
alltime = data[data["window"] == "all"]

records = []
for token in ["UNI", "AAVE", "DAI", "USDC", "USDT"]:
    sent = alltime[(alltime["token"] == token) & (alltime["active_definition"] == "sent_only")]["active_addresses"].iloc[0]
    received = alltime[(alltime["token"] == token) & (alltime["active_definition"] == "sent_or_received")]["active_addresses"].iloc[0]
    dormant = received - sent
    records.append({
        "token": token,
        "active": sent,
        "dormant": dormant,
        "total": received,
        "dormant_pct": 100.0 * dormant / received,
    })

df = pd.DataFrame(records).sort_values("dormant_pct", ascending=True).reset_index(drop=True)

COLORS = {
    "UNI":  "#c0392b",
    "AAVE": "#e67e22",
    "DAI":  "#2980b9",
    "USDC": "#16a085",
    "USDT": "#27ae60",
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

tokens = df["token"].tolist()
y_pos = range(len(tokens))

active_pct = 100.0 - df["dormant_pct"]
dormant_pct = df["dormant_pct"]

ax1.barh(y_pos, active_pct, color="#d5dbdb", edgecolor="black", linewidth=0.5, label="Active (have sent at least once)")
ax1.barh(y_pos, dormant_pct, left=active_pct,
         color=[COLORS[t] for t in tokens],
         edgecolor="black", linewidth=0.5, label="Dormant (received but never sent)")

for i, (token, pct, dormant_n, total_n) in enumerate(zip(tokens, dormant_pct, df["dormant"], df["total"])):
    ax1.text(active_pct.iloc[i] + pct / 2, i,
             f"{pct:.0f}%",
             ha="center", va="center", fontsize=10, fontweight="bold", color="white")

ax1.set_yticks(y_pos)
ax1.set_yticklabels(tokens, fontsize=11)
ax1.set_xlim(0, 100)
ax1.set_xlabel("Share of all-time recipients (%)", fontsize=11)
ax1.set_title("Dormant tail as percentage of recipients", fontsize=12, pad=10)
ax1.grid(True, axis="x", alpha=0.3, linestyle="--")
ax1.set_axisbelow(True)
ax1.legend(loc="lower right", fontsize=9, framealpha=0.95)

bar_colors = [COLORS[t] for t in tokens]
ax2.barh(y_pos, df["dormant"], color=bar_colors, edgecolor="black", linewidth=0.5)

for i, (n, total) in enumerate(zip(df["dormant"], df["total"])):
    if n > 1_000_000:
        label = f"{n/1_000_000:.2f}M of {total/1_000_000:.2f}M"
    else:
        label = f"{n/1000:.0f}K of {total/1_000_000:.2f}M" if total > 1_000_000 else f"{n/1000:.0f}K of {total/1000:.0f}K"
    ax2.text(n + max(df["dormant"]) * 0.02, i, label,
             va="center", fontsize=9.5)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(tokens, fontsize=11)
ax2.set_xlabel("Number of dormant addresses (absolute)", fontsize=11)
ax2.set_title("Dormant tail in absolute terms", fontsize=12, pad=10)
ax2.grid(True, axis="x", alpha=0.3, linestyle="--")
ax2.set_axisbelow(True)
ax2.set_xlim(0, max(df["dormant"]) * 1.45)

fig.suptitle(
    'The "dormant tail": addresses that received tokens but never moved them\n(all-time data, sorted by dormant percentage)',
    fontsize=13, y=1.02,
)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "05_dormant_tail.png", dpi=160, bbox_inches="tight")
