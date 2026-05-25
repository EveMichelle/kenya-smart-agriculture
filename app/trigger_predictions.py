"""
app/trigger_predictions.py
===========================
Generates fresh predictions for all counties.
Called by the Streamlit app when user requests a prediction update.

Usage:
    python app/trigger_predictions.py
"""

import pandas as pd
import joblib
import os

MODELS_DIR  = "models/saved"
MASTER_PATH = "data/processed/master_dataset.csv"


def load_ipc_model():
    path = os.path.join(MODELS_DIR, "xgboost_ipc_classifier.pkl")
    if os.path.exists(path):
        return joblib.load(path)
    return None


def predict_all_counties():
    """Run IPC classification prediction for all counties."""
    print("  Running county predictions...")

    if not os.path.exists(MASTER_PATH):
        print("  ⚠️  Master dataset not found. Run main.py first.")
        return None

    master = pd.read_csv(MASTER_PATH)
    model  = load_ipc_model()

    if model is None:
        print("  ⚠️  Model not found. Run scripts/train_model1.py first.")
        return None

    feature_cols = ["total_rainfall","mean_temp","mean_solar",
                    "mean_humidity","dry_days","spi_3","temp_range"]
    available    = [f for f in feature_cols if f in master.columns]

    # Predict on latest available month per county
    latest = master.sort_values(["year","month"]).groupby("county").last().reset_index()
    X = latest[available].fillna(latest[available].median())

    le     = model.label_encoder_
    y_pred = le.inverse_transform(model.predict(X))

    predictions = pd.DataFrame({
        "county":          latest["county"],
        "predicted_phase": y_pred,
        "phase_label":     [
            {1:"Minimal", 2:"Stressed", 3:"Crisis"}.get(int(p), str(p))
            for p in y_pred
        ],
    })

    predictions.to_csv("data/processed/latest_predictions.csv", index=False)
    print(f"  ✅ Predictions generated for {len(predictions)} counties")
    return predictions


if __name__ == "__main__":
    preds = predict_all_counties()
    if preds is not None:
        print("\n  County Predictions:")
        print(preds.to_string(index=False))
