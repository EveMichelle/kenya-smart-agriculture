"""
utils.py — Shared constants, county mappings, and utility functions
===================================================================
Import in any notebook or module:
    from src.utils import COUNTIES, COUNTY_MAP, season_of_date
"""

import pandas as pd
import numpy as np
from typing import Optional

# ── All 47 Kenya Counties with centroid coordinates ───────────────────────────
COUNTIES = {
    "Mombasa":         {"lat": -4.0435, "lon": 39.6682, "region": "Coast"},
    "Kwale":           {"lat": -4.1817, "lon": 39.4606, "region": "Coast"},
    "Kilifi":          {"lat": -3.5107, "lon": 39.9093, "region": "Coast"},
    "Tana River":      {"lat": -1.5000, "lon": 39.5000, "region": "Coast"},
    "Lamu":            {"lat": -2.2686, "lon": 40.9020, "region": "Coast"},
    "Taita Taveta":    {"lat": -3.3167, "lon": 38.4833, "region": "Coast"},
    "Garissa":         {"lat": -0.4536, "lon": 39.6401, "region": "North Eastern"},
    "Wajir":           {"lat":  1.7471, "lon": 40.0573, "region": "North Eastern"},
    "Mandera":         {"lat":  3.9373, "lon": 41.8570, "region": "North Eastern"},
    "Marsabit":        {"lat":  2.3284, "lon": 37.9899, "region": "Eastern"},
    "Isiolo":          {"lat":  0.3556, "lon": 37.5820, "region": "Eastern"},
    "Meru":            {"lat":  0.0467, "lon": 37.6490, "region": "Eastern"},
    "Tharaka Nithi":   {"lat": -0.2000, "lon": 37.8000, "region": "Eastern"},
    "Embu":            {"lat": -0.5357, "lon": 37.4580, "region": "Eastern"},
    "Kitui":           {"lat": -1.3671, "lon": 38.0108, "region": "Eastern"},
    "Machakos":        {"lat": -1.5177, "lon": 37.2634, "region": "Eastern"},
    "Makueni":         {"lat": -2.2558, "lon": 37.6242, "region": "Eastern"},
    "Nyandarua":       {"lat": -0.1833, "lon": 36.5833, "region": "Central"},
    "Nyeri":           {"lat": -0.4167, "lon": 36.9500, "region": "Central"},
    "Kirinyaga":       {"lat": -0.6600, "lon": 37.3800, "region": "Central"},
    "Muranga":         {"lat": -0.7167, "lon": 37.1500, "region": "Central"},
    "Kiambu":          {"lat": -1.0314, "lon": 36.8063, "region": "Central"},
    "Turkana":         {"lat":  3.1162, "lon": 35.5960, "region": "Rift Valley"},
    "West Pokot":      {"lat":  1.6210, "lon": 35.1170, "region": "Rift Valley"},
    "Samburu":         {"lat":  1.2166, "lon": 36.9000, "region": "Rift Valley"},
    "Trans Nzoia":     {"lat":  1.0566, "lon": 35.0000, "region": "Rift Valley"},
    "Uasin Gishu":     {"lat":  0.5143, "lon": 35.2698, "region": "Rift Valley"},
    "Elgeyo Marakwet": {"lat":  0.7833, "lon": 35.5167, "region": "Rift Valley"},
    "Nandi":           {"lat":  0.1833, "lon": 35.1000, "region": "Rift Valley"},
    "Baringo":         {"lat":  0.6667, "lon": 36.0833, "region": "Rift Valley"},
    "Laikipia":        {"lat":  0.3608, "lon": 36.7819, "region": "Rift Valley"},
    "Nakuru":          {"lat": -0.3031, "lon": 36.0800, "region": "Rift Valley"},
    "Narok":           {"lat": -1.0921, "lon": 35.8700, "region": "Rift Valley"},
    "Kajiado":         {"lat": -1.8532, "lon": 36.7820, "region": "Rift Valley"},
    "Kericho":         {"lat": -0.3667, "lon": 35.2833, "region": "Rift Valley"},
    "Bomet":           {"lat": -0.7833, "lon": 35.3500, "region": "Rift Valley"},
    "Kakamega":        {"lat":  0.2827, "lon": 34.7519, "region": "Western"},
    "Vihiga":          {"lat":  0.0833, "lon": 34.7167, "region": "Western"},
    "Bungoma":         {"lat":  0.5635, "lon": 34.5597, "region": "Western"},
    "Busia":           {"lat":  0.4347, "lon": 34.1113, "region": "Western"},
    "Siaya":           {"lat": -0.0608, "lon": 34.2878, "region": "Nyanza"},
    "Kisumu":          {"lat": -0.1022, "lon": 34.7617, "region": "Nyanza"},
    "Homa Bay":        {"lat": -0.5167, "lon": 34.4500, "region": "Nyanza"},
    "Migori":          {"lat": -1.0634, "lon": 34.4731, "region": "Nyanza"},
    "Kisii":           {"lat": -0.6817, "lon": 34.7667, "region": "Nyanza"},
    "Nyamira":         {"lat": -0.5667, "lon": 34.9333, "region": "Nyanza"},
    "Nairobi":         {"lat": -1.2921, "lon": 36.8219, "region": "Nairobi"},
}

