"""visualize.py — EDA plots and maps"""
import matplotlib.pyplot as plt
import seaborn as sns
import os

def save_figure(name, dpi=150):
    os.makedirs("figures", exist_ok=True)
    path = f"figures/{name}.png"
    plt.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.show()
    print(f"Saved: {path}")

def plot_county_rainfall(monthly_df):
    rain = monthly_df.groupby("county")["total_rainfall"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(12,8))
    rain.plot(kind="barh", ax=ax, color="#1565C0", alpha=0.8)
    ax.set_title("Average Monthly Rainfall by County (2000–2023)", fontweight="bold")
    ax.set_xlabel("Mean Monthly Rainfall (mm)")
    save_figure("rainfall_by_county")

def plot_ipc_distribution(ipc_df):
    counts = ipc_df["ipc_phase"].value_counts().sort_index()
    labels = {1:"Phase 1\nMinimal", 2:"Phase 2\nStressed", 3:"Phase 3\nCrisis"}
    fig, ax = plt.subplots(figsize=(7,5))
    colours = ["#66BB6A","#FFA726","#EF5350"]
    counts.plot(kind="bar", ax=ax, color=colours, rot=0)
    ax.set_xticklabels([labels.get(i, str(i)) for i in counts.index])
    ax.set_title("IPC Food Security Phase Distribution (March 2026)", fontweight="bold")
    save_figure("ipc_phase_distribution")
