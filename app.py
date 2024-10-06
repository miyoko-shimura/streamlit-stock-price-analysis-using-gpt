import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI
import plotly.graph_objects as go
import re

# Streamlit app title
st.title('Stock Analysis App - GPT-4 Genius Analyst')

# Sidebar for OpenAI API key input
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
client = OpenAI(api_key=api_key)

# User input for stock ticker symbol
ticker = st.text_input('Enter a stock ticker symbol (e.g., AAPL, GOOGL):')

if st.button('Analyze'):
    if not ticker:
        st.warning('Please enter a ticker symbol.')
    elif not api_key:
        st.warning('Please enter your OpenAI API key.')
    else:
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            # Display stock price chart
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'])])
            fig.update_layout(title=f'{ticker} Stock Price - Last 12 Months')
            st.plotly_chart(fig)

            # Display basic information
            info = stock.info
            st.subheader('Company Information')
            st.write(f"Company Name: {info.get('longName', 'N/A')}")
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
            
            # GPT-4 analysis
            prompt = f"""
            As a genius financial analyst, please provide a structured analysis of the stock {ticker} based on the following data:

            Latest Close: ${hist['Close'].iloc[-1]:.2f}
            52-Week High: ${hist['High'].max():.2f}
            52-Week Low: ${hist['Low'].min():.2f}
            Average Volume: {hist['Volume'].mean():.0f}

            Please structure your analysis with the following sections, using markdown formatting:

            1. ## Summary
               Provide a brief overview of the stock's performance and potential. NOt use the numbers to prevent error. Add space between numbers and letters. Add space after period. Add space after numbers.

            2. ## Technical Analysis
               Analyze the stock's price movements, trends, and key levels.

            3. ## Fundamental Analysis
               Discuss the company's financial health, market position, and growth prospects.

            4. ## Market Sentiment
               Evaluate current market trends and investor sentiment towards this stock.

            5. ## Risks and Opportunities
               Highlight potential risks and opportunities for investors.


            Ensure each section is concise yet informative. The entire analysis should be about 400 words.
            
            IMPORTANT: Ensure proper spacing between words and symbols. Do not use special characters or emojis.
            Use standard punctuation and formatting. Separate all words and numbers with spaces.
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a genius financial analyst. Provide clear, well-formatted analysis."},
                    {"role": "user", "content": prompt}
                ]
            )

            analysis = response.choices[0].message.content

            # Post-process the analysis to fix any remaining formatting issues
            analysis = re.sub(r'(\d)([A-Za-z])', r'\1 \2', analysis)  # Add space between numbers and letters
            analysis = re.sub(r'([A-Za-z])(\d)', r'\1 \2', analysis)  # Add space between letters and numbers
            analysis = re.sub(r'(\S)([-+*/])', r'\1 \2', analysis)  # Add space before operators
            analysis = re.sub(r'([-+*/])(\S)', r'\1 \2', analysis)  # Add space after operators

            st.subheader('GPT-4 Analysis')
            st.markdown(analysis)

        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
