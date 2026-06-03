"""scripts/train_recommendation.py
Build county risk intelligence and crop recommendation system.
Run: python scripts/train_recommendation.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.recommend import build_county_profiles, recommend_similar_counties


def main():
    print("\n" + "="*55)
    print("  MODEL 3 — County Risk Intelligence")
    print("  Algorithm: Cosine Similarity Content-Based Filtering")
    print("  Input    : NASA (National Aeronautics and Space Administration)")
    print("             weather + IPC (Integrated Food Security Phase")
    print("             Classification) → ranked counties")
    print("="*55)

    master = pd.read_csv("data/processed/master_dataset.csv")
    ipc    = pd.read_csv("data/processed/ipc_county.csv")

    profiles = build_county_profiles(master, ipc)
    profiles.to_csv("data/processed/county_profiles.csv", index=False)
    print(f"\n  County profiles built: {len(profiles)} counties")

    print("\n  Sample — Counties similar to Turkana:")
    similar = recommend_similar_counties(profiles, "Turkana", top_n=5)
    print(similar.to_string(index=False))

    print("\n  Sample — Counties similar to Kiambu:")
    similar2 = recommend_similar_counties(profiles, "Kiambu", top_n=5)
    print(similar2.to_string(index=False))

    print("\n  ✅ Model 3 complete — county profiles saved")


if __name__ == "__main__":
    main()
