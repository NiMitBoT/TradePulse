import yfinance as yf
import pandas as pd

def get_nifty_data():
    print("Connecting to Yahoo Finance...")
    # Ticker for NIFTY 50 is ^NSEI
    # We'll pull 5 years of data for better ML training
    nifty = yf.download('^NSEI', start='2021-01-01', end='2026-04-23')
    
    if nifty.empty:
        print("Failed to fetch data. Check your internet connection.")
    else:
        print("\n--- First 5 rows of NIFTY-50 Data ---")
        print(nifty.head())
        # Save to CSV so we don't have to keep downloading it
        nifty.to_csv('nifty_data.csv')
        print("\nSuccess! Data saved to 'nifty_data.csv'")

if __name__ == "__main__":
    get_nifty_data()