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
    from anomaly import detect_anomalies
    from chatbot import get_response
except ImportError as e:
    st.error(f"Error importing custom modules: {e}. Ensure 'src' folder contains 'forecasting.py', 'anomaly.py', and 'chatbot.py'.")
    st.stop()

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="CFO AI Agent", layout="wide")

# Tailwind-style custom CSS via CDN
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css');
    
    /* Main Container Styling */
    .main {
        background-color: #f4f7fb;
        min-height: 100vh;
        padding: 2rem;
    }

    /* Card Styling */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }

    /* Titles */
    .title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1D4ED8;
        margin-bottom: 1.5rem;
    }

    .subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4B5563;
        margin-bottom: 1.25rem;
    }

    /* Text Input Styling */
    .stTextInput input {
        border-radius: 0.375rem;
        border: 2px solid #CBD5E1;
        padding: 0.75rem;
        font-size: 1rem;
    }

    /* Button Styling */
    .stButton button {
        background-color: #1D4ED8;
        color: white;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 0.375rem;
        border: none;
    }

    .stButton button:hover {
        background-color: #2563EB;
    }

    /* Custom Card for displaying tables */
    .dataframe-card {
        background-color: #F9FAFB;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    </style>
""", unsafe_allow_html=True)

# Layout
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">CFO AI Agent</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Dashboard", "Chatbot"])

# --- Dashboard Tab ---
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Financial Dashboard</h2>', unsafe_allow_html=True)

    try:
        # Load financial data
        data_path = "data/sample_financials.csv"
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Financial data file not found at '{data_path}'")
        data = pd.read_csv(data_path)

        # Generate forecast and detect anomalies
        forecast = forecast_budget(data)
        anomalies = detect_anomalies(data)

        # Plot forecast
        fig = px.line(forecast, x="Date", y="Forecast", title="Budget Forecast", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Display anomalies
        st.markdown('<h3 class="subtitle">Anomalies Detected</h3>', unsafe_allow_html=True)
        st.markdown('<div class="dataframe-card">', unsafe_allow_html=True)
        st.dataframe(anomalies, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure 'data/sample_financials.csv' exists in the repository.")
    except Exception as e:
        st.error(f"Error processing financial data: {e}. Check 'forecasting.py' or 'anomaly.py' for compatibility issues.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Chatbot Tab ---
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Financial Chatbot</h2>', unsafe_allow_html=True)

    query = st.text_input("Ask a financial question:", placeholder="E.g., What's our Q1 burn rate?")

    if query:
        with st.spinner("Thinking..."):
            try:
                response = get_response(query)
                st.markdown(f"**Response**: {response}")
            except Exception as e:
                st.error(f"Error in chatbot response: {e}. Check 'chatbot.py' or API configuration.")

    st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
