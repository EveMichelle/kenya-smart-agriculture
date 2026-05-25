"""scripts/train_model3.py — County recommendation system"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.recommend import build_county_profiles, recommend_similar_counties

def main():
    print("\n" + "="*55)
    print("  MODEL 3 — County Recommendation System")
    print("  Algorithm: Cosine Similarity Content-Based Filtering")
    print("  Input    : County + season → ranked counties")
    print("="*55)

    master = pd.read_csv("data/processed/master_dataset.csv")
    ipc    = pd.read_csv("data/processed/ipc_clean.csv")

    profiles = build_county_profiles(master, ipc)
    profiles.to_csv("data/processed/county_profiles.csv", index=False)
    print(f"\n  County profiles built: {len(profiles)} counties")

    print("\n  Sample — Counties similar to Turkana:")
    similar = recommend_similar_counties(profiles, "Turkana", top_n=5)
    print(similar.to_string(index=False))

    print("\n  ✅ Model 3 complete — county profiles saved")

if __name__ == "__main__":
    main()
