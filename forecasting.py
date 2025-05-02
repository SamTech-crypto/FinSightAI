import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_budget(data: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    """Forecast future budget values using Holt-Winters Exponential Smoothing."""
    # Ensure Date column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    
    model = ExponentialSmoothing(data['Amount'], trend='add', seasonal='add', seasonal_periods=12)
    model_fit = model.fit()
    forecast = model_fit.forecast(periods)
    forecast_dates = pd.date_range(start=data['Date'].max(), periods=periods + 1, freq='M')[1:]
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
    return forecast_df
