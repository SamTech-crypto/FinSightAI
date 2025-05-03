import pytest
import pandas as pd
import numpy as np
from src.forecasting import forecast_budget

@pytest.fixture
def sample_data():
    """Linear trend data for testing."""
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=24, freq='M'),
        'Amount': [1000 + i * 50 for i in range(24)]
    }
    return pd.DataFrame(data)

@pytest.fixture
def seasonal_data():
    """Seasonal data for testing."""
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=24, freq='M'),
        'Amount': [1000 + 200 * np.sin(i * np.pi / 6) for i in range(24)]
    }
    return pd.DataFrame(data)

@pytest.fixture
def short_data():
    """Short data for testing non-seasonal fallback."""
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=10, freq='M'),
        'Amount': [1000] * 10
    }
    return pd.DataFrame(data)

def test_forecast_budget(sample_data):
    """Test forecast output structure."""
    forecast = forecast_budget(sample_data)
    assert len(forecast) == len(sample_data) + 12
    assert 'Date' in forecast.columns
    assert 'Forecast' in forecast.columns
    assert 'Historical' in forecast.columns

def test_forecast_values(sample_data):
    """Test forecast values are reasonable."""
    forecast = forecast_budget(sample_data)
    forecast_values = forecast['Forecast'].dropna()
    assert forecast_values.min() > sample_data['Amount'].min() * 0.8
    assert forecast_values.max() < sample_data['Amount'].max() * 1.2

def test_seasonal_forecast(seasonal_data):
    """Test forecast with seasonal data."""
    forecast = forecast_budget(seasonal_data, seasonal_periods=12)
    assert len(forecast) == len(seasonal_data) + 12
    forecast_values = forecast['Forecast'].dropna()
    assert forecast_values.std() > 50  # Expect some variation due to seasonality

def test_short_data(short_data):
    """Test fallback to non-seasonal model."""
    forecast = forecast_budget(short_data)
    assert len(forecast) == len(short_data) + 12
    assert forecast['Forecast'].dropna().std() < 10  # Expect stable forecast
