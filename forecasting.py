import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import acf
from sklearn.metrics import mean_absolute_error

def forecast_budget(data: pd.DataFrame, periods: int = 12, seasonal_periods: int = None) -> pd.DataFrame:
    """Forecast future budget values using Holt-Winters method with optional seasonality detection.
    
    Args:
        data (pd.DataFrame): Input DataFrame with 'Date' and 'Amount' columns.
        periods (int): Number of periods to forecast. Defaults to 12.
        seasonal_periods (int, optional): Seasonal periodicity. If None, detected automatically.
    
    Returns:
        pd.DataFrame: DataFrame with 'Date', 'Forecast', and 'Historical' columns.
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values('Date')

    # Detect seasonality if not provided
    if seasonal_periods is None and len(data) >= 24:
        lags = acf(data['Amount'], nlags=24, fft=False)
        seasonal_periods = np.argmax(lags[1:]) + 1
        print(f"Detected seasonal period: {seasonal_periods}")
    elif seasonal_periods is None:
        seasonal_periods = 12  # Default

    # Select model based on data length
    if len(data) < 24 or seasonal_periods >= len(data):
        print("⚠️ Not enough data for seasonal model. Using non-seasonal Holt’s Linear Trend.")
        model = ExponentialSmoothing(data['Amount'], trend='add', seasonal=None)
    else:
        model = ExponentialSmoothing(data['Amount'], trend='add', seasonal='add', seasonal_periods=seasonal_periods)

    # Fit model and forecast
    model_fit = model.fit()
    forecast = model_fit.forecast(periods)

    # Calculate MAE for historical fit
    historical_pred = model_fit.fittedvalues
    mae = mean_absolute_error(data['Amount'], historical_pred)
    print(f"Forecast MAE: {mae:.2f}")

    # Create output DataFrame
    forecast_dates = pd.date_range(start=data['Date'].max(), periods=periods + 1, freq='M')[1:]
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Forecast': forecast,
        'Historical': [np.nan] * periods
    })

    # Append historical data
    historical_df = pd.DataFrame({
        'Date': data['Date'],
        'Forecast': [np.nan] * len(data),
        'Historical': data['Amount']
    })

    return pd.concat([historical_df, forecast_df]).reset_index(drop=True)
