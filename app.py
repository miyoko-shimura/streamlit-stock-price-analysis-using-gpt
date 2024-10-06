import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI
import plotly.graph_objects as go
import re

# Streamlit app title
st.title('Stock Analysis App - GPT-4 Analyst')

# Disclaimer
# Concise Legal Disclaimer (approximately 70 words)
st.warning("""
    **LEGAL DISCLAIMER**

    This app provides AI-generated stock analysis for educational purposes only, not financial advice. Information may be inaccurate or outdated. We make no warranties and accept no liability for any losses or decisions based on this data.

    Consult a qualified financial advisor before making investment decisions. By using this app, you agree to these terms and use the information at your own risk.
    """)

# Sidebar for OpenAI API key input
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
client = OpenAI(api_key=api_key)

# User input for stock ticker symbol
ticker = st.text_input('Enter a stock ticker symbol (e.g., AAPL, GOOGL):')

# ... (rest of the code remains the same)
