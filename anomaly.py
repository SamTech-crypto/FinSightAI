import pandas as pd
import numpy as np

def detect_anomalies(data: pd.DataFrame, threshold: float = 1.5, z_score_threshold: float = 3.0) -> pd.DataFrame:
    """Detect anomalies in financial data using a hybrid IQR and z-score method with logging."""
    
    # Ensure required columns exist
    required_columns = ['Amount', 'Account', 'Department']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Calculate IQR for Amount
    Q1 = data['Amount'].quantile(0.25)
    Q3 = data['Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    print(f"IQR: {IQR:.2f}, Lower Bound: {lower_bound:.2f}, Upper Bound: {upper_bound:.2f}")

    # Calculate z-scores for Amount
    data['Z_Score'] = (data['Amount'] - data['Amount'].mean()) / data['Amount'].std()
    
    # Detect anomalies using both IQR and z-score
    anomalies_iqr = data[(data['Amount'] < lower_bound) | (data['Amount'] > upper_bound)]
    anomalies_z = data[abs(data['Z_Score']) > z_score_threshold]
    
    # Combine anomalies, avoiding duplicates
    anomalies = pd.concat([anomalies_iqr, anomalies_z]).drop_duplicates().reset_index(drop=True)
    
    # Add description for anomalies
    anomalies['Description'] = anomalies.apply(
        lambda row: f"High deviation in {row['Department']} department, Account: {row['Account']}" 
        if row['Amount'] > upper_bound or row['Z_Score'] > z_score_threshold 
        else f"Low deviation in {row['Department']} department, Account: {row['Account']}", 
        axis=1
    )
    
    # Drop Z_Score column from final output
    anomalies = anomalies.drop(columns=['Z_Score'])
    
    if anomalies.empty:
        print("🚫 No anomalies detected.")
    else:
        print(f"✅ Detected {len(anomalies)} anomalies.")
    
    return anomalies
