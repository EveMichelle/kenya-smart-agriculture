"""scripts/train_model1.py — Train food security classification model (IPC + NASA)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.train_classifier import prepare_data, train_xgboost, save_model
from src.evaluate import evaluate_classifier

def main():
    print("\n" + "="*55)
    print("  MODEL 1 — Food Security Classification")
    print("  Algorithm: XGBoost Multi-class Classifier")
    print("  Target   : IPC Phase (1=Minimal 2=Stressed 3=Crisis)")
    print("="*55)

    master = pd.read_csv("data/processed/master_dataset.csv")
    X_train, X_test, y_train, y_test = prepare_data(master)

    print("\n  Training XGBoost...")
    model = train_xgboost(X_train, y_train)

    le = model.label_encoder_
    results = evaluate_classifier(model, X_test, y_test,
                                  "XGBoost IPC Classifier", le)
    save_model(model, "xgboost_ipc_classifier")
    print("\n  ✅ Model 1 complete — saved to models/saved/")
    return results

if __name__ == "__main__":
    main()
