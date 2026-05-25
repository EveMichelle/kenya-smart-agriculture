"""
data_cleaner.py — Reusable dataset cleaning functions
=====================================================
Used in notebooks/02_data_cleaning.ipynb

Functions:
    clean_nasa()       → Clean NASA POWER weather dataset
    clean_ipc()        → Clean FEWS NET IPC food security data
    clean_knbs_cpi()   → Extract structured data from raw KNBS CPI text
    clean_news()       → Clean scraped news articles
    merge_master()     → Merge cleaned datasets into one master DataFrame
"""

import pandas as pd
import numpy as np
import re
from typing import Optional
from src.utils import normalise_county, season_of_date, compute_spi, COUNTIES


# ════════════════════════════════════════════════════════════════
# 1. NASA POWER — Weather Data Cleaning
# ════════════════════════════════════════════════════════════════

def clean_nasa(path: str) -> pd.DataFrame:
    """
    Clean the NASA POWER all-counties weather CSV.

    Steps:
        1. Replace -999 fill values with NaN
        2. Parse dates to datetime64
        3. Normalise county names
        4. Add season column (MAM / OND / DS1 / DS2)
        5. Report missing data

    Args:
        path: Path to kenya_weather_all_counties.csv

    Returns:
        Cleaned daily weather DataFrame
    """
    print("  Loading NASA POWER data...")
    df = pd.read_csv(path, low_memory=False)
    print(f"  Raw shape: {df.shape}")

    # Step 1 — Replace NASA missing value flag
    nasa_cols = ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR",
                 "RH2M", "WS2M", "ALLSKY_SFC_SW_DWN"]
    before = df[nasa_cols].isnull().sum().sum()
    df[nasa_cols] = df[nasa_cols].replace(-999.0, np.nan)
    after  = df[nasa_cols].isnull().sum().sum()
    print(f"  Replaced {after - before:,} -999 fill values with NaN")

    # Step 2 — Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month
    print(f"  Date range: {df['date'].min().date()} → {df['date'].max().date()}")

    # Step 3 — Normalise county names
    df["county"] = df["county"].apply(normalise_county)

    # Step 4 — Add season
    df["season"] = df["date"].apply(season_of_date)

    # Step 5 — Report
    missing_pct = df[nasa_cols].isnull().mean().mul(100).round(2)
    print(f"  Missing data after cleaning:")
    for col, pct in missing_pct.items():
        flag = " ⚠" if pct > 5 else ""
        print(f"    {col:<25} {pct:.2f}%{flag}")

    print(f"  Clean shape: {df.shape}")
    print(f"  Counties: {df['county'].nunique()}")
    return df


def aggregate_nasa_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily NASA weather to monthly county-level summaries.
    Used to align with monthly KNBS CPI data.

    Returns:
        Monthly DataFrame with columns:
        county, year, month, season,
        total_rainfall, mean_temp, max_temp, min_temp,
        mean_humidity, mean_solar, mean_wind
    """
    print("  Aggregating NASA daily → monthly...")

    monthly = df.groupby(["county", "year", "month", "season"]).agg(
        total_rainfall   = ("PRECTOTCORR",      "sum"),
        mean_temp        = ("T2M",              "mean"),
        max_temp         = ("T2M_MAX",          "mean"),
        min_temp         = ("T2M_MIN",          "mean"),
        mean_humidity    = ("RH2M",             "mean"),
        mean_solar       = ("ALLSKY_SFC_SW_DWN","mean"),
        mean_wind        = ("WS2M",             "mean"),
        dry_days         = ("PRECTOTCORR",
                            lambda x: (x < 1.0).sum()),
    ).reset_index()

    # Add SPI per county
    monthly = monthly.sort_values(["county", "year", "month"])
    monthly["spi_3"] = (
        monthly.groupby("county")["total_rainfall"]
        .transform(lambda x: compute_spi(x, window=3))
    )

    # Add temperature range
    monthly["temp_range"] = monthly["max_temp"] - monthly["min_temp"]

    print(f"  Monthly shape: {monthly.shape}")
    return monthly


def aggregate_nasa_seasonal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily NASA weather to seasonal county-level summaries.
    Used to pair with annual FEWS IPC data.

    Returns:
        Seasonal DataFrame: county, year, season + weather aggregates
    """
    print("  Aggregating NASA daily → seasonal...")

    seasonal = df.groupby(["county", "year", "season"]).agg(
        total_rainfall   = ("PRECTOTCORR",      "sum"),
        mean_temp        = ("T2M",              "mean"),
        mean_solar       = ("ALLSKY_SFC_SW_DWN","mean"),
        consecutive_dry  = ("PRECTOTCORR",
                            lambda x: max(
                                (x < 1.0).astype(int).groupby(
                                    (x >= 1.0).astype(int).cumsum()
                                ).sum(),
                                default=0
                            )),
    ).reset_index()

    # Add SPI per county per season
    seasonal = seasonal.sort_values(["county", "year"])
    seasonal["spi_seasonal"] = (
        seasonal.groupby(["county", "season"])["total_rainfall"]
        .transform(lambda x: compute_spi(x, window=1))
    )

    print(f"  Seasonal shape: {seasonal.shape}")
    return seasonal


