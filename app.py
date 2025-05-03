import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from dotenv import load_dotenv

# Add 'src' to sys.path for importing custom modules
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import custom modules
try:
    from forecasting import forecast_budget
    from anomaly import detect_anomalies, plot_anomalies
    from chatbot import get_response
except ImportError as e:
    st.error(f"Error importing custom modules: {e}. Ensure 'src' folder contains 'forecasting.py', 'anomaly.py', and 'chatbot.py'.")
    st.stop()

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="CFO AI Agent", layout="wide")

# Load external CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("styles.css not found. Please ensure it exists in the project directory.")
    st.stop()

# Cache data loading
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# Layout
st.markdown('<div class="main">', unsafe_allow_html=True)

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<h1 class="title">CFO AI Agent</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Dashboard", "💬 Chatbot"])

# --- Dashboard Tab ---
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Financial Dashboard</h2>', unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Upload Financial Data (CSV)", type="csv")
    data_path = "data/sample_financials.csv"

    try:
        if uploaded_file:
            data = load_data(uploaded_file)
        elif os.path.exists(data_path):
            data = load_data(data_path)
        else:
            raise FileNotFoundError(f"Financial data file not found at '{data_path}'")

        # Dynamic parameters
        st.markdown("### Configuration")
        threshold = st.slider("IQR Threshold", min_value=1.0, max_value=3.0, value=1.5)
        z_score_threshold = st.slider("Z-Score Threshold", min_value=2.0, max_value=4.0, value=3.0)
        forecast_periods = st.slider("Forecast Periods", min_value=6, max_value=24, value=12)

        # Generate forecast and detect anomalies
        with st.spinner("Generating forecast..."):
            forecast = forecast_budget(data, periods=forecast_periods)
        with st.spinner("Detecting anomalies..."):
            anomalies = detect_anomalies(
                data,
                threshold=threshold,
                z_score_threshold=z_score_threshold
            )

        # Forecast plot
        fig = px.line(
            forecast,
            x="Date",
            y="Forecast",
            title="Budget Forecast",
            template="plotly_white",
            color_discrete_sequence=["#3B82F6"],
            line_shape="spline"
        )
        fig.add_scatter(x=data['Date'], y=data['Amount'], mode='lines', name='Historical', line=dict(color='#6B7280'))
        fig.update_traces(line=dict(width=3), hovertemplate="Date: %{x}<br>Amount: $%{y:.2f}")
        fig.update_layout(
            title_font=dict(size=22, color="#1E3A8A", family="'Inter', sans-serif"),
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            font=dict(family="'Inter', sans-serif", size=14, color="#4B5563"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#E5E7EB", tickfont=dict(size=12)),
            yaxis=dict(gridcolor="#E5E7EB", tickfont=dict(size=12)),
            hovermode="x unified",
            margin=dict(l=50, r=50, t=80, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Anomaly plot
        st.markdown('<h3 class="subtitle">Anomalies Detected</h3>', unsafe_allow_html=True)
        anomaly_fig = plot_anomalies(data, anomalies)
        st.plotly_chart(anomaly_fig, use_container_width=True)

        # Display anomalies
        st.markdown('<div class="dataframe-card">', unsafe_allow_html=True)
        st.dataframe(
            anomalies.style.set_properties(**{
                'background-color': '#F9FAFB',
                'color': '#1F2937',
                'border-color': '#E5E7EB',
                'font-family': "'Inter', sans-serif",
                'font-size': '14px',
            }).highlight_max(subset=['Amount'], color='#FECACA'),
            use_container_width=True
        )
        st.download_button("Download Anomalies", anomalies.to_csv(index=False), "anomalies.csv")
        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure 'data/sample_financials.csv' exists or upload a CSV file.")
    except Exception as e:
        st.error(f"Error processing financial data: {e}. Check 'forecasting.py' or 'anomaly.py' for compatibility issues.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Chatbot Tab ---
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Financial Chatbot</h2>', unsafe_allow_html=True)

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("Chatbot disabled: OpenAI API key not configured.")
    else:
        query = st.text_input("Ask a financial question:", placeholder="E.g., What's our Q1 burn rate?")
        if query:
            with st.spinner("Thinking..."):
                try:
                    response = get_response(query)
                    st.markdown(f"**Response**: {response}", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error in chatbot response: {e}. Check 'chatbot.py' or API configuration.")

    st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
