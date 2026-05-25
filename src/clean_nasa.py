"""clean_nasa.py — NASA POWER weather data cleaning pipeline"""
import pandas as pd
import numpy as np
from src.constants import SEASONS

def clean_nasa(df: pd.DataFrame) -> pd.DataFrame:
    nasa_cols = ["T2M","T2M_MAX","T2M_MIN","PRECTOTCORR","RH2M","WS2M","ALLSKY_SFC_SW_DWN"]
    df[nasa_cols] = df[nasa_cols].replace(-999.0, np.nan)
    df["date"]   = pd.to_datetime(df["date"], errors="coerce")
    df["year"]   = df["date"].dt.year
    df["month"]  = df["date"].dt.month
    df["season"] = df["month"].map({m: s for s, ms in SEASONS.items() for m in ms})
    return df

def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["county","year","month","season"]).agg(
        total_rainfall=("PRECTOTCORR","sum"),
        mean_temp=("T2M","mean"),
        max_temp=("T2M_MAX","mean"),
        min_temp=("T2M_MIN","mean"),
        mean_humidity=("RH2M","mean"),
        mean_solar=("ALLSKY_SFC_SW_DWN","mean"),
        dry_days=("PRECTOTCORR", lambda x: (x < 1.0).sum()),
    ).reset_index()
