"""recommend.py — County recommendation system"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def build_county_profiles(master_df, ipc_df):
    features = ["total_rainfall","mean_temp","mean_solar","mean_humidity","dry_days","spi_3"]
    available = [f for f in features if f in master_df.columns]
    profiles = master_df.groupby("county")[available].mean().reset_index()
    ipc_county = ipc_df.groupby("county")["ipc_phase"].agg(lambda x: x.mode()[0]).reset_index()
    profiles = profiles.merge(ipc_county, on="county", how="left")
    profiles["food_security_score"] = (
        (4 - profiles["ipc_phase"].fillna(3)) * 0.5 +
        profiles.get("spi_3", pd.Series(0, index=profiles.index)).fillna(0).clip(-2,2) * 0.3 +
        profiles[available[0]].fillna(0) / 1000 * 0.2
    )
    return profiles

def recommend_similar_counties(profiles, target_county, top_n=5):
    feature_cols = [c for c in profiles.columns if c not in ["county","ipc_phase","food_security_score"]]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(profiles[feature_cols].fillna(0))
    sim = cosine_similarity(X)
    sim_df = pd.DataFrame(sim, index=profiles["county"], columns=profiles["county"])
    if target_county not in sim_df.index:
        return pd.DataFrame()
    return sim_df[target_county].sort_values(ascending=False)[1:top_n+1].reset_index()
