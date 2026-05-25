"""constants.py — Shared paths, labels, county list"""
import os

# Paths
RAW_DIR        = "data/raw"
PROCESSED_DIR  = "data/processed"
MODELS_DIR     = "models/saved"
FIGURES_DIR    = "figures"
TABLEAU_DIR    = "tableau"

NASA_PATH      = os.path.join(RAW_DIR, "weather/kenya_weather_all_counties.csv")
IPC_PATH       = os.path.join(RAW_DIR, "food_security/kenya_ipc.csv")
KNBS_PATH      = os.path.join(RAW_DIR, "prices/knbs_cpi_raw_text.csv")
NEWS_PATH      = os.path.join(RAW_DIR, "news/kenya_agri_news_raw.csv")

# IPC Phase labels
IPC_LABELS = {1: "Minimal", 2: "Stressed", 3: "Crisis", 4: "Emergency", 5: "Famine"}
IPC_COLOURS = {1: "#FFFFFF", 2: "#FFFF00", 3: "#FF6600", 4: "#FF0000", 5: "#660000"}

# Kenya seasons
SEASONS = {"MAM": [3,4,5], "OND": [10,11,12], "DS1": [1,2], "DS2": [6,7,8,9]}

# All 47 counties
KENYA_COUNTIES = [
    "Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita Taveta",
    "Garissa","Wajir","Mandera","Marsabit","Isiolo","Meru",
    "Tharaka Nithi","Embu","Kitui","Machakos","Makueni","Nyandarua",
    "Nyeri","Kirinyaga","Muranga","Kiambu","Turkana","West Pokot",
    "Samburu","Trans Nzoia","Uasin Gishu","Elgeyo Marakwet","Nandi",
    "Baringo","Laikipia","Nakuru","Narok","Kajiado","Kericho","Bomet",
    "Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu",
    "Homa Bay","Migori","Kisii","Nyamira","Nairobi",
]
