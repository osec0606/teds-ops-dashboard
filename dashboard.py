"""
Ted's Operations Dashboard
==========================
Analyzes appointment, revenue, and peak-hour data across multiple branches.
Built with Python + pandas + matplotlib.

Author: Osman Ural
Purpose: Portfolio project demonstrating real-world data automation skills
"""

import pandas as pd
import matplotlib.pyplot as plt                
import matplotlib.gridspec as gridspec
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
DATA_FILE = "data/sample_data.csv"
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────
def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["date"])
    print(f"✓ Loaded {len(df)} records from {filepath}")
    return df

# ── ANALYSIS FUNCTIONS ───────────────────────────────────────────────────────
def branch_summary(df):
    """Total appointments and revenue per branch."""
    summary = df.groupby("branch").agg(
        total_appointments=("appointments", "sum"),
        total_revenue=("revenue", "sum"),
        avg_daily_revenue=("revenue", "mean")
    ).round(2)
    summary["revenue_per_appointment"] = (
        summary["total_revenue"] / summary["total_appointments"]
    ).round(2)
    return summary.sort_values("total_revenue", ascending=False)

def peak_hours(df):
    """Find busiest hours across all branches."""
    return df.groupby("hour").agg(
        avg_appointments=("appointments", "mean"),
        avg_revenue=("revenue", "mean")
    ).round(2)

def service_breakdown(df):
    """Revenue contribution by service type."""
    return df.groupby("service_type").agg(
        total_revenue=("revenue", "sum"),
        total_appointments=("appointments", "sum")
    ).sort_values("total_revenue", ascending=False)

def daily_trend(df):
    """Revenue trend over time."""
    return df.groupby("date").agg(
        daily_revenue=("revenue", "sum"),
        daily_appointments=("appointments", "sum")
    )

# ── VISUALIZATION ────────────────────────────────────────────────────────────
def generate_dashboard(df):
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Ted's Operations Dashboard", fontsize=18, fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    # 1. Branch Revenue Bar Chart
    ax1 = fig.add_subplot(gs[0, 0])
    bs = branch_summary(df)
    bars = ax1.bar(bs.index, bs["total_revenue"], color="#4A90D9", edgecolor="white")
    ax1.set_title("Total Revenue by Branch", fontweight="bold")
    ax1.set_ylabel("Revenue (£)")
    ax1.tick_params(axis="x", rotation=45)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 f"£{bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8)

    # 2. Peak Hours Line Chart
    ax2 = fig.add_subplot(gs[0, 1])
    ph = peak_hours(df)
    ax2.plot(ph.index, ph["avg_appointments"], marker="o", color="#E74C3C", linewidth=2)
    ax2.fill_between(ph.index, ph["avg_appointments"], alpha=0.15, color="#E74C3C")
    ax2.set_title("Peak Hours (Avg Appointments)", fontweight="bold")
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Avg Appointments")
    ax2.set_xticks(ph.index)

    # 3. Service Type Pie Chart
    ax3 = fig.add_subplot(gs[0, 2])
    sb = service_breakdown(df)
    colors = ["#2ECC71", "#3498DB", "#9B59B6"]
    ax3.pie(sb["total_revenue"], labels=sb.index, autopct="%1.1f%%",
            colors=colors, startangle=90)
    ax3.set_title("Revenue by Service Type", fontweight="bold")

    # 4. Daily Revenue Trend
    ax4 = fig.add_subplot(gs[1, :2])
    dt = daily_trend(df)
    ax4.plot(dt.index, dt["daily_revenue"], marker="s", color="#F39C12",
             linewidth=2, markersize=6)
    ax4.fill_between(dt.index, dt["daily_revenue"], alpha=0.15, color="#F39C12")
    ax4.set_title("Daily Revenue Trend", fontweight="bold")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Revenue (£)")
    ax4.tick_params(axis="x", rotation=30)

    # 5. Summary KPI Table
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis("off")
    total_rev = df["revenue"].sum()
    total_appts = df["appointments"].sum()
    best_branch = branch_summary(df)["total_revenue"].idxmax()
    peak_hour = peak_hours(df)["avg_appointments"].idxmax()

    kpis = [
        ["Metric", "Value"],
        ["Total Revenue", f"£{total_rev:,}"],
        ["Total Appointments", f"{total_appts:,}"],
        ["Best Branch", best_branch],
        ["Peak Hour", f"{peak_hour}:00"],
        ["Branches Tracked", str(df["branch"].nunique())],
    ]
    table = ax5.table(cellText=kpis[1:], colLabels=kpis[0],
                      cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.6)
    # Style header row
    for j in range(2):
        table[0, j].set_facecolor("#4A90D9")
        table[0, j].set_text_props(color="white", fontweight="bold")
    ax5.set_title("KPI Summary", fontweight="bold", pad=12)

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"dashboard_{timestamp}.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"✓ Dashboard saved → {output_path}")
    plt.show()

# ── REPORT EXPORT ────────────────────────────────────────────────────────────
def export_csv_reports(df):
    branch_summary(df).to_csv(os.path.join(OUTPUT_DIR, "branch_summary.csv"))
    peak_hours(df).to_csv(os.path.join(OUTPUT_DIR, "peak_hours.csv"))
    service_breakdown(df).to_csv(os.path.join(OUTPUT_DIR, "service_breakdown.csv"))
    print("✓ CSV reports exported to /reports/")

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data(DATA_FILE)

    print("\n── Branch Summary ──────────────────────────")
    print(branch_summary(df).to_string())

    print("\n── Peak Hours ──────────────────────────────")
    print(peak_hours(df).to_string())

    print("\n── Service Breakdown ───────────────────────")
    print(service_breakdown(df).to_string())

    export_csv_reports(df)
    generate_dashboard(df)
