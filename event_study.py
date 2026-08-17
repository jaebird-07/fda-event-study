import yfinance as yf
import pandas as pd
from scipy.stats import linregress
from datetime import datetime, timedelta

def run_event_study(ticker, event_date, benchmark="^GSPC"):
    event_dt = datetime.strptime(event_date, "%Y-%m-%d")
    start = (event_dt - timedelta(days=320)).strftime("%Y-%m-%d")
    end = (event_dt + timedelta(days=20)).strftime("%Y-%m-%d")
    return start, end 

print(run_event_study("AZN","2026-07-14"))
