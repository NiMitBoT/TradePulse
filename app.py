import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import joblib

st.set_page_config(layout="wide")
st.title("TradePulse Analytics: AI NIFTY-50 Predictor")

# Sidebar for live data fetching
with st.sidebar:
    st.header("Control Panel")
    if st.button("Fetch Live Data"):
        nifty = yf.download('^NSEI', start='2021-01-01')
        nifty.to_csv('nifty_data.csv')
        st.success("Live data updated successfully!")

# Load model and raw data
model = joblib.load('tradepulse_model.pkl')
df = pd.read_csv('nifty_data.csv', header=[0, 1], index_col=0, parse_dates=True)
df.columns = df.columns.droplevel(1) 

# Re-calculate indicators
df.ta.rsi(length=14, append=True)
df.ta.macd(append=True)
df.ta.bbands(append=True)
df.dropna(inplace=True)

# Extract features and predict
latest_features = df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], errors='ignore').iloc[-1:]
prediction = model.predict(latest_features)[0]
signal = "🟢 BUY" if prediction == 1 else "🔴 SELL / HOLD"

# Dashboard Layout
st.subheader(f"Latest AI Signal: {signal}")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**NIFTY-50 Price Trend (Last 100 Days)**")
    st.line_chart(df['Close'].tail(100))

with col2:
    st.markdown("**RSI Indicator (Momentum)**")
    st.line_chart(df['RSI_14'].tail(100))