# ════════════════════════════════════════════════════════════════
# 2. FEWS NET IPC — Food Security Classification Cleaning
# ════════════════════════════════════════════════════════════════

def clean_ipc(path: str) -> pd.DataFrame:
    """
    Clean FEWS NET IPC food security dataset.

    Steps:
        1. Rename columns to clear names
        2. Normalise county (ADMIN1) names
        3. Parse coverage dates
        4. Drop high-missing ADMIN3 column
        5. Map IPC phase to labels
        6. Keep county-level rows only

    Args:
        path: Path to kenya_ipc.csv

    Returns:
        Cleaned IPC DataFrame
    """
    print("  Loading FEWS NET IPC data...")
    df = pd.read_csv(path)
    print(f"  Raw shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")

    # Step 1 — Rename columns
    col_map = {
        "cov_start":  "period_start",
        "cov_end":    "period_end",
        "report_mon": "report_month",
        "country":    "country",
        "ADMIN0":     "country_name",
        "ADMIN1":     "county",
        "ADMIN2":     "sub_county",
        "ADMIN3":     "location",
        "LZCODE":     "livelihood_zone_code",
        "LZNAME":     "livelihood_zone_name",
        "ML1":        "ipc_phase",
        "HA1":        "humanitarian_assistance",
        "unit_type":  "unit_type",
        "fewsnet_re": "fewsnet_region",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    # Step 2 — Normalise county names
    df["county"] = df["county"].apply(normalise_county)
    print(f"  Counties found: {df['county'].nunique()} → {sorted(df['county'].unique())}")

    # Step 3 — Parse dates
    for col in ["period_start", "period_end", "report_month"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%m-%Y", errors="coerce")

    # Step 4 — Drop ADMIN3 (55.5% missing, not needed)
    if "location" in df.columns:
        missing_pct = df["location"].isnull().mean() * 100
        print(f"  Dropping 'location' column ({missing_pct:.1f}% missing)")
        df = df.drop(columns=["location"])

    # Step 5 — Add IPC phase label
    phase_labels = {1: "Minimal", 2: "Stressed", 3: "Crisis",
                    4: "Emergency", 5: "Famine"}
    df["ipc_phase_label"] = df["ipc_phase"].map(phase_labels)
    print(f"  IPC phase distribution:")
    print(f"  {df['ipc_phase'].value_counts().sort_index().to_dict()}")

    # Step 6 — Keep county-level rows (drop sub-county duplicates if needed)
    print(f"  Clean shape: {df.shape}")
    return df


# ════════════════════════════════════════════════════════════════
# 3. KNBS CPI — Raw Text Extraction & Structuring
# ════════════════════════════════════════════════════════════════

# Regex patterns for KNBS CPI table extraction
PRICE_PATTERNS = {
    "maize_grain_kg":     r"Maize\s+Grain[^0-9]*(\d+\.?\d*)",
    "maize_flour_2kg":    r"Maize\s+[Ff]lour[^0-9]*(\d+\.?\d*)",
    "sugar_kg":           r"Sugar\s+1\s*Kilogramme[^0-9]*(\d+\.?\d*)",
    "cooking_oil_L":      r"Cooking\s+Oil[^0-9]*(\d+\.?\d*)",
    "tomatoes_kg":        r"Tomatoes\s+1\s*Kg[^0-9]*(\d+\.?\d*)",
    "potatoes_kg":        r"Potatoes\s*\(Irish\)[^0-9]*(\d+\.?\d*)",
    "onions_kg":          r"Onion[^0-9]*1\s*Kilogramme[^0-9]*(\d+\.?\d*)",
    "kale_kg":            r"Kale[^0-9]*1\s*Kg[^0-9]*(\d+\.?\d*)",
    "wheat_flour_2kg":    r"Wheat\s+Flour[^0-9]*2\s*Kg[^0-9]*(\d+\.?\d*)",
    "overall_cpi":        r"(?:Overall|Total)\s+(?:New\s+)?CPI[^0-9]*(\d+\.?\d*)",
    "food_cpi_change":    r"Food\s+and\s+Non.Alcoholic\s+Beverages\s+[\d.]+\s+([\d.]+)",
    "yoy_inflation":      r"year\s+on\s+year\s+inflation[^0-9]*([\d.]+)\s+per\s+cent",
}

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def extract_month_year_from_filename(filename: str):
    """Extract (month, year) integers from KNBS PDF filename."""
    fn = filename.lower()
    year_match = re.search(r"(\d{4})", fn)
    year = int(year_match.group(1)) if year_match else None

    month = None
    for month_name, month_num in MONTH_MAP.items():
        if month_name in fn:
            month = month_num
            break

    return month, year


def extract_prices_from_text(text: str) -> dict:
    """
    Extract commodity prices and CPI values from raw KNBS PDF text.

    Args:
        text: Raw extracted PDF text content

    Returns:
        Dict of {field_name: float_value}
    """
    results = {}
    for field, pattern in PRICE_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                # Remove commas from numbers like "1,234.56"
                val_str = match.group(1).replace(",", "")
                results[field] = float(val_str)
            except (ValueError, IndexError):
                results[field] = None
        else:
            results[field] = None
    return results


def clean_knbs_cpi(path: str) -> pd.DataFrame:
    """
    Extract structured price data from raw KNBS CPI text CSV.

    The input CSV has 2 columns: file (PDF filename) + content (raw text).
    This function extracts commodity prices and CPI values using regex.

    Args:
        path: Path to knbs_cpi_raw_text.csv

    Returns:
        Structured DataFrame with one row per month-year,
        columns: month, year, date + all commodity prices
    """
    print("  Loading KNBS CPI raw text...")
    df = pd.read_csv(path)
    print(f"  Raw shape: {df.shape}")
    print(f"  PDF reports: {df['file'].nunique()}")

    rows = []
    for _, row in df.iterrows():
        month, year = extract_month_year_from_filename(row["file"])
        if not month or not year:
            continue

        prices = extract_prices_from_text(str(row["content"]))
        prices["month"]     = month
        prices["year"]      = year
        prices["date"]      = pd.Timestamp(year=year, month=month, day=1)
        prices["source_file"] = row["file"]
        rows.append(prices)

    structured = pd.DataFrame(rows)

    if structured.empty:
        print("  WARNING: No prices extracted — check regex patterns")
        return structured

    structured = structured.sort_values(["year", "month"]).reset_index(drop=True)

    print(f"  Extracted {len(structured)} monthly records")
    print(f"  Date range: {structured['date'].min().date()} → {structured['date'].max().date()}")
    print(f"  Extraction success rate:")
    price_cols = [c for c in structured.columns
                  if c not in ["month", "year", "date", "source_file"]]
    for col in price_cols:
        success = structured[col].notna().mean() * 100
        flag = " ⚠" if success < 50 else ""
        print(f"    {col:<25} {success:.0f}% extracted{flag}")

    return structured


# ════════════════════════════════════════════════════════════════
# 4. News Articles — NLP Preprocessing
# ════════════════════════════════════════════════════════════════

# Keywords for county and commodity extraction
COUNTY_KEYWORDS = [c.lower() for c in COUNTIES.keys()] + [
    "muranga", "murang'a", "elgeyo", "homa bay", "tana river"
]

COMMODITY_KEYWORDS = [
    "maize", "beans", "sugar", "flour", "rice", "tomatoes", "onions",
    "potatoes", "kale", "sukuma", "milk", "beef", "chicken", "cooking oil",
    "wheat", "sorghum", "millet", "tea", "coffee", "avocado"
]


def extract_counties_mentioned(title: str) -> list:
    """Extract county names mentioned in a news title."""
    if not isinstance(title, str):
        return []
    title_lower = title.lower()
    return [kw.title() for kw in COUNTY_KEYWORDS if kw in title_lower]


def extract_commodities_mentioned(title: str) -> list:
    """Extract commodity names mentioned in a news title."""
    if not isinstance(title, str):
        return []
    title_lower = title.lower()
    return [kw.title() for kw in COMMODITY_KEYWORDS if kw in title_lower]


def clean_news(path: str) -> pd.DataFrame:
    """
    Clean scraped Kenya agricultural news articles.

    Steps:
        1. Parse dates to datetime64
        2. Remove duplicate URLs
        3. Clean title text (strip HTML artifacts)
        4. Extract county mentions
        5. Extract commodity mentions
        6. Add text length feature

    Args:
        path: Path to kenya_agri_news_raw.csv

    Returns:
        Cleaned news DataFrame ready for NLP
    """
    print("  Loading news articles...")
    df = pd.read_csv(path)
    print(f"  Raw shape: {df.shape}")

    # Step 1 — Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    df["date"] = df["date"].dt.tz_localize(None)
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month
    print(f"  Date range: {df['date'].min()} → {df['date'].max()}")

    # Step 2 — Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
    print(f"  Removed {before - len(df)} duplicate URLs")

    # Step 3 — Clean titles
    df["title_clean"] = (
        df["title"]
        .str.replace(r"<[^>]+>", "", regex=True)    # Strip HTML tags
        .str.replace(r"\s+", " ", regex=True)        # Collapse whitespace
        .str.strip()
    )
    df = df[df["title_clean"].str.len() > 15]        # Drop very short titles

    # Step 4 — Extract county mentions
    df["counties_mentioned"] = df["title_clean"].apply(extract_counties_mentioned)
    df["county_count"]       = df["counties_mentioned"].apply(len)

    # Step 5 — Extract commodity mentions
    df["commodities_mentioned"] = df["title_clean"].apply(extract_commodities_mentioned)
    df["commodity_count"]       = df["commodities_mentioned"].apply(len)

    # Step 6 — Text length
    df["title_length"] = df["title_clean"].str.len()

    print(f"  Clean shape: {df.shape}")
    print(f"  Articles with county mention: {(df['county_count'] > 0).sum()}")
    print(f"  Articles with commodity mention: {(df['commodity_count'] > 0).sum()}")
    return df


# ════════════════════════════════════════════════════════════════
# 5. MERGE — Build Master Dataset
# ════════════════════════════════════════════════════════════════

def merge_master(
    nasa_monthly: pd.DataFrame,
    ipc_clean: pd.DataFrame,
    knbs_clean: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge cleaned datasets into a unified master modelling DataFrame.

    Join keys:
        NASA monthly ← county + year + month
        KNBS CPI     ← year + month (national level)
        IPC          ← county (single snapshot, broadcast across months)

    Args:
        nasa_monthly: Output of aggregate_nasa_monthly()
        ipc_clean:    Output of clean_ipc()
        knbs_clean:   Output of clean_knbs_cpi()

    Returns:
        Master DataFrame for modelling
    """
    print("  Building master dataset...")
    print(f"  Input shapes — NASA: {nasa_monthly.shape}, "
          f"IPC: {ipc_clean.shape}, KNBS: {knbs_clean.shape}")

    # Merge 1: NASA monthly + KNBS CPI on year + month
    # KNBS is national-level so broadcast to all counties
    cpi_cols = ["year", "month", "overall_cpi", "food_cpi_change",
                "yoy_inflation", "maize_grain_kg", "sugar_kg",
                "cooking_oil_L", "tomatoes_kg"]
    cpi_cols = [c for c in cpi_cols if c in knbs_clean.columns]

    master = nasa_monthly.merge(
        knbs_clean[cpi_cols],
        on=["year", "month"],
        how="left"
    )
    print(f"  After NASA + KNBS merge: {master.shape}")

    # Merge 2: Add IPC phase (county-level, single snapshot)
    # Take county-level IPC phase (aggregate sub-county to county mode)
    ipc_county = (
        ipc_clean
        .groupby("county")["ipc_phase"]
        .agg(lambda x: x.mode()[0])
        .reset_index()
        .rename(columns={"ipc_phase": "ipc_phase_county"})
    )

    master = master.merge(ipc_county, on="county", how="left")
    print(f"  After IPC merge: {master.shape}")

    # Summary
    print(f"\n  MASTER DATASET SUMMARY:")
    print(f"  Shape          : {master.shape}")
    print(f"  Counties       : {master['county'].nunique()}")
    print(f"  Date range     : {master['year'].min()} – {master['year'].max()}")
    print(f"  Missing values : {master.isnull().mean().mul(100).round(1).to_dict()}")

    return master