# ── County name normalisation map ─────────────────────────────────────────────
# Maps variant spellings → canonical name (used across all datasets)
COUNTY_MAP = {
    # NASA variants
    "tana river":       "Tana River",
    "taita taveta":     "Taita Taveta",
    "tharaka nithi":    "Tharaka Nithi",
    "trans nzoia":      "Trans Nzoia",
    "west pokot":       "West Pokot",
    "uasin gishu":      "Uasin Gishu",
    "elgeyo marakwet":  "Elgeyo Marakwet",
    "homa bay":         "Homa Bay",

    # FEWS NET IPC variants
    "elgeyo-marakwet":  "Elgeyo Marakwet",
    "murang'a":         "Muranga",
    "muranga":          "Muranga",
    "murang\u2019a":    "Muranga",

    # Simple lowercase → title case
    **{k.lower(): k for k in COUNTIES.keys()},
}


def normalise_county(name: str) -> Optional[str]:
    """
    Normalise a county name string to the canonical form.

    Args:
        name: Raw county name string from any dataset

    Returns:
        Canonical county name or None if not found

    Example:
        normalise_county("Elgeyo-Marakwet") → "Elgeyo Marakwet"
        normalise_county("NAIROBI")          → "Nairobi"
    """
    if not isinstance(name, str):
        return None
    cleaned = name.strip().lower()
    return COUNTY_MAP.get(cleaned, name.strip().title())


def season_of_date(date) -> str:
    """
    Return Kenya crop season for a given date.

    Kenya has two main crop seasons:
        MAM — Long rains (March–May)
        OND — Short rains (October–December)
        DS1 — Dry season Jan–Feb
        DS2 — Dry season Jun–Sep

    Args:
        date: datetime-like object

    Returns:
        Season string: 'MAM', 'OND', 'DS1', or 'DS2'
    """
    if pd.isnull(date):
        return None
    m = pd.Timestamp(date).month
    if m in [3, 4, 5]:
        return "MAM"
    elif m in [10, 11, 12]:
        return "OND"
    elif m in [1, 2]:
        return "DS1"
    else:
        return "DS2"


def compute_spi(rainfall_series: pd.Series, window: int = 3) -> pd.Series:
    """
    Compute a simplified Standardised Precipitation Index (SPI).
    SPI = (rainfall - rolling mean) / rolling std

    Positive SPI → wetter than normal
    Negative SPI → drier than normal (drought indicator)

    Args:
        rainfall_series: Monthly rainfall totals
        window: Rolling window in months (default 3 = SPI-3)

    Returns:
        SPI series (same index as input)
    """
    rolling_mean = rainfall_series.rolling(window=window, min_periods=1).mean()
    rolling_std  = rainfall_series.rolling(window=window, min_periods=1).std()
    spi = (rainfall_series - rolling_mean) / rolling_std.replace(0, np.nan)
    return spi


def ipc_label(phase: int) -> str:
    """Return human-readable label for IPC phase integer."""
    labels = {
        1: "Phase 1 — Minimal",
        2: "Phase 2 — Stressed",
        3: "Phase 3 — Crisis",
        4: "Phase 4 — Emergency",
        5: "Phase 5 — Famine",
    }
    return labels.get(phase, f"Unknown Phase ({phase})")


# ── Colour palettes for consistent plots ──────────────────────────────────────
IPC_COLOURS = {
    1: "#FFFFFF",   # Minimal — white
    2: "#FFFF00",   # Stressed — yellow
    3: "#FF6600",   # Crisis — orange
    4: "#FF0000",   # Emergency — red
    5: "#660000",   # Famine — dark red
}

SEASON_COLOURS = {
    "MAM": "#1565C0",   # Long rains — blue
    "OND": "#2E7D32",   # Short rains — green
    "DS1": "#F57F17",   # Dry season 1 — amber
    "DS2": "#BF360C",   # Dry season 2 — brown
}


# ── Print utility ─────────────────────────────────────────────────────────────
def section(title: str):
    """Print a formatted section header in notebooks."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
