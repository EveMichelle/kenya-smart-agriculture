"""train_forecaster.py — CPI food price forecasting models"""
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def prepare_cpi_series(knbs_df, col="overall_cpi"):
    df = knbs_df.dropna(subset=[col]).copy()
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")[col].sort_index()

def train_arima(series, order=(1,1,1)):
    train = series.iloc[:-6]
    model = ARIMA(train, order=order).fit()
    return model, model.forecast(steps=6)

def train_prophet(knbs_df, col="overall_cpi"):
    try:
        from prophet import Prophet
        df = knbs_df.dropna(subset=[col]).copy()
        df["ds"] = pd.to_datetime(df["date"])
        df["y"]  = df[col]
        train, test = df.iloc[:-6], df.iloc[-6:]
        m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
                    daily_seasonality=False)
        m.fit(train[["ds","y"]])
        future = m.make_future_dataframe(periods=6, freq="MS")
        return m, m.predict(future), test
    except ImportError:
        print("Install prophet: pip install prophet")
        return None, None, None
