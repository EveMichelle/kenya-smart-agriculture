"""clean_knbs.py — KNBS CPI raw text extraction via regex"""
import pandas as pd
import re

MONTH_MAP = {
    "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
    "july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
}

PATTERNS = {
    "overall_cpi":      r"(?:Overall|Total)\s+(?:New\s+)?CPI[^0-9]*(\d+\.?\d*)",
    "maize_grain_kg":   r"Maize\s+Grain[^0-9]*(\d+\.?\d*)",
    "sugar_kg":         r"Sugar\s+1\s*Kilogramme[^0-9]*(\d+\.?\d*)",
    "tomatoes_kg":      r"Tomatoes\s+1\s*Kg[^0-9]*(\d+\.?\d*)",
    "yoy_inflation":    r"year\s+on\s+year\s+inflation[^0-9]*([\d.]+)\s+per\s+cent",
}

def extract_month_year(filename):
    fn = filename.lower()
    year = re.search(r"(\d{4})", fn)
    year = int(year.group(1)) if year else None
    month = next((v for k,v in MONTH_MAP.items() if k in fn), None)
    return month, year

def clean_knbs(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        month, year = extract_month_year(row["file"])
        if not month or not year:
            continue
        record = {"month": month, "year": year,
                  "date": pd.Timestamp(year=year, month=month, day=1),
                  "source_file": row["file"]}
        for field, pattern in PATTERNS.items():
            m = re.search(pattern, str(row["content"]), re.IGNORECASE)
            record[field] = float(m.group(1).replace(",","")) if m else None
        rows.append(record)
    return pd.DataFrame(rows).sort_values(["year","month"]).reset_index(drop=True)
