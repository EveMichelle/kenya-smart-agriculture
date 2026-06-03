"""scripts/train_price_forecast.py
Train food price forecasting model (KNBS CPI).
Run: python scripts/train_price_forecast.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.train_forecaster import prepare_cpi_series, train_arima, train_prophet


def main():
    print("\n" + "="*55)
    print("  MODEL 2 — Food Price Forecasting")
    print("  Algorithm: ARIMA (AutoRegressive Integrated Moving Average)")
    print("             baseline → Facebook Prophet")
    print("  Target   : Monthly KNBS (Kenya National Bureau of Statistics)")
    print("             CPI (Consumer Price Index) Food Index")
    print("="*55)

    knbs = pd.read_csv("data/processed/knbs_cpi_structured.csv")

    if "overall_cpi" not in knbs.columns:
        print("  ⚠️  overall_cpi column not found — check cleaning pipeline")
        return

    series = prepare_cpi_series(knbs)
    print(f"\n  CPI series: {len(series)} months "
          f"({series.index.min()} → {series.index.max()})")

    print("\n  Training ARIMA baseline...")
    arima_model, arima_forecast = train_arima(series)
    print("  ARIMA trained ✅")

    print("\n  Training Prophet...")
    prophet_model, forecast_df, test_df = train_prophet(knbs)
    if prophet_model:
        print("  Prophet trained ✅")

    print("\n  ✅ Model 2 complete")


if __name__ == "__main__":
    main()
