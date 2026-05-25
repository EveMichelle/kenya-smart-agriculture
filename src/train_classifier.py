"""train_classifier.py — IPC food security classification models"""
import joblib, os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

FEATURES = ["total_rainfall","mean_temp","mean_solar","mean_humidity","dry_days","spi_3","temp_range"]
TARGET   = "ipc_phase_county"

def prepare_data(master):
    df = master.dropna(subset=[TARGET]).copy()
    cols = [f for f in FEATURES if f in df.columns]
    df[cols] = df[cols].fillna(df[cols].median())
    X, y = df[cols], df[TARGET].astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def train_logistic(X_train, y_train):
    m = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    m.fit(X_train, y_train)
    return m

def train_xgboost(X_train, y_train):
    le = LabelEncoder()
    y_enc = le.fit_transform(y_train)
    m = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05,
                           eval_metric="mlogloss", random_state=42)
    m.fit(X_train, y_enc)
    m.label_encoder_ = le
    return m

def save_model(model, name):
    os.makedirs("models/saved", exist_ok=True)
    joblib.dump(model, f"models/saved/{name}.pkl")
    print(f"Saved: models/saved/{name}.pkl")
