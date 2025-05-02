import streamlit as st
import pandas as pd
import plotly.express as px

# Fix for "ModuleNotFoundError" by adding 'src' to sys.path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from forecasting import forecast_budget
from anomaly import detect_anomalies
from chatbot import get_response

from dotenv import load_dotenv
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="CFO AI Agent", layout="wide")

# Tailwind-style custom CSS via CDN
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css');
    .main { background-color: #f3f4f6; min-height: 100vh; padding: 1.5rem; }
    .card { background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .title { font-size: 2rem; font-weight: bold; color: #1e3a8a; margin-bottom: 1rem; }
    .subtitle { font-size: 1.25rem; font-weight: 600; color: #374151; margin-bottom: 1rem; }
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
        data = pd.read_csv("data/sample_financials.csv")
        forecast = forecast_budget(data)
        anomalies = detect_anomalies(data)

        # Plot forecast
        fig = px.line(forecast, x="Date", y="Forecast", title="Budget Forecast")
        st.plotly_chart(fig, use_container_width=True)

        # Display anomalies
        st.markdown('<h3 class="subtitle">Anomalies Detected</h3>', unsafe_allow_html=True)
        st.dataframe(anomalies, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Chatbot Tab ---
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Financial Chatbot</h2>', unsafe_allow_html=True)

    query = st.text_input("Ask a financial question:", placeholder="E.g., What's our Q1 burn rate?")

    if query:
        with st.spinner("Thinking..."):
            response = get_response(query)
            st.markdown(f"**Response**: {response}")

    st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
