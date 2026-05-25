"""load_data.py — Raw data loading functions"""
import pandas as pd
from src.constants import NASA_PATH, IPC_PATH, KNBS_PATH, NEWS_PATH

def load_nasa():
    return pd.read_csv(NASA_PATH, low_memory=False)

def load_ipc():
    return pd.read_csv(IPC_PATH)

def load_knbs():
    return pd.read_csv(KNBS_PATH)

def load_news():
    return pd.read_csv(NEWS_PATH)

def load_all():
    return {
        "nasa": load_nasa(),
        "ipc":  load_ipc(),
        "knbs": load_knbs(),
        "news": load_news(),
    }
