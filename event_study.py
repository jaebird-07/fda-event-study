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

    event_idx = returns.index.get_loc(event_date)

    estimation_window = returns.iloc[event_idx - 210 : event_idx - 10]
    pre_event = returns.iloc[event_idx - 10 : event_idx]
    event_window = returns.iloc[event_idx - 1 : event_idx + 2]
    post_event = returns.iloc[event_idx + 2 : event_idx + 11]

    result = linregress(estimation_window[benchmark], estimation_window[ticker])
    alpha = result.intercept
    beta = result.slope

    def calc_car(window):
        predicted = alpha + beta * window[benchmark]
        abnormal_return = window[ticker] - predicted
        return abnormal_return.sum()

    car_pre = calc_car(pre_event)
    car_event = calc_car(event_window)
    car_post = calc_car(post_event)

    return {
        "ticker": ticker,
        "event_date": event_date,
        "alpha": alpha,
        "beta": beta,
        "car_pre": car_pre,
        "car_event": car_event,
        "car_post": car_post,
    }


result = run_event_study("AZN", "2026-07-14")
print(result)