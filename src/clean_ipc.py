"""clean_ipc.py — FEWS NET IPC food security cleaning"""
import pandas as pd
from src.constants import IPC_LABELS

def clean_ipc(df: pd.DataFrame) -> pd.DataFrame:
    col_map = {"ADMIN1":"county","ADMIN2":"sub_county","ML1":"ipc_phase","HA1":"humanitarian_assistance"}
    df = df.rename(columns={k:v for k,v in col_map.items() if k in df.columns})
    if "ADMIN3" in df.columns:
        df = df.drop(columns=["ADMIN3"])
    df["ipc_phase_label"] = df["ipc_phase"].map(IPC_LABELS)
    return df
