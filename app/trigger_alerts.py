"""
app/trigger_alerts.py
=====================
Checks for counties in drought alert and food security crisis.
Called automatically by the Streamlit app on load.

Usage:
    python app/trigger_alerts.py
"""

import pandas as pd
import os

MASTER_PATH = "data/processed/master_dataset.csv"
IPC_PATH    = "data/processed/ipc_clean.csv"


def get_drought_alerts(threshold=-1.0):
    """Return counties currently in drought alert (SPI-3 < threshold)."""
    if not os.path.exists(MASTER_PATH):
        return []
    master = pd.read_csv(MASTER_PATH)
    if "spi_3" not in master.columns:
        return []
    latest_year = master["year"].max()
    recent = master[master["year"] == latest_year]
    alerts = recent[recent["spi_3"] < threshold]["county"].unique().tolist()
    return sorted(alerts)


def get_crisis_counties():
    """Return counties currently in IPC Phase 3 (Crisis)."""
    if not os.path.exists(IPC_PATH):
        return []
    ipc = pd.read_csv(IPC_PATH)
    if "ipc_phase" not in ipc.columns:
        return []
    crisis = ipc[ipc["ipc_phase"] == 3]["county"].unique().tolist()
    return sorted(crisis)


def run_alerts():
    print("\n" + "="*50)
    print("  KENYA AGRICULTURE — ALERT SYSTEM")
    print("="*50)

    drought  = get_drought_alerts()
    crisis   = get_crisis_counties()

    print(f"\n  🔴 DROUGHT ALERT  ({len(drought)} counties)")
    for c in drought:
        print(f"     - {c}")

    print(f"\n  🔴 FOOD CRISIS    ({len(crisis)} counties, IPC Phase 3)")
    for c in crisis:
        print(f"     - {c}")

    if not drought and not crisis:
        print("  ✅ No active alerts")

    print("="*50 + "\n")
    return {"drought_alerts": drought, "crisis_counties": crisis}


if __name__ == "__main__":
    run_alerts()
