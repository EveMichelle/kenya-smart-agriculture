"""clean_news.py — News article cleaning and entity extraction"""
import pandas as pd
import re

COUNTY_KEYWORDS = [
    "mombasa","kwale","kilifi","tana river","lamu","taita taveta","garissa",
    "wajir","mandera","marsabit","isiolo","meru","embu","kitui","machakos",
    "makueni","nyandarua","nyeri","kirinyaga","muranga","kiambu","turkana",
    "west pokot","samburu","trans nzoia","uasin gishu","nandi","baringo",
    "laikipia","nakuru","narok","kajiado","kericho","bomet","kakamega",
    "vihiga","bungoma","busia","siaya","kisumu","homa bay","migori",
    "kisii","nyamira","nairobi",
]

COMMODITY_KEYWORDS = [
    "maize","beans","sugar","flour","rice","tomatoes","onions","potatoes",
    "kale","sukuma","milk","beef","cooking oil","wheat","sorghum","tea","coffee",
]

def clean_news(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
    df["title_clean"] = (df["title"]
        .str.replace(r"<[^>]+>", "", regex=True)
        .str.replace(r"\s+", " ", regex=True).str.strip())
    df = df[df["title_clean"].str.len() > 15]
    tl = df["title_clean"].str.lower()
    df["counties_mentioned"]    = tl.apply(lambda t: [k.title() for k in COUNTY_KEYWORDS if k in t])
    df["commodities_mentioned"] = tl.apply(lambda t: [k.title() for k in COMMODITY_KEYWORDS if k in t])
    return df
