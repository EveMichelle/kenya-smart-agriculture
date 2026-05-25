"""
scripts/fetch_nasa.py
=====================
Run ONCE to fetch NASA POWER weather data for all 47 Kenya counties.
Saves CSVs to: data/raw/weather/

Run:
    python scripts/fetch_nasa.py

Compatible with Python 3.8+
"""

import requests
import pandas as pd
import time
import os
from tqdm import tqdm

# ── Output ────────────────────────────────────────────────────
OUTPUT_DIR = "data/raw/weather"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── All 47 Counties ───────────────────────────────────────────
KENYA_COUNTIES = {
    "Mombasa":         {"lat": -4.0435, "lon": 39.6682},
    "Kwale":           {"lat": -4.1817, "lon": 39.4606},
    "Kilifi":          {"lat": -3.5107, "lon": 39.9093},
    "Tana River":      {"lat": -1.5000, "lon": 39.5000},
    "Lamu":            {"lat": -2.2686, "lon": 40.9020},
    "Taita Taveta":    {"lat": -3.3167, "lon": 38.4833},
    "Garissa":         {"lat": -0.4536, "lon": 39.6401},
    "Wajir":           {"lat":  1.7471, "lon": 40.0573},
    "Mandera":         {"lat":  3.9373, "lon": 41.8570},
    "Marsabit":        {"lat":  2.3284, "lon": 37.9899},
    "Isiolo":          {"lat":  0.3556, "lon": 37.5820},
    "Meru":            {"lat":  0.0467, "lon": 37.6490},
    "Tharaka Nithi":   {"lat": -0.2000, "lon": 37.8000},
    "Embu":            {"lat": -0.5357, "lon": 37.4580},
    "Kitui":           {"lat": -1.3671, "lon": 38.0108},
    "Machakos":        {"lat": -1.5177, "lon": 37.2634},
    "Makueni":         {"lat": -2.2558, "lon": 37.6242},
    "Nyandarua":       {"lat": -0.1833, "lon": 36.5833},
    "Nyeri":           {"lat": -0.4167, "lon": 36.9500},
    "Kirinyaga":       {"lat": -0.6600, "lon": 37.3800},
    "Muranga":         {"lat": -0.7167, "lon": 37.1500},
    "Kiambu":          {"lat": -1.0314, "lon": 36.8063},
    "Turkana":         {"lat":  3.1162, "lon": 35.5960},
    "West Pokot":      {"lat":  1.6210, "lon": 35.1170},
    "Samburu":         {"lat":  1.2166, "lon": 36.9000},
    "Trans Nzoia":     {"lat":  1.0566, "lon": 35.0000},
    "Uasin Gishu":     {"lat":  0.5143, "lon": 35.2698},
    "Elgeyo Marakwet": {"lat":  0.7833, "lon": 35.5167},
    "Nandi":           {"lat":  0.1833, "lon": 35.1000},
    "Baringo":         {"lat":  0.6667, "lon": 36.0833},
    "Laikipia":        {"lat":  0.3608, "lon": 36.7819},
    "Nakuru":          {"lat": -0.3031, "lon": 36.0800},
    "Narok":           {"lat": -1.0921, "lon": 35.8700},
    "Kajiado":         {"lat": -1.8532, "lon": 36.7820},
    "Kericho":         {"lat": -0.3667, "lon": 35.2833},
    "Bomet":           {"lat": -0.7833, "lon": 35.3500},
    "Kakamega":        {"lat":  0.2827, "lon": 34.7519},
    "Vihiga":          {"lat":  0.0833, "lon": 34.7167},
    "Bungoma":         {"lat":  0.5635, "lon": 34.5597},
    "Busia":           {"lat":  0.4347, "lon": 34.1113},
    "Siaya":           {"lat": -0.0608, "lon": 34.2878},
    "Kisumu":          {"lat": -0.1022, "lon": 34.7617},
    "Homa Bay":        {"lat": -0.5167, "lon": 34.4500},
    "Migori":          {"lat": -1.0634, "lon": 34.4731},
    "Kisii":           {"lat": -0.6817, "lon": 34.7667},
    "Nyamira":         {"lat": -0.5667, "lon": 34.9333},
    "Nairobi":         {"lat": -1.2921, "lon": 36.8219},
}

NASA_PARAMS = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN"
NASA_URL    = "https://power.larc.nasa.gov/api/temporal/daily/point"
START_YEAR  = 2000
END_YEAR    = 2023


def fetch_year(county_name, lat, lon, year):
    params = {
        "parameters": NASA_PARAMS,
        "community":  "AG",
        "longitude":  lon,
        "latitude":   lat,
        "start":      "{}0101".format(year),
        "end":        "{}1231".format(year),
        "format":     "JSON",
    }
    try:
        r = requests.get(NASA_URL, params=params, timeout=45)
        r.raise_for_status()
        data = r.json().get("properties", {}).get("parameter", {})
        if not data:
            return None
        df = pd.DataFrame(data)
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        df.index.name = "date"
        df.reset_index(inplace=True)
        df.insert(0, "county",    county_name)
        df.insert(1, "latitude",  lat)
        df.insert(2, "longitude", lon)
        df.replace(-999.0, float("nan"), inplace=True)
        return df
    except Exception as e:
        print("  Error {} {}: {}".format(county_name, year, e))
        return None


def main():
    print("\n" + "="*60)
    print("  NASA POWER — Kenya Weather Data Fetcher")
    print("  Counties : {}".format(len(KENYA_COUNTIES)))
    print("  Years    : {} - {}".format(START_YEAR, END_YEAR))
    print("  Output   : {}/".format(OUTPUT_DIR))
    print("  Est. time: 45-90 minutes")
    print("="*60 + "\n")

    all_frames = []
    years = list(range(START_YEAR, END_YEAR + 1))

    for county_name, coords in tqdm(KENYA_COUNTIES.items(), desc="Counties"):
        lat, lon    = coords["lat"], coords["lon"]
        county_slug = county_name.replace(" ", "_").lower()
        county_file = os.path.join(OUTPUT_DIR, "{}.csv".format(county_slug))

        if os.path.exists(county_file):
            all_frames.append(pd.read_csv(county_file))
            continue

        county_frames = []
        for year in years:
            df = fetch_year(county_name, lat, lon, year)
            if df is not None:
                county_frames.append(df)
            time.sleep(0.5)

        if county_frames:
            county_df = pd.concat(county_frames, ignore_index=True)
            county_df.to_csv(county_file, index=False)
            all_frames.append(county_df)
            print("  Done: {} ({} rows)".format(county_name, len(county_df)))

    if all_frames:
        master = pd.concat(all_frames, ignore_index=True)
        master_file = os.path.join(OUTPUT_DIR, "kenya_weather_all_counties.csv")
        master.to_csv(master_file, index=False)
        print("\n" + "="*60)
        print("  COMPLETE!")
        print("  Total rows : {:,}".format(len(master)))
        print("  Counties   : {}".format(master["county"].nunique()))
        print("  Saved      : {}".format(master_file))
        print("="*60)


if __name__ == "__main__":
    main()
