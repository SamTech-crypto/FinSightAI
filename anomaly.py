import pandas as pd
import numpy as np
import plotly.express as px

def detect_anomalies(
    data: pd.DataFrame,
    amount_col: str = 'Amount',
    account_col: str = 'Account',
    dept_col: str = 'Department',
    threshold: float = 1.5,
    z_score_threshold: float = 3.0
) -> pd.DataFrame:
    """Detect anomalies in financial data using a hybrid IQR and z-score method with logging.
    
    Args:
        data (pd.DataFrame): Input DataFrame with financial data.
        amount_col (str): Column name for amount values. Defaults to 'Amount'.
        account_col (str): Column name for account values. Defaults to 'Account'.
        dept_col (str): Column name for department values. Defaults to 'Department'.
        threshold (float): IQR multiplier for anomaly detection. Defaults to 1.5.
        z_score_threshold (float): Z-score threshold for anomaly detection. Defaults to 3.0.
    
    Returns:
        pd.DataFrame: DataFrame containing detected anomalies with descriptions.
    """
    # Ensure required columns exist
    required_columns = [amount_col, account_col, dept_col]
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Handle missing values
    data = data.dropna(subset=[amount_col])

    # Calculate IQR for Amount
    Q1 = data[amount_col].quantile(0.25)
    Q3 = data[amount_col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    print(f"IQR: {IQR:.2f}, Lower Bound: {lower_bound:.2f}, Upper Bound: {upper_bound:.2f}")

    # Calculate z-scores for Amount
    data['Z_Score'] = (data[amount_col] - data[amount_col].mean()) / data[amount_col].std()

    # Detect anomalies using both IQR and z-score
    is_anomaly = (
        (data[amount_col] < lower_bound) |
        (data[amount_col] > upper_bound) |
        (abs(data['Z_Score']) > z_score_threshold)
    )
    anomalies = data[is_anomaly].copy()

    # Add description for anomalies
    anomalies['Description'] = anomalies.apply(
        lambda row: f"High deviation in {row[dept_col]} department, Account: {row[account_col]}"
        if row[amount_col] > upper_bound or row['Z_Score'] > z_score_threshold
        else f"Low deviation in {row[dept_col]} department, Account: {row[account_col]}",
        axis=1
    )

    # Drop Z_Score column from final output
    anomalies = anomalies.drop(columns=['Z_Score']).reset_index(drop=True)

    if anomalies.empty:
        print("🚫 No anomalies detected.")
    else:
        print(f"✅ Detected {len(anomalies)} anomalies.")

    return anomalies

def plot_anomalies(data: pd.DataFrame, anomalies: pd.DataFrame, date_col: str = 'Date', amount_col: str = 'Amount') -> px.scatter:
    """Create a scatter plot highlighting anomalies in the financial data.
    
    Args:
        data (pd.DataFrame): Original financial data.
        anomalies (pd.DataFrame): Detected anomalies.
        date_col (str): Column name for dates. Defaults to 'Date'.
        amount_col (str): Column name for amounts. Defaults to 'Amount'.
    
    Returns:
        plotly.express.scatter: Plotly figure object.
    """
    data['Is_Anomaly'] = data.index.isin(anomalies.index)
    fig = px.scatter(
        data,
        x=date_col,
        y=amount_col,
        color='Is_Anomaly',
        color_discrete_map={True: '#EF4444', False: '#3B82F6'},
        title='Anomalies in Financial Data',
        template='plotly_white'
    )
    fig.update_traces(marker=dict(size=8), hovertemplate="Date: %{x}<br>Amount: $%{y:.2f}")
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        font=dict(family="'Inter', sans-serif", size=14),
        showlegend=True
    )
    return fig
