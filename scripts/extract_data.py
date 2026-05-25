"""scripts/extract_data.py — Load all raw datasets and validate them"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.load_data import load_all
from constants import NASA_PATH, IPC_PATH, KNBS_PATH, NEWS_PATH

def main():
    print("\n" + "="*55)
    print("  STEP 1 — Data Extraction & Validation")
    print("="*55)
    data = load_all()
    for name, df in data.items():
        print(f"  {name:<10} : {df.shape[0]:>8,} rows  {df.shape[1]:>3} cols")
    print("\n  ✅ All datasets loaded successfully")
    return data

if __name__ == "__main__":
    main()
