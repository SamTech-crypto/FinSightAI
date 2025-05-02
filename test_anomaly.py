import pytest
import pandas as pd
from src.anomaly import detect_anomalies

@pytest.fixture
def sample_data():
    data = {'Date': pd.date_range(start='2023-01-01', periods=24, freq='M'),
            'Amount': [1000 + i * 50 for i in range(24)]}
    data['Amount'][10] = 5000  # Introduce an anomaly
    return pd.DataFrame(data)

def test_detect_anomalies(sample_data):
    anomalies = detect_anomalies(sample_data)
    assert len(anomalies) == 1
    assert anomalies['Amount'].iloc[0] == 5000
