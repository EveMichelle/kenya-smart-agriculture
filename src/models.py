"""
models.py — Model training, evaluation, and saving functions
============================================================
Used across modelling notebooks (04, 05, 06, 07)
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix,
    f1_score, accuracy_score,
    mean_absolute_error, mean_absolute_percentage_error,
    root_mean_squared_error, r2_score
)
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

MODELS_DIR = "models/saved"
os.makedirs(MODELS_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════
# CLASSIFICATION — IPC Phase Prediction
# ════════════════════════════════════════════════════════════════

IPC_FEATURES = [
    "total_rainfall", "mean_temp", "mean_solar", "mean_humidity",
    "mean_wind", "dry_days", "spi_3", "temp_range",
]

IPC_TARGET = "ipc_phase_county"


def prepare_classification_data(master: pd.DataFrame):
    """
    Prepare features and target for IPC classification.

    Returns:
        X_train, X_test, y_train, y_test, feature_names
    """
    print("  Preparing classification data...")

    # Filter to rows with IPC phase
    df = master.dropna(subset=[IPC_TARGET]).copy()
    print(f"  Rows with IPC phase: {len(df)}")

    # Use available features
    feature_cols = [f for f in IPC_FEATURES if f in df.columns]
    print(f"  Features used: {feature_cols}")

    # Handle any remaining missing values
    df[feature_cols] = df[feature_cols].fillna(df[feature_cols].median())

    X = df[feature_cols]
    y = df[IPC_TARGET].astype(int)

    print(f"  Class distribution: {y.value_counts().sort_index().to_dict()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")

    return X_train, X_test, y_train, y_test, feature_cols


def train_baseline_classifier(X_train, y_train):
    """
    Train baseline rule-based + logistic regression classifier.
    """
    print("\n  Training baseline (Logistic Regression)...")
    baseline = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    baseline.fit(X_train, y_train)
    return baseline


def train_xgboost_classifier(X_train, y_train):
    """
    Train XGBoost multi-class classifier for IPC phase prediction.
    """
    print("\n  Training XGBoost classifier...")

    # Encode labels to 0-based for XGBoost
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_train)

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
    )
    model.fit(X_train, y_encoded)
    model.label_encoder_ = le
    return model


def evaluate_classifier(model, X_test, y_test, model_name: str, label_encoder=None):
    """
    Evaluate a classifier and print a full report.
    """
    print(f"\n  {'='*50}")
    print(f"  {model_name} — Evaluation Results")
    print(f"  {'='*50}")

    if label_encoder:
        y_pred_encoded = model.predict(X_test)
        y_pred = label_encoder.inverse_transform(y_pred_encoded)
        y_test_decoded = y_test.values
    else:
        y_pred = model.predict(X_test)
        y_test_decoded = y_test.values

    # Metrics
    f1        = f1_score(y_test_decoded, y_pred, average="weighted")
    accuracy  = accuracy_score(y_test_decoded, y_pred)
    print(f"  Weighted F1 Score : {f1:.4f}")
    print(f"  Accuracy          : {accuracy:.4f}")
    print(f"\n  Classification Report:")
    print(classification_report(y_test_decoded, y_pred))

    return {"model": model_name, "f1_weighted": f1, "accuracy": accuracy}


def plot_confusion_matrix(model, X_test, y_test, model_name: str, label_encoder=None):
    """Plot and save confusion matrix."""
    if label_encoder:
        y_pred = label_encoder.inverse_transform(model.predict(X_test))
    else:
        y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    labels = sorted(y_test.unique())
    label_names = [f"Phase {l}" for l in labels]

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=label_names, yticklabels=label_names, ax=ax)
    ax.set_title(f"Confusion Matrix — {model_name}")
    ax.set_xlabel("Predicted Phase")
    ax.set_ylabel("Actual Phase")
    plt.tight_layout()

    save_path = f"reports/figures/confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Saved: {save_path}")


# ════════════════════════════════════════════════════════════════
# REGRESSION — CPI Price Forecasting
# ════════════════════════════════════════════════════════════════

def evaluate_regression(y_true, y_pred, model_name: str) -> dict:
    """
    Evaluate a regression model and print results.
    """
    print(f"\n  {'='*50}")
    print(f"  {model_name} — Regression Evaluation")
    print(f"  {'='*50}")

    mae  = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    rmse = root_mean_squared_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)

    print(f"  MAE  : {mae:.4f}")
    print(f"  MAPE : {mape:.2f}%")
    print(f"  RMSE : {rmse:.4f}")
    print(f"  R²   : {r2:.4f}")

    return {"model": model_name, "mae": mae, "mape": mape, "rmse": rmse, "r2": r2}


def compare_models(results: list) -> pd.DataFrame:
    """
    Create a comparison table of model results.

    Args:
        results: List of dicts from evaluate_classifier or evaluate_regression

    Returns:
        Sorted comparison DataFrame
    """
    df = pd.DataFrame(results)

    # Sort by best metric
    if "f1_weighted" in df.columns:
        df = df.sort_values("f1_weighted", ascending=False)
    elif "mape" in df.columns:
        df = df.sort_values("mape", ascending=True)

    print("\n  MODEL COMPARISON:")
    print(df.to_string(index=False))
    return df


# ════════════════════════════════════════════════════════════════
# MODEL SAVING & LOADING
# ════════════════════════════════════════════════════════════════

def save_model(model, name: str):
    """Serialise and save a model to models/saved/."""
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    joblib.dump(model, path)
    size = os.path.getsize(path) / 1024
    print(f"  Saved: {path} ({size:.1f} KB)")


def load_model(name: str):
    """Load a saved model from models/saved/."""
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)
