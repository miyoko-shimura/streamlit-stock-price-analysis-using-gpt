import streamlit as st
import yfinance as yf
import pandas as pd
import openai
import plotly.graph_objects as go

# Streamlit app title
st.title('Stock Analysis App - GPT-4 Genius Analyst')

# Sidebar for OpenAI API key input
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
openai.api_key = api_key

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
            You are a genius financial analyst. Please analyze the following stock data for {ticker}
            and provide insightful analysis for investors.
            
            Latest Close: ${hist['Close'].iloc[-1]:.2f}
            52-Week High: ${hist['High'].max():.2f}
            52-Week Low: ${hist['Low'].min():.2f}
            Average Volume: {hist['Volume'].mean():.0f}

            Please consider current market trends and recent news about the company in your analysis.
            Provide a comprehensive yet concise analysis in about 200-300 words.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",  # Changed to GPT-4
                messages=[{"role": "system", "content": "You are a genius financial analyst."},
                          {"role": "user", "content": prompt}]
            )

            analysis = response.choices[0].message.content
            st.subheader('GPT-4 Analysis')
            st.write(analysis)

        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
