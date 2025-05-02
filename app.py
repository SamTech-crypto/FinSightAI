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

# Updated Tailwind-style custom CSS with adjustments for the top space
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Main Container Styling */
    .main {
        background: linear-gradient(135deg, #e0e7ff 0%, #f4f7fb 100%);
        min-height: 100vh;
        padding: 1rem; /* Reduced padding to minimize empty space */
        font-family: 'Inter', sans-serif;
    }

    /* Header Section to Fill Top Space */
    .header {
        background: #1E3A8A;
        padding: 1rem;
        border-radius: 0.75rem 0.75rem 0 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    /* Titles */
    .title {
        font-size: 2.5rem; /* Slightly smaller for better fit */
        font-weight: 700;
        color: #ffffff; /* White text on dark header */
        margin-bottom: 0.5rem; /* Reduced margin to bring tabs closer */
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .subtitle {
        font-size: 1.75rem;
        font-weight: 600;
        color: #3B82F6;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #DBEAFE;
        padding-bottom: 0.5rem;
    }

    /* Text Input Styling */
    .stTextInput input {
        border-radius: 0.5rem;
        border: 2px solid #93C5FD;
        padding: 1rem;
        font-size: 1.1rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    /* Button Styling */
    .stButton button {
        background: linear-gradient(to right, #3B82F6, #1D4ED8);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        transition: background 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(to right, #2563EB, #1E3A8A);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
    }

    /* Custom Card for displaying tables */
    .dataframe-card {
        background: #F9FAFB;
        border-radius: 0.75rem;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #3B82F6;
    }

    /* Card Styling */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    /* Tab Styling */
    .stTabs [role="tablist"] {
        border-bottom: 2px solid #DBEAFE;
    }

    .stTabs [role="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        color: #6B7280;
        padding: 0.75rem 1.5rem;
        transition: color 0.3s ease;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        color: #1D4ED8;
        border-bottom: 3px solid #1D4ED8;
    }

    .stTabs [role="tab"]:hover {
        color: #3B82F6;
    }

    </style>
""", unsafe_allow_html=True)

# Layout
st.markdown('<div class="main">', unsafe_allow_html=True)

# Add a header section to fill the top space
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<h1 class="title">CFO AI Agent</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Dashboard", "💬 Chatbot"])

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

        # Enhanced Plotly chart with better styling
        fig = px.line(
            forecast, 
            x="Date", 
            y="Forecast", 
            title="Budget Forecast",
            template="plotly_white",
            color_discrete_sequence=["#3B82F6"],
            line_shape="spline"
        )
        fig.update_traces(
            line=dict(width=3),
            hovertemplate="Date: %{x}<br>Forecast: $%{y:.2f}"
        )
        fig.update_layout(
            title_font=dict(size=22, color="#1E3A8A", family="'Inter', sans-serif"),
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            font=dict(family="'Inter', sans-serif", size=14, color="#4B5563"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                gridcolor="#E5E7EB",
                tickfont=dict(size=12),
            ),
            yaxis=dict(
                gridcolor="#E5E7EB",
                tickfont=dict(size=12),
            ),
            hovermode="x unified",
            margin=dict(l=50, r=50, t=80, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display anomalies with better styling
        st.markdown('<h3 class="subtitle">Anomalies Detected</h3>', unsafe_allow_html=True)
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
                st.markdown(f"**Response**: {response}", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error in chatbot response: {e}. Check 'chatbot.py' or API configuration.")

    st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
