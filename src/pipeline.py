"""pipeline.py — End-to-end pipeline orchestration"""
import pandas as pd
import os
from src.load_data import load_all
from src.clean_nasa import clean_nasa, aggregate_monthly
from src.clean_ipc import clean_ipc
from src.clean_knbs import clean_knbs
from src.clean_news import clean_news

def run_cleaning_pipeline(save=True):
    print("Loading raw data...")
    data = load_all()

    print("Cleaning NASA POWER...")
    nasa_clean   = clean_nasa(data["nasa"])
    nasa_monthly = aggregate_monthly(nasa_clean)

    print("Cleaning FEWS NET IPC...")
    ipc_clean = clean_ipc(data["ipc"])

    print("Extracting KNBS CPI prices...")
    knbs_clean = clean_knbs(data["knbs"])

    print("Cleaning news articles...")
    news_clean = clean_news(data["news"])

    if save:
        os.makedirs("data/processed", exist_ok=True)
        nasa_monthly.to_csv("data/processed/nasa_monthly_clean.csv", index=False)
        ipc_clean.to_csv("data/processed/ipc_clean.csv", index=False)
        knbs_clean.to_csv("data/processed/knbs_cpi_structured.csv", index=False)
        news_clean.to_csv("data/processed/news_clean.csv", index=False)
        print("All processed files saved to data/processed/")

    return nasa_monthly, ipc_clean, knbs_clean, news_clean
