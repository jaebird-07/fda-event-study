"""
fetch_prices.py

Pulls daily stock prices around each FDA approval date so we can
measure how the market reacted to the decision.

Run: python fetch_prices.py
Output: data/event_prices.csv
"""

import pandas as pd
import yfinance as yf
from datetime import timedelta

APPROVALS_FILE = "data/approvals_2025.csv"
OUTPUT_FILE = "data/event_prices.csv"

BUFFER_DAYS = 15


def fetch_window(ticker: str, event_date: pd.Timestamp) -> pd.DataFrame:
    start = event_date - timedelta(days=BUFFER_DAYS)
    end = event_date + timedelta(days=BUFFER_DAYS)

    prices = yf.download(ticker, start=start, end=end, progress=False)

    if prices.empty:
        raise ValueError(f"No price data returned for {ticker}")

    prices = prices[["Close"]].reset_index()
    prices.columns = ["date", "close"]
    prices["ticker"] = ticker
    prices["event_date"] = event_date
    prices["days_from_event"] = (prices["date"] - event_date).dt.days
    return prices


def main():
    approvals = pd.read_csv(APPROVALS_FILE, parse_dates=["approval_date"])
    all_prices = []

    for _, row in approvals.iterrows():
        print(f"Fetching {row['ticker']} around {row['approval_date'].date()}...")
        try:
            window = fetch_window(row["ticker"], row["approval_date"])
            window["company"] = row["company"]
            window["drug"] = row["drug"]
            all_prices.append(window)
        except Exception as e:
            print(f"  Failed for {row['ticker']}: {e}")

    if not all_prices:
        print("No data fetched — check your internet connection and tickers.")
        return

    result = pd.concat(all_prices, ignore_index=True)
    result.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(result)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
