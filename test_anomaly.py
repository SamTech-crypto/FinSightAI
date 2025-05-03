import pytest
import pandas as pd
from src.anomaly import detect_anomalies

@pytest.fixture
def anomaly_data():
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=10, freq='M'),
        'Amount': [100, 105, 110, 5000, 115, 120, 90, 85, 80, 6000],
        'Account': ['Sales'] * 10,
        'Department': ['Finance'] * 10
    })
    return data

def test_anomalies_detected(anomaly_data):
    anomalies = detect_anomalies(anomaly_data)
    assert not anomalies.empty
    assert len(anomalies) >= 2

def test_description_column(anomaly_data):
    anomalies = detect_anomalies(anomaly_data)
    assert 'Description' in anomalies.columns
