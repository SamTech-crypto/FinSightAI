import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_budget(data: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    """Forecast future budget values using Holt-Winters method. Falls back to non-seasonal model if needed."""
    data['Date'] = pd.to_datetime(data['Date'])

    if len(data) < 24:
        # Fallback: Holt's Linear Trend (no seasonality)
        print("⚠️ Not enough data for seasonal model. Using non-seasonal Holt’s Linear Trend instead.")
        model = ExponentialSmoothing(data['Amount'], trend='add', seasonal=None)
    else:
        # Full Holt-Winters with seasonality
        model = ExponentialSmoothing(data['Amount'], trend='add', seasonal='add', seasonal_periods=12)

    model_fit = model.fit()
    forecast = model_fit.forecast(periods)

    forecast_dates = pd.date_range(start=data['Date'].max(), periods=periods + 1, freq='M')[1:]
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
    return forecast_df
