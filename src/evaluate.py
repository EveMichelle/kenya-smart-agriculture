"""evaluate.py — Evaluation metrics and reporting"""
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score, classification_report

def evaluate_classifier(model, X_test, y_test, name, label_encoder=None):
    y_pred = model.predict(X_test)
    if label_encoder:
        y_pred = label_encoder.inverse_transform(y_pred)
    f1  = f1_score(y_test, y_pred, average="weighted")
    acc = accuracy_score(y_test, y_pred)
    print(f"\n{name} — Weighted F1: {f1:.4f} | Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    return {"model": name, "f1_weighted": f1, "accuracy": acc}

def compare_models(results):
    df = pd.DataFrame(results).sort_values("f1_weighted", ascending=False)
    print("\nMODEL COMPARISON:")
    print(df.to_string(index=False))
    return df
