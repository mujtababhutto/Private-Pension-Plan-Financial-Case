"""Build the published exhibits for the private-pension case study."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "assets" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#17324D"
BLUE = "#356B8C"
TEAL = "#3E7C78"
GOLD = "#B58A45"
PALE = "#E8EDF1"
INK = "#1D252C"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.labelsize": 10,
    "axes.edgecolor": "#C7D0D8",
    "axes.linewidth": 0.8,
    "xtick.color": "#56616A",
    "ytick.color": "#56616A",
    "text.color": INK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def pension_gap():
    labels = ["Retirement\nspending", "Statutory\npension", "Private pension\ngap"]
    values = [73157.0, 46155.0, 27003.0]
    colors = [NAVY, PALE, GOLD]
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    bars = ax.bar(labels, values, width=0.58, color=colors, edgecolor=[NAVY, "#9FAAB3", GOLD])
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1600, f"€{value/1000:.1f}k", ha="center", va="bottom", fontweight="bold", color=NAVY)
    ax.plot([0, 2], [73157.0, 27003.0], alpha=0)
    ax.set_title("Projected annual retirement income requirement", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "Age 68, nominal euros", transform=ax.transAxes, color="#65717B")
    ax.set_ylim(0, 80000)
    ax.set_ylabel("Annual amount (€)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E8EDF1", linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "pension-gap.png")


def glide_path():
    ages = np.arange(45, 69)
    equity = np.select(
        [ages <= 50, ages <= 55, ages <= 60, ages <= 65],
        [50, 45, 40, 35],
        default=30,
    )
    gold = np.full_like(ages, 10)
    bonds = 100 - equity - gold
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.stackplot(ages, equity, bonds, gold, labels=["Equities", "Bonds", "Gold"], colors=[BLUE, NAVY, GOLD], alpha=0.96)
    ax.set_title("A gradual de-risking path into retirement", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "Target allocation with annual review and ±5 percentage-point rebalance bands", transform=ax.transAxes, color="#65717B")
    ax.set_xlim(45, 68)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Age")
    ax.set_ylabel("Portfolio weight")
    ax.set_yticks([0, 20, 40, 60, 80, 100], labels=["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="white", alpha=0.35)
    save(fig, "glide-path.png")


def correlations():
    raw = pd.read_csv(DATA / "new_data.csv", na_values=["#N/A N/A", "#N/A", "N/A"])
    raw.columns = [c.strip().replace(" ", "_") for c in raw.columns]
    raw["Dates"] = pd.to_datetime(raw["Dates"], dayfirst=True, errors="coerce")
    selected = {
        "Core_MSCI_World_ETF": "Global equity",
        "Global_Infrastructure_ETF": "Infrastructure",
        "Core_Eur_govt_bond": "Euro government bonds",
        "Eur_Core_Corp_Bond_ETF": "Euro corporate bonds",
        "Invesco_Physical_Gold_ETF": "Gold",
    }
    available = [c for c in selected if c in raw.columns]
    returns = raw[available].apply(pd.to_numeric, errors="coerce").rename(columns=selected)
    corr = returns.corr()

    coverage = []
    for source, label in selected.items():
        if source not in raw.columns:
            continue
        mask = pd.to_numeric(raw[source], errors="coerce").notna() & raw["Dates"].notna()
        dates = raw.loc[mask, "Dates"]
        coverage.append({
            "asset": label,
            "start_date": dates.min().date().isoformat(),
            "end_date": dates.max().date().isoformat(),
            "observations": int(mask.sum()),
        })
    pd.DataFrame(coverage).to_csv(DATA / "market_data_coverage.csv", index=False)
    corr.to_csv(DATA / "asset_correlations.csv")

    fig, ax = plt.subplots(figsize=(8.1, 6.8))
    cmap = sns.diverging_palette(30, 215, s=55, l=48, center="light", as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0, cmap=cmap, square=True,
                linewidths=1, linecolor="white", cbar_kws={"label": "Correlation"}, ax=ax)
    ax.set_title("Diversification across the proposed building blocks", loc="left", pad=18, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=35)
    ax.tick_params(axis="y", rotation=0)
    save(fig, "asset-correlations.png")


def etf_allocation():
    labels = [
        "MSCI World",
        "Euro government bonds",
        "Euro corporate bonds",
        "Global infrastructure",
        "Physical gold",
    ]
    weights = [40, 20, 20, 10, 10]
    colors = [BLUE, NAVY, "#647D91", TEAL, GOLD]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    bars = ax.barh(labels[::-1], weights[::-1], color=colors[::-1], height=0.58)
    for bar, value in zip(bars, weights[::-1]):
        ax.text(value + 0.8, bar.get_y() + bar.get_height() / 2, f"{value}%", va="center", color=NAVY, fontweight="bold")
    ax.set_title("Starting allocation by ETF", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "Age 45 target weights", transform=ax.transAxes, color="#65717B")
    ax.set_xlim(0, 46)
    ax.set_xlabel("Portfolio weight")
    ax.set_xticks([0, 10, 20, 30, 40], labels=["0%", "10%", "20%", "30%", "40%"])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color="#E8EDF1", linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "etf-allocation.png")


def portfolio_projection():
    results = pd.read_csv(ROOT / "results" / "reports" / "simulation_results.csv")
    pre_tax = results["final_value"].astype(float).to_numpy()
    effective_tax_rate = 0.30 * 0.1846 + 0.70 * 0.2638
    after_tax = 250_000 + np.maximum(pre_tax - 250_000, 0) * (1 - effective_tax_rate)

    pre = np.percentile(pre_tax, [10, 50, 90])
    post = np.percentile(after_tax, [10, 50, 90])
    summary = pd.DataFrame({
        "measure": ["10th percentile", "Median", "90th percentile"],
        "pre_tax_eur": np.round(pre, 2),
        "after_tax_eur": np.round(post, 2),
    })
    summary.to_csv(DATA / "portfolio_projection_summary.csv", index=False)

    base_target = 675_070.0
    metrics = pd.DataFrame([{
        "simulation_paths": len(pre_tax),
        "base_target_eur": base_target,
        "pre_tax_base_success_pct": round((pre_tax >= base_target).mean() * 100, 2),
        "after_tax_base_success_pct": round((after_tax >= base_target).mean() * 100, 2),
        "effective_tax_rate_on_gains_pct": round(effective_tax_rate * 100, 2),
    }])
    metrics.to_csv(DATA / "portfolio_projection_metrics.csv", index=False)

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    x = np.array([0, 1])
    for xpos, values, color, label in zip(x, [pre, post], [BLUE, GOLD], ["Before tax", "After simplified tax"]):
        ax.vlines(xpos, values[0] / 1e6, values[2] / 1e6, color=color, linewidth=12, alpha=0.25)
        ax.scatter([xpos] * 3, values / 1e6, s=[70, 120, 70], color=color, edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(xpos + 0.06, values[0] / 1e6, f"10th  €{values[0]/1e6:.2f}m", va="center", color=NAVY)
        ax.text(xpos + 0.06, values[1] / 1e6, f"Median  €{values[1]/1e6:.2f}m", va="center", color=NAVY, fontweight="bold")
        ax.text(xpos + 0.06, values[2] / 1e6, f"90th  €{values[2]/1e6:.2f}m", va="center", color=NAVY)
    ax.axhline(base_target / 1e6, color=TEAL, linestyle="--", linewidth=1.5, label="Base capital target")
    ax.set_title("Range of simulated portfolio values at age 68", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "50,000 historical-distribution paths with annual glide-path rebalancing", transform=ax.transAxes, color="#65717B")
    ax.set_xticks(x, ["Before tax", "After simplified tax"])
    ax.set_ylabel("Portfolio value (€m)")
    ax.set_xlim(-0.25, 1.55)
    ax.set_ylim(0.4, 2.25)
    ax.legend(frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E8EDF1", linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "portfolio-projection.png")


def tax_impact():
    pre_tax = 1_416_687
    effective_tax_rate = 0.30 * 0.1846 + 0.70 * 0.2638
    tax = (pre_tax - 250_000) * effective_tax_rate
    after_tax = pre_tax - tax
    fig, ax = plt.subplots(figsize=(8.6, 4.5))
    labels = ["Median before tax", "Estimated tax on gains", "Median after tax"]
    values = [pre_tax, tax, after_tax]
    colors = [BLUE, "#C7D0D8", GOLD]
    bars = ax.bar(labels, np.array(values) / 1e6, color=colors, width=0.58)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value / 1e6 + 0.04, f"€{value/1e6:.2f}m", ha="center", color=NAVY, fontweight="bold")
    ax.set_title("Tax reduces the median projected value by about €280k", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "Simplified tax at withdrawal, applied only to investment gains", transform=ax.transAxes, color="#65717B")
    ax.set_ylim(0, 1.62)
    ax.set_ylabel("Portfolio value (€m)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E8EDF1", linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "tax-impact.png")


def stagflation_stress():
    labels = ["10th percentile", "Median", "90th percentile"]
    values = np.array([372_628.08, 569_900.10, 1_021_165.90])
    target = 675_070.0
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    bars = ax.bar(labels, values / 1e6, color=["#C7D0D8", GOLD, BLUE], width=0.58)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value / 1e6 + 0.035, f"€{value/1000:,.0f}k", ha="center", color=NAVY, fontweight="bold")
    ax.axhline(target / 1e6, color=TEAL, linestyle="--", linewidth=1.6, label="€675k retirement target")
    ax.set_title("Stagflation puts the median outcome below the target", loc="left", pad=18, fontweight="bold")
    ax.text(0, 1.02, "10,000-path static-allocation stress module", transform=ax.transAxes, color="#65717B")
    ax.set_ylim(0, 1.18)
    ax.set_ylabel("Portfolio value at age 68 (€m)")
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E8EDF1", linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "stagflation-stress.png")


if __name__ == "__main__":
    pension_gap()
    glide_path()
    correlations()
    etf_allocation()
    portfolio_projection()
    tax_impact()
    stagflation_stress()
    print(f"Exhibits written to {OUT}")
