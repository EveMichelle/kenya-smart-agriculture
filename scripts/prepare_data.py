"""scripts/prepare_data.py — Run full data cleaning pipeline"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.pipeline import run_cleaning_pipeline

def main():
    print("\n" + "="*55)
    print("  STEP 2 — Data Cleaning & Feature Engineering")
    print("="*55)
    run_cleaning_pipeline(save=True)
    print("\n  ✅ All cleaned files saved to data/processed/")

if __name__ == "__main__":
    main()
