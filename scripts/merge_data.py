"""scripts/merge_data.py — Merge all cleaned datasets into master"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd

def main():
    print("\n" + "="*55)
    print("  STEP 3 — Merging Cleaned Datasets → Master")
    print("="*55)
    nasa  = pd.read_csv("data/processed/nasa_monthly_clean.csv")
    ipc   = pd.read_csv("data/processed/ipc_clean.csv")
    knbs  = pd.read_csv("data/processed/knbs_cpi_structured.csv")

    cpi_cols = ["year","month","overall_cpi","yoy_inflation","maize_grain_kg","sugar_kg"]
    cpi_cols = [c for c in cpi_cols if c in knbs.columns]

    master = nasa.merge(knbs[cpi_cols], on=["year","month"], how="left")

    ipc_county = (ipc.groupby("county")["ipc_phase"]
                  .agg(lambda x: x.mode()[0]).reset_index()
                  .rename(columns={"ipc_phase":"ipc_phase_county"}))
    master = master.merge(ipc_county, on="county", how="left")

    master.to_csv("data/processed/master_dataset.csv", index=False)
    print(f"  ✅ Master dataset: {master.shape[0]:,} rows × {master.shape[1]} columns")
    print(f"     Saved: data/processed/master_dataset.csv")

if __name__ == "__main__":
    main()
