import yfinance as yf
import pandas as pd
from scipy.stats import linregress
from datetime import datetime, timedelta

def run_event_study(ticker, event_date, benchmark="^GSPC"):
    event_dt = datetime.strptime(event_date, "%Y-%m-%d")
    start = (event_dt - timedelta(days=320)).strftime("%Y-%m-%d")
    end = (event_dt + timedelta(days=20)).strftime("%Y-%m-%d")

    stock_data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    stock_close = stock_data["Close"][ticker]

    bench_data = yf.download(benchmark, start=start, end=end, auto_adjust=True)
    bench_close = bench_data["Close"][benchmark]

    combined = pd.concat([stock_close, bench_close], axis=1)
    returns = combined.pct_change()

    return returns

azn_returns = run_event_study("AZN", "2026-07-14")
print(azn_returns.shape)
print(azn_returns.head())