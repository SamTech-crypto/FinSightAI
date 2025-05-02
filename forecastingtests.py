import pytest
import pandas as pd
from src.forecasting import forecast_budget

@pytest.fixture
def sample_data():
    data = {'Date': pd.date_range(start='2023-01-01', periods=24, freq='M'),
            'Amount': [1000 + i * 50 for i in range(24)]}
    return pd.DataFrame(data)

def test_forecast_budget(sample_data):
    forecast = forecast_budget(sample_data)
    assert len(forecast) == 12
    assert 'Date' in forecast.columns
    assert 'Forecast' in forecast.columns
