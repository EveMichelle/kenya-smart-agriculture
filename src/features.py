"""
features.py — Feature engineering pipeline
==========================================
Called from notebooks/02_data_cleaning.ipynb after base cleaning.
"""

import pandas as pd
import numpy as np
from src.utils import season_of_date, compute_spi


def engineer_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived weather features to monthly NASA DataFrame.

    New features:
        - temp_range: daily temp variability
        - drought_flag: bool, SPI-3 < -1
        - season_rainfall_rank: rainfall rank within season for that county
        - is_long_rains: bool, month in MAM
        - is_short_rains: bool, month in OND
    """
    df = df.copy()

    if "max_temp" in df.columns and "min_temp" in df.columns:
        df["temp_range"] = df["max_temp"] - df["min_temp"]

    if "spi_3" in df.columns:
        df["drought_flag"] = (df["spi_3"] < -1.0).astype(int)

    if "month" in df.columns:
        df["is_long_rains"]  = df["month"].isin([3, 4, 5]).astype(int)
        df["is_short_rains"] = df["month"].isin([10, 11, 12]).astype(int)

    return df
