import pandas as pd

def detect_anomalies(data: pd.DataFrame, threshold: float = 1.5) -> pd.DataFrame:
    """Detect anomalies in financial data based on the Interquartile Range (IQR)."""
    Q1 = data['Amount'].quantile(0.25)
    Q3 = data['Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    anomalies = data[(data['Amount'] < lower_bound) | (data['Amount'] > upper_bound)]
    return anomalies
