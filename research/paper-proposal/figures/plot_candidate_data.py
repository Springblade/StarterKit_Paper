"""Plot only the existing candidate-task inventory, never agent outcomes."""
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "smartkit-task-audit-v0.csv"
rows = list(csv.DictReader(SOURCE.open(encoding="utf-8-sig", newline="")))
inventory = []
for row in rows:
    # Classify from the recorded source surface, not from generated outcomes.
    domain = "Billing" if "/billing/" in row["source_surface"] else "User administration"
    inventory.append({"task_id": row["task_id"], "domain": domain,
                      "origin": row["origin"], "status": row["status"]})
counts = Counter(row["domain"] for row in inventory)
labels = ["Billing", "User administration"]
with plt.rc_context({"font.family": "serif", "font.size": 10,
                     "pdf.fonttype": 42, "svg.fonttype": "none"}):
    fig, ax = plt.subplots(figsize=(5.7, 1.85), layout="constrained")
    bars = ax.barh(labels[::-1], [counts[k] for k in labels[::-1]],
                   color=["#777777", "#0072B2"], height=.48)
    for bar in bars:
        ax.text(bar.get_width()+.12, bar.get_y()+bar.get_height()/2,
                str(int(bar.get_width())), va="center")
    ax.set_xlim(0, max(counts.values())+1)
    ax.set_xlabel("Number of constructed task candidates")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=".9", linewidth=.6)
    fig.savefig(HERE / "candidate-data.pdf")
    fig.savefig(HERE / "candidate-data.svg")
    plt.close(fig)
(HERE / "candidate-data-source.json").write_text(
    json.dumps({"source": "research/smartkit-task-audit-v0.csv",
                "classification": "billing source path versus user administration",
                "records": inventory, "counts": dict(counts)}, indent=2), encoding="utf-8")
