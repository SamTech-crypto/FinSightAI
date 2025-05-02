import pandas as pd

def detect_anomalies(data: pd.DataFrame, threshold: float = 1.5) -> pd.DataFrame:
    """Detect anomalies in financial data using IQR method with logging and adaptive sensitivity."""
    
    # Calculate IQR
    Q1 = data['Amount'].quantile(0.25)
    Q3 = data['Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    print(f"IQR: {IQR:.2f}, Lower Bound: {lower_bound:.2f}, Upper Bound: {upper_bound:.2f}")

    anomalies = data[(data['Amount'] < lower_bound) | (data['Amount'] > upper_bound)]
    
    if anomalies.empty:
        print("🚫 No anomalies detected.")
    else:
        print(f"✅ Detected {len(anomalies)} anomalies.")
    
    return anomalies